#!/usr/bin/python2.2

## partWindow - event handling code for redhat-config-kickstart's partitioning dialog
## Copyright (C) 2001, 2002 Red Hat, Inc.
## Copyright (C) 2001, 2002 Brent Fox <bfox@redhat.com>
## Copyright (C) 2001, 2002 Tammy Fox <tfox@redhat.com>

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

## Authors: Brent Fox <bfox@redhat.com>
##          Tammy Fox <tfox@redhat.com>

import gtk
import gtk.glade
import string
import signal
import partEntry

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class partWindow:
    def __init__(self, xml, part_store, part_view):
        print "in partWindow init", xml
        self.part_store = part_store
        self.part_view = part_view

        self.partitionDialog = xml.get_widget("partition_dialog")
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
        self.sizeSetRadio = xml.get_widget("sizeSetRadio")
        self.sizeSetCombo = xml.get_widget("sizeSetCombo")
        self.sizeMaxRadio = xml.get_widget("sizeMaxRadio")
        self.formatCheck = xml.get_widget("formatCheck")
        self.partCancelButton = xml.get_widget("part_cancel_button")
        self.partOkButton = xml.get_widget("part_ok_button")
        self.sizeOptionsTable = xml.get_widget("size_options_table")
        self.swap_checkbutton = xml.get_widget("swap_checkbutton")

        self.fsTypeCombo.list.connect("selection-changed", self.on_fsTypeCombo_set_focus_child)
        self.partCancelButton.connect("clicked", self.on_part_cancel_button_clicked)
        self.sizeSetRadio.connect("toggled", self.on_sizeSetRadio_toggled)
        self.sizeMaxRadio.connect("toggled", self.on_sizeMaxRadio_toggled)
        self.onPartCheck.connect("toggled", self.on_onPartCheck_toggled)
        self.onDiskCheck.connect("toggled", self.on_onDiskCheck_toggled)
        self.swap_checkbutton.connect("toggled", self.on_swap_recommended_toggled)
        
        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

        self.fsTypesDict = { _("ext2"):"ext2", _("ext3"):"ext3",
                               _("physical volume (LVM)"):"lvm", _("software RAID"):"raid",
                               _("swap"):"swap", "vfat":"vfat"}
        
        self.fsTypes = self.fsTypesDict.keys()
        self.fsTypeCombo.set_popdown_strings(self.fsTypes)
        self.fsTypeCombo.list.select_item(0)

    def on_fsTypeCombo_set_focus_child(self, *args):
        key = self.fsTypeCombo.entry.get_text()

        if key == None or key == "":
            return
        
        index = self.fsTypesDict[key]

        if index == "swap":
            self.mountPointCombo.set_sensitive(gtk.FALSE)
            self.formatCheck.set_sensitive(gtk.FALSE)
            self.swap_checkbutton.set_sensitive(gtk.TRUE)
        elif index == "raid":
            self.mountPointCombo.set_sensitive(gtk.FALSE)
            self.formatCheck.set_sensitive(gtk.FALSE)
        elif index == "lvm":
            self.mountPointCombo.set_sensitive(gtk.FALSE)
            self.formatCheck.set_sensitive(gtk.TRUE)
        else:
            self.mountPointCombo.set_sensitive(gtk.TRUE)
            self.formatCheck.set_sensitive(gtk.TRUE)
            self.swap_checkbutton.set_sensitive(gtk.FALSE)

    def on_sizeSetRadio_toggled(self, *args):
        self.sizeSetCombo.set_sensitive(self.sizeSetRadio.get_active())

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
        part_object = self.part_store.get_value(self.current_iter, 4)
        self.ok_handler = self.partOkButton.connect("clicked", self.on_edit_ok_button_clicked)
        self.win_reset()

        self.mountPointCombo.entry.set_text(part_object.mountPoint)
        self.fsTypeCombo.entry.set_text(part_object.fsType) 
        self.sizeCombo.set_text(part_object.size) 
        self.asPrimaryCheck.set_active(part_object.asPrimary)
        self.onDiskCheck.set_active(part_object.onDisk)
        self.onDiskEntry.set_text(str(part_object.onDiskVal))
        self.onPartCheck.set_active(part_object.onPart)
        self.onPartEntry.set_text(str(part_object.onPartVal))
        
        if part_object.sizeStrategy == "fixed":
            self.sizeFixedRadio.set_active(gtk.TRUE)
        elif part_object.sizeStrategy == "grow":
            self.sizeSetRadio.set_active(gtk.TRUE)
            self.sizeSetCombo.set_text(part_object.sizeSetVal)
        elif part_object.sizeStrategy == "max":
            self.sizeMaxRadio.set_active(gtk.TRUE)
        
        self.formatCheck.set_active(part_object.doFormat)        

        fsTypeKey = self.fsTypeCombo.entry.get_text()
        curr = self.fsTypesDict[fsTypeKey]
        if curr in self.fsTypes:
            index = self.fsTypes.index(curr)
        
            if index == 2:
                self.mountPointCombo.set_sensitive(gtk.FALSE)
                self.formatCheck.set_sensitive(gtk.FALSE)

        self.partitionDialog.show_all()

    def win_reset(self):
        self.mountPointCombo.entry.set_text("")
        self.mountPointCombo.set_sensitive(gtk.TRUE)
        self.fsTypeCombo.list.select_item(1)
        self.sizeCombo.set_text("1") 
        self.asPrimaryCheck.set_active(gtk.FALSE)
        self.onDiskCheck.set_active(gtk.FALSE)
        self.onDiskEntry.set_text("")
        self.onPartCheck.set_active(gtk.FALSE)
        self.onPartEntry.set_text("")
        self.sizeFixedRadio.set_active(gtk.TRUE)
        self.sizeSetCombo.set_text("1")
        self.formatCheck.set_active(gtk.TRUE)
        
    def on_part_cancel_button_clicked(self, *args):
        self.partOkButton.disconnect(self.ok_handler)
        self.win_reset()
        self.partitionDialog.hide()

    def on_edit_ok_button_clicked(self, *args):
        part_object = self.part_store.get_value(self.current_iter, 4)
        self.getData(part_object)

        self.part_store.set_value(self.current_iter, 0, part_object.mountPoint)
        self.part_store.set_value(self.current_iter, 1, part_object.fsType)
        self.part_store.set_value(self.current_iter, 2, part_object.size)
        self.part_store.set_value(self.current_iter, 3, part_object.onDiskVal)
            
        self.partOkButton.disconnect(self.ok_handler)
        self.win_reset()
        self.partitionDialog.hide()

    def on_ok_button_clicked(self, *args):
        part_object = partEntry.partEntry()
        result = self.getData(part_object)

        if not result:
            return
        
        iter = self.part_store.append()
        self.part_store.set_value(iter, 0, part_object.mountPoint)
        self.part_store.set_value(iter, 1, part_object.fsType)
        self.part_store.set_value(iter, 2, part_object.size)
        self.part_store.set_value(iter, 3, part_object.onDiskVal)
        self.part_store.set_value(iter, 4, part_object)

        self.partOkButton.disconnect(self.ok_handler)
        self.win_reset()
        self.partitionDialog.hide()

    def on_swap_recommended_toggled(self, *args):
        active = self.swap_checkbutton.get_active()
        self.sizeOptionsTable.set_sensitive(not active)

    def getData(self, part_object):
        onDiskVal = ""
        onPartVal = ""
        setSizeVal = ""
        raidPartition = None

        part_object.mountPoint = self.mountPointCombo.entry.get_text()
        fsTypeKey = self.fsTypeCombo.entry.get_text()
        part_object.fsType = self.fsTypesDict[fsTypeKey]

        ## size stuff
        if self.swap_checkbutton.get_active() == 1:
            part_object.size = "recommended"
        else:
            part_object.size = self.sizeCombo.get_text()

        if self.sizeFixedRadio.get_active() == gtk.TRUE:
            part_object.sizeStrategy = "fixed"
        elif self.sizeSetRadio.get_active() == gtk.TRUE:
            part_object.sizeStrategy = "grow"
            part_object.setSizeVal = self.sizeSetCombo.get_text()
        elif self.sizeMaxRadio.get_active() == gtk.TRUE:
            part_object.sizeStrategy = "max"

        part_object.asPrimary = self.asPrimaryCheck.get_active()

        part_object.onDisk = self.onDiskCheck.get_active()
        if part_object.onDisk == 1:
            part_object.onDiskVal = self.onDiskEntry.get_text()

        part_object.onPart = self.onPartCheck.get_active()
        if part_object.onPart == 1:
            part_object.onPartVal = self.onPartEntry.get_text()

        part_object.doFormat = self.formatCheck.get_active()

        #Let's do some error checking to make sure things make sense
        if part_object.fsType == "raid":
            result = self.checkRaid(part_object)

            if not result:
                return None
            else:
                part_object.fsType = result

        elif part_object.fsType != "RAID":
            if part_object.fsType != "swap":
                if part_object.mountPoint == "":
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                            _("Specify a mount point for the partition."))
                    dlg.set_title(_("Error"))
                    dlg.set_default_size(100, 100)
                    dlg.set_position (gtk.WIN_POS_CENTER)
                    dlg.set_border_width(2)
                    dlg.set_modal(gtk.TRUE)
                    rc = dlg.run()
                    if rc == gtk.RESPONSE_OK:
                        dlg.hide()
                    return None

        if part_object.fsType == "swap":   
            part_object.fsType = "swap"
            part_object.mountPoint = ""

        #If onDisk is true, let's check for validity for onDiskVal.  Same for onPart
        result = self.checkPartitionValidity(part_object.onDisk, part_object.onDiskVal,
                                             part_object.onPart, part_object.onPartVal)

        if not result:
            return None
        else:
            return 1
        

    def checkRaid(self, part_object):
        fsType = part_object.fsType
        onDisk = part_object.onDisk
        onDiskVal = part_object.onDiskVal
        onPart = part_object.onPart
        onPartVal = part_object.onPartVal

        mountPoint = ""            
        if not onDisk and not onPart:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                    _("To create a new RAID partition, "
                                      "you must specify either a hard drive "
                                      "or an existing partition."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return None

        elif onDisk and onDiskVal == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                    _("Specify a device on which to create the RAID partition."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return None

        elif onPart and onPartVal == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                    _("Specify an existing partition on which to create the RAID partition."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return None

        lastRaidNumber = ""
        iter = self.part_store.get_iter_first()        
        while iter:
            pyObject = self.part_store.get_value(iter, 4)
            if pyObject.fsType == "raid":
                lastRaidNumber = pyObject.raidNumber
            iter = self.part_store.iter_next(iter)        

        if lastRaidNumber == "":
            fsType = "raid"
            part_object.raidNumber = "01"
        else:
            tmpNum = int(lastRaidNumber) + 1
            if tmpNum < 10:
                part_object.raidNumber = "0%s" % str(tmpNum)
            else:
                part_object.raidNumber = str(tmpNum)
            
        #If all the checks pass, then return
        return fsType
    
    def checkPartitionValidity(self, onDisk, onDiskVal, onPart, onPartVal):
        if onDisk and onDiskVal == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        _("Specify a device on which to create the partition."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return None

        elif onPart and onPartVal == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        _("Specify an existing partition to use."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return None
        
        # Everything's good, so return
        return 1
    
