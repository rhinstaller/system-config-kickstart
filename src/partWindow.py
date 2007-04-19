## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
## Copyright (C) 2001, 2002, 2003 Tammy Fox <tfox@redhat.com>

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import gtk
import gtk.glade
import string
import signal
import getopt
import re
import partEntry
import kickstartGui

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class partWindow:
    def __init__(self, xml, part_store, part_view):
        self.part_store = part_store
        self.part_view = part_view
        self.hard_drive_parent_iter = None
        self.raid_parent_iter = None
        self.lvm_parent_iter = None
        self.auto_parent_iter = None
        self.device_iter_dict = {}

        self.partitionDialog = xml.get_widget("partition_dialog")
        self.partitionDialog.connect("delete-event", self.on_part_cancel_button_clicked)
        toplevel = xml.get_widget("main_window")
        self.partitionDialog.set_transient_for(toplevel)
        self.partitionDialog.set_icon(kickstartGui.iconPixbuf)
        self.mountPointCombo = xml.get_widget("mountPointCombo")
        self.fsTypeCombo = xml.get_widget("fsTypeCombo")
        self.sizeCombo = xml.get_widget("sizeCombo")
        self.asPrimaryCheck = xml.get_widget("asPrimaryCheck")
        self.onDiskCheck = xml.get_widget("onDiskCheck")
        self.onDiskEntry = xml.get_widget("onDiskEntry")
        self.onDiskBox = xml.get_widget("onDiskBox")
        self.onPartCheck = xml.get_widget("onPartCheck")
        self.onPartEntry = xml.get_widget("onPartEntry")
        self.onPartBox = xml.get_widget("onPartBox")
        self.sizeFixedRadio = xml.get_widget("sizeFixedRadio")
        self.setSizeRadio = xml.get_widget("setSizeRadio")
        self.setSizeCombo = xml.get_widget("setSizeCombo")
        self.sizeMaxRadio = xml.get_widget("sizeMaxRadio")
        self.formatCheck = xml.get_widget("formatCheck")
        self.partCancelButton = xml.get_widget("part_cancel_button")
        self.partOkButton = xml.get_widget("part_ok_button")
        self.sizeOptionsTable = xml.get_widget("size_options_table")
        self.swap_checkbutton = xml.get_widget("swap_checkbutton")

        self.fsTypeCombo.list.connect("selection-changed", self.on_fsTypeCombo_set_focus_child)
        self.partCancelButton.connect("clicked", self.on_part_cancel_button_clicked)
        self.setSizeRadio.connect("toggled", self.on_setSizeRadio_toggled)
        self.sizeMaxRadio.connect("toggled", self.on_sizeMaxRadio_toggled)
        self.onPartCheck.connect("toggled", self.on_onPartCheck_toggled)
        self.onDiskCheck.connect("toggled", self.on_onDiskCheck_toggled)
        self.swap_checkbutton.connect("toggled", self.on_swap_recommended_toggled)

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

        self.fsTypesDict = { _("ext2"):"ext2", _("ext3"):"ext3",
#                               _("physical volume (LVM)"):"lvm",
                             _("software RAID"):"raid",
                             _("swap"):"swap", _("vfat"):"vfat",
                             _("PPC PReP Boot"): "PPC PReP Boot"}

        self.fsTypes = self.fsTypesDict.keys()
        self.fsTypes.sort()
        self.fsTypeCombo.set_popdown_strings(self.fsTypes)

        try:
            fsTypeSelect = self.fsTypes.index("ext3")
        except:
            fsTypeSelect = 0

        self.fsTypeCombo.list.select_item(fsTypeSelect)

    def on_fsTypeCombo_set_focus_child(self, *args):
        key = self.fsTypeCombo.entry.get_text()

        if key == None or key == "":
            return

        index = self.fsTypesDict[key]

        if index == "swap":
            self.mountPointCombo.set_sensitive(False)
            self.formatCheck.set_sensitive(False)
            self.swap_checkbutton.set_sensitive(True)
            if self.swap_checkbutton.get_active() == True:
                self.sizeOptionsTable.set_sensitive(False)
        else:
            self.swap_checkbutton.set_sensitive(False)
            self.sizeOptionsTable.set_sensitive(True)

            if index == "raid":
                self.mountPointCombo.set_sensitive(False)
                self.formatCheck.set_sensitive(True)
            elif index == "lvm":
                self.mountPointCombo.set_sensitive(False)
            elif index == "PPC PReP Boot":
                self.mountPointCombo.set_sensitive(False)
                self.sizeCombo.set_text("8")
            else:
                self.mountPointCombo.set_sensitive(True)
                self.formatCheck.set_sensitive(True)

    def on_setSizeRadio_toggled(self, *args):
        self.setSizeCombo.set_sensitive(self.setSizeRadio.get_active())

    def on_sizeMaxRadio_toggled(self, *args):
        self.sizeCombo.set_sensitive(not self.sizeMaxRadio.get_active())

    def on_onPartCheck_toggled(self, *args):
        self.onPartBox.set_sensitive(self.onPartCheck.get_active())
        self.onDiskCheck.set_sensitive(not self.onPartCheck.get_active())

    def on_onDiskCheck_toggled(self, *args):
        self.onDiskBox.set_sensitive(self.onDiskCheck.get_active())
        self.onPartCheck.set_sensitive(not self.onDiskCheck.get_active())

    def add_partition(self, type=None):
        self.ok_handler = self.partOkButton.connect("clicked", self.on_ok_button_clicked)
        self.win_reset()
        if type == "TYPE_RAID":
            self.fsTypeCombo.entry.set_text(_("software RAID"))
        self.partitionDialog.show_all()

    def edit_partition(self, iter):
        self.current_iter = iter
        part_object = self.part_store.get_value(self.current_iter, 5)
        self.ok_handler = self.partOkButton.connect("clicked", self.on_edit_ok_button_clicked)
        self.win_reset()

        self.mountPointCombo.entry.set_text(part_object.mountPoint)

        for type in self.fsTypesDict.keys():
            if part_object.fsType == self.fsTypesDict[type]:
                fsType = type
                break
        self.fsTypeCombo.entry.set_text(fsType) 
        self.asPrimaryCheck.set_active(part_object.asPrimary)

        if part_object.partition:
            self.onPartCheck.set_active(True)
            self.onPartEntry.set_text(part_object.partition)
        elif part_object.device:
            self.onDiskCheck.set_active(True)
            self.onDiskEntry.set_text(part_object.device)

        self.formatCheck.set_active(part_object.doFormat)

        fsTypeKey = self.fsTypeCombo.entry.get_text()
        curr = self.fsTypesDict[fsTypeKey]
        if curr in self.fsTypes:
            index = self.fsTypes.index(curr)

            if index == 2:
                self.mountPointCombo.set_sensitive(False)
                self.formatCheck.set_sensitive(False)

        self.partitionDialog.show_all()

        if part_object.sizeStrategy == "fixed":
            self.sizeFixedRadio.set_active(True)
        elif part_object.sizeStrategy == "grow":
            self.setSizeRadio.set_active(True)
            self.setSizeCombo.set_text(part_object.setSizeVal)
        elif part_object.sizeStrategy == "max":
            self.sizeMaxRadio.set_active(True)

        #XXX - have to do this after the show_all due to a bug in gtkSpinButton, I suspect
        if part_object.size == "recommended":
            self.swap_checkbutton.set_active(True)
        else:
            self.sizeCombo.set_text(str(part_object.size))

    def win_reset(self):
        self.mountPointCombo.entry.set_text("")
        self.mountPointCombo.set_sensitive(True)
        try:
            fsTypeSelect = self.fsTypes.index("ext3")
        except:
            fsTypeSelect = 0
        self.fsTypeCombo.list.select_item(fsTypeSelect)
        self.sizeCombo.set_text("1") 
        self.sizeCombo.set_sensitive(True)
        self.asPrimaryCheck.set_active(False)
        self.onDiskCheck.set_active(False)
        self.onDiskEntry.set_text("")
        self.onPartCheck.set_active(False)
        self.onPartEntry.set_text("")
        self.sizeFixedRadio.set_active(True)
        self.setSizeCombo.set_text("1")
        self.swap_checkbutton.set_active(False)
        self.formatCheck.set_active(True)

    def on_part_cancel_button_clicked(self, *args):
        self.partOkButton.disconnect(self.ok_handler)
        self.win_reset()
        self.partitionDialog.hide()
        return True

    def on_edit_ok_button_clicked(self, *args):
        part_object = self.part_store.get_value(self.current_iter, 5)
        result = self.formToKickstart(part_object)

        if result is None:
            return

        parent_iter = self.part_store.iter_parent(self.current_iter)

        if not part_object.device:
            # Move the partition object to under the Auto tree.
            if self.part_store.iter_n_children(parent_iter) == 1:
                # If this was previously in a hard drive drop down, we need
                # to remove the now-invalid iter as well.
                oldDevice = self.part_store.get_value(parent_iter, 0)
                try:
                    self.device_iter_dict.pop(oldDevice)
                except KeyError:
                    pass

                # If the current iter is the only child, delete the parent and
                # the child
                self.part_store.remove(self.current_iter)
                self.part_store.remove(parent_iter)
            else:
                # If there are other children, just delete this child
                self.part_store.remove(self.current_iter)

            self.current_iter = self.addPartitionToTree(part_object, self.current_iter)
        else:
            if self.part_store.get_value(parent_iter, 0) != part_object.device:
                if self.part_store.iter_n_children(parent_iter) == 1:
                    # If this was previously in a hard drive drop down, we need
                    # to remove the now-invalid iter as well.
                    oldDevice = self.part_store.get_value(parent_iter, 0)
                    try:
                        self.device_iter_dict.pop(oldDevice)
                    except KeyError:
                        pass

                    # If the current iter is the only child, delete the parent
                    # and the child
                    self.part_store.remove(self.current_iter)
                    self.part_store.remove(parent_iter)
                else:
                    #If there are other children, just delete this child
                    self.part_store.remove(self.current_iter)

                self.current_iter = self.addPartitionToTree(part_object, self.current_iter)

            else:
                if part_object.raidNumber:
                    self.part_store.set_value(self.current_iter, 0, part_object.raidNumber)
                elif part_object.partition:
                    self.part_store.set_value(self.current_iter, 0, part_object.partition)
                else:
                    self.part_store.set_value(self.current_iter, 0, part_object.device)

        self.part_store.set_value(self.current_iter, 1, part_object.mountPoint)
        self.part_store.set_value(self.current_iter, 2, part_object.fsType)
        if part_object.doFormat == 1:
            self.part_store.set_value(self.current_iter, 3, (_("Yes")))
        else:
            self.part_store.set_value(self.current_iter, 3, (_("No")))
        self.part_store.set_value(self.current_iter, 4, part_object.size)
        self.part_store.set_value(self.current_iter, 5, part_object)

        self.part_view.expand_all()

        self.partOkButton.disconnect(self.ok_handler)
        self.win_reset()
        self.partitionDialog.hide()

    def on_ok_button_clicked(self, *args):
        part_object = partEntry.partEntry()
        result = self.formToKickstart(part_object)

        if result is None:
            return
        else:
            self.setValues(part_object)
            self.partOkButton.disconnect(self.ok_handler)
            self.win_reset()
            self.partitionDialog.hide()

    def find_auto_parent(self, store, data, iter):
        if self.part_store.get_value(iter, 0) == (_("Auto")):
                self.auto_parent_iter = iter

    def addPartitionToTree(self, part_object, iter):
        self.auto_parent_iter = None
        self.part_store.foreach(self.find_auto_parent)

        if iter == None:
            self.hard_drive_parent_iter = self.part_store.append(None)
            self.part_store.set_value(self.hard_drive_parent_iter, 0, (_("Hard Drives")))

        if not part_object.device:
            #If they didn't specify a device, create a group called "Auto"
            if self.auto_parent_iter == None:
                self.auto_parent_iter = self.part_store.append(self.hard_drive_parent_iter)
                self.part_store.set_value(self.auto_parent_iter, 0, (_("Auto")))

            #If the auto parent node already exits, just add the new auto partition to it
            iter = self.part_store.append(self.auto_parent_iter)
            self.part_store.set_value(iter, 0, "")

        else:
            #Now, there's a device specified for this partition, so let's see if it already has a parent node
            if part_object.device in self.device_iter_dict.keys():
                #There's already a device parent for this device.  Just add the info
                device_iter = self.device_iter_dict[part_object.device]
                if part_object.partition != None:
                    iter = self.part_store.append(device_iter)
                    self.part_store.set_value(iter, 0, part_object.partition)
                else:
                    iter = self.part_store.append(device_iter)
                    if part_object.raidNumber:
                        self.part_store.set_value(iter, 0, part_object.raidNumber)
                    else:
                        self.part_store.set_value(iter, 0, (_("Auto")))
            else:
                #There's no device parent for this device.  Create one and add it to the device
                device_iter = self.part_store.append(self.hard_drive_parent_iter)
                self.part_store.set_value(device_iter, 0, part_object.device)
                self.device_iter_dict[part_object.device] = device_iter
                if part_object.partition != None:
                    iter = self.part_store.append(device_iter)
                    self.part_store.set_value(iter, 0, part_object.partition)
                else:
                    iter = self.part_store.append(device_iter)
                    if part_object.raidNumber:
                        self.part_store.set_value(iter, 0, part_object.raidNumber)
                    else:
                        self.part_store.set_value(iter, 0, (_("Auto")))

        return iter

    def on_swap_recommended_toggled(self, *args):
        active = self.swap_checkbutton.get_active()
        self.sizeCombo.set_sensitive(not active)
        self.sizeOptionsTable.set_sensitive(not active)

    def deviceFromPartition(self, part):
        if self.isPartitionValid(part) == 1:
            device = part

            if device.startswith("cciss") or device.startswith("rd") or \
               device.startswith("ida") or device.startswith("sx8"):
                device = re.sub("p[0-9]+$", "", device)
            elif device.startswith("i2o"):
                device = re.sub("[0-9]+$", "", device)
            else:
                device = re.sub("[0-9]+$", "", device)
        else:
            return None

        return device

    def formToKickstart(self, part_object):
        onDiskVal = ""
        onPartVal = ""
        setSizeVal = ""
        raidPartition = None

        fsTypeKey = self.fsTypeCombo.entry.get_text()
        part_object.fsType = self.fsTypesDict[fsTypeKey]

        ## size stuff
        if self.swap_checkbutton.get_active() == True:
            part_object.size = "recommended"
            part_object.sizeStrategy = "fixed"
        else:
            part_object.size = self.sizeCombo.get_text()

            if self.sizeFixedRadio.get_active() == True:
                part_object.sizeStrategy = "fixed"
            elif self.setSizeRadio.get_active() == True:
                part_object.sizeStrategy = "grow"
                part_object.setSizeVal = self.setSizeCombo.get_text()
            elif self.sizeMaxRadio.get_active() == True:
                part_object.sizeStrategy = "max"

        part_object.asPrimary = self.asPrimaryCheck.get_active()

        if self.onDiskCheck.get_active() == True:
            device = self.onDiskEntry.get_text()

            if self.isDeviceValid(device) == 1:
                part_object.device = device
            else:
                return None
        else:
            part_object.device = ""

        if self.onPartCheck.get_active() == True:
            part = self.onPartEntry.get_text()
            device = self.deviceFromPartition(part)

            if device == None:
                return None
            else:
                part_object.device = device
                part_object.partition = part
        else:
            part_object.partition = ""

        part_object.doFormat = self.formatCheck.get_active()

        #Let's do some error checking to make sure things make sense
        if part_object.fsType == "raid":
            part_object.mountPoint = ""
            # If it's a raid partition, run it through the checkRaid sanity checker
            if part_object.raidNumber == "":
                if not self.checkRaid(part_object):
                    return None
            else:
                #this already has a raid number, leave it alone
                pass

        else:
            #Erase any exiting raid data if we've edited a RAID partition to be non-RAID
            part_object.raidNumber = ""

            #It's not raid, so move on
            if part_object.fsType == "swap":   
                #If it's a swap partition, set fsType to be swap
                part_object.fsType = "swap"
                part_object.mountPoint = "swap"

            elif part_object.fsType == "PPC PReP Boot":
                part_object.mountPoint = "prepboot"

            else:
                #It's not raid and it's not swap, so it must be a regular partition
                mountPoint = self.mountPointCombo.entry.get_text()

                if mountPoint == "":
                    self.deviceNotValid(_("Specify a mount point for the partition."))
                    return None

                #Check to see if the mount point has already been used
                self.mp_is_duplicate = None
                self.part_store.foreach(self.checkMountPoint, mountPoint)

                if self.mp_is_duplicate:
                    #They are trying to use a mount point already in use.  Let's complain
                    self.deviceNotValid(_("The mount point \"%s\" is already in use.  "
                                          "Please select another mount point." % mountPoint))
                    return None

                part_object.mountPoint = mountPoint

        return 0

    def checkMountPoint(self, store, data, iter, mountPoint):
        #This will scan the part_store and see if there are any duplicate mount points
        part_object = self.part_store.get_value(iter, 5)
        if part_object and part_object.mountPoint == mountPoint:
            self.mp_is_unique = 1

    def checkRaid(self, part_object):
        device = part_object.device
        partition = part_object.partition

        mountPoint = ""
        if not device:
            self.deviceNotValid(_("To create a new RAID partition, you must specify either "
                                  "a hard drive device name or an existing partition."))
            return None

        self.lastRaidNumber = ""
        self.part_store.foreach(self.countRaid, part_object)

        if self.lastRaidNumber == "":
            part_object.raidNumber = "raid.01"
        elif self.lastRaidNumber == None:
            pass
        elif part_object.raidNumber != None:
            tmpNum = 0
            tmpNum = int(self.lastRaidNumber) + 1
            if tmpNum < 10:
                part_object.raidNumber = "raid.0%s" % str(tmpNum)
            else:
                part_object.raidNumber = "raid.%s" % str(tmpNum)

        part_object.mountPoint = part_object.raidNumber

        #If all the checks pass, then return
        return 1

    def countRaid(self, store, data, iter, object):
        part_object = self.part_store.get_value(iter, 5)
        if object == part_object:
            #Don't iterate if we're counting the object that's being edited
            return None

        if part_object and part_object.fsType == "raid":
            tag, number = string.split(part_object.raidNumber, '.')
            if self.lastRaidNumber < number:
                self.lastRaidNumber = number

    def isDeviceValid(self, device):
        if device == "":
            self.deviceNotValid(_("Specify a device on which to create the partition."))
            return 0
        else:
            return 1

    def isPartitionValid(self, partition):
        if partition[-1] in string.digits:
            return 1
        else:
            self.deviceNotValid(_("The partition you specified does not end "
                                     "in a number.  Partitions must have a partition number "
                                     "such as \"hda1\" or \"sda3\"."))
            return 0

    def deviceNotValid(self, label):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, label)
        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER)
        dlg.set_border_width(2)
        dlg.set_modal(True)
        dlg.set_transient_for(self.partitionDialog)
        dlg.set_icon(kickstartGui.iconPixbuf)
        rc = dlg.run()
        if rc == gtk.RESPONSE_OK:
            dlg.hide()
        return None

    def setValues(self, part_object):
        iter = self.part_store.get_iter_first()
        parent = None

        iter = self.addPartitionToTree(part_object, iter)

        self.part_store.set_value(iter, 1, part_object.mountPoint)
        self.part_store.set_value(iter, 2, part_object.fsType)

        if part_object.doFormat == 1:
            self.part_store.set_value(iter, 3, (_("Yes")))
        else:
            self.part_store.set_value(iter, 3, (_("No")))

        self.part_store.set_value(iter, 4, part_object.size)
        self.part_store.set_value(iter, 5, part_object)

        self.part_view.expand_all()

    def populateList(self, kspart):
        part_object = partEntry.partEntry()

        if kspart.mountpoint[:5] == "raid.":
            part_object.raidNumber = kspart.mountpoint[6:]
            part_object.fsType = "raid"
        else:
            part_object.fsType = kspart.fstype
            part_object.mountPoint = kspart.mountpoint

        if kspart.recommended == True:
            part_object.size = "recommended"
        elif kspart.size != 0:
            part_object.size = kspart.size

        if kspart.disk != "":
            part_object.device = kspart.disk

        if kspart.onPart != "":
            part_object.partition = kspart.onPart
            part_object.device = self.deviceFromPartition(kspart.onPart)

        if kspart.grow == True:
            part_object.sizeStrategy = "max"

        if kspart.maxSizeMB != 0:
            part_object.sizeStrategy = "grow"
            part_object.setSizeVal = kspart.maxSizeMB

        if kspart.format == True:
            part_object.doFormat = 1
        else:
            part_object.doFormat = 0

        self.setValues(part_object)
