#!/usr/bin/python

## raidWindow - code for redhat-config-kickstart's raid dialog
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

import string
import gtk
import gobject
import getopt
import signal
import partWindow
import raidWindow
import partEntry
import kickstartGui

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'redhat-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class raidWindow:
    def __init__(self, xml, part_store, part_view):
        self.xml = xml
        self.part_store = part_store
        self.part_view = part_view
        self.original_partitions = None
        
        self.raid_window = xml.get_widget("raid_window")
        self.raid_window.connect("delete-event", self.destroy)
        toplevel = self.xml.get_widget("main_window")
        self.raid_window.set_transient_for(toplevel)
        self.raid_window.set_icon(kickstartGui.iconPixbuf)
        self.raid_mp_combo = xml.get_widget("raid_mp_combo")
        self.raid_fsType_menu = xml.get_widget("raid_fsType_menu")
        self.raid_device_menu = xml.get_widget("raid_device_menu")
        self.raid_level_menu = xml.get_widget("raid_level_menu")
        self.raid_partitions_view = xml.get_widget("raid_partitions_view")
        self.raid_spares_spin = xml.get_widget("raid_spares_spin")
        self.raid_format_check = xml.get_widget("raid_format_check")
        self.raid_ok_button = xml.get_widget("raid_ok_button")
        self.raid_cancel_button = xml.get_widget("raid_cancel_button")        

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.fsTypesList = [ "ext2", "ext3", "raid", "swap", "vfat" ]
        self.raidDeviceList = ['md0', 'md1', 'md2', 'md3', 'md4', 'md5',
                               'md6', 'md7', 'md8', 'md9', 'md10', 'md11',
                               'md12', 'md13', 'md14', 'md15']
        self.raidLevelList = [ "0", "1", "5" ]
        
        self.raid_mp_combo.set_popdown_strings(mountPoints)

        self.raid_partition_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING,
                                                  gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)
 
        self.checkbox = gtk.CellRendererToggle()
        col = gtk.TreeViewColumn('', self.checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.checkbox.connect("toggled", self.partitionToggled)
        self.raid_partitions_view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.raid_partitions_view.append_column(col)

        self.raid_partitions_view.set_model(self.raid_partition_store)

        self.raid_ok_button.connect("clicked", self.okClicked)
        self.raid_cancel_button.connect("clicked", self.destroy)
        self.raid_fsType_menu.connect("changed", self.on_raid_fsType_menu_changed)

    def on_raid_fsType_menu_changed(self, *args):
        if self.raid_fsType_menu.get_children()[0].get_text() == "swap":
            #it's a swap partition, so desensitize the mountPoint combo
            self.raid_mp_combo.set_sensitive(gtk.FALSE)
        else:
            self.raid_mp_combo.set_sensitive(gtk.TRUE)            

    def addPartition(self):
        self.raid_partition_store.clear()
        self.original_partitions = None
        self.original_iter = None
        self.part_store.foreach(self.countRaidPartitions)
        self.raid_window.show_all()

    def editDevice(self, iter, part_object):
        self.original_iter = iter
        self.raid_partition_store.clear()
        self.raid_mp_combo.entry.set_text(part_object.mountPoint)

        fsType = part_object.fsType
        index = self.fsTypesList.index(fsType) - 1
        self.raid_fsType_menu.set_history(index)

        device = part_object.raidDevice
        index = self.raidDeviceList.index(device) - 1
        self.raid_device_menu.set_history(index)
        
        level = part_object.raidLevel
        index = self.raidLevelList.index(level) - 1
        self.raid_level_menu.set_history(index)
        
        self.original_partitions = part_object.raidPartitions
        self.part_store.foreach(self.countRaidPartitions, part_object.raidPartitions)

        self.raid_window.show_all()

    def countRaidPartitions(self, store, data, iter, raidPartitions = None):
        part_object = self.part_store.get_value(iter, 5)

        if part_object and part_object.raidNumber:
            new_iter = self.raid_partition_store.append()

            if raidPartitions and part_object.raidNumber in raidPartitions:
                self.raid_partition_store.set_value(new_iter, 0, gtk.TRUE)
            else:
                self.raid_partition_store.set_value(new_iter, 0, gtk.FALSE)
                
            self.raid_partition_store.set_value(new_iter, 1, part_object.raidNumber)
            self.raid_partition_store.set_value(new_iter, 2, iter)
            self.raid_partition_store.set_value(new_iter, 3, part_object)

    def partitionToggled(self, data, row):
        iter = self.raid_partition_store.get_iter((int(row),))
        val = self.raid_partition_store.get_value(iter, 0)
        self.raid_partition_store.set_value(iter, 0 , not val)

    def okClicked(self, *args):
        fsType = self.raid_fsType_menu.get_children()[0].get_text()
        if fsType == "swap":
            mount_point = "swap"
        else:
            mount_point = self.raid_mp_combo.entry.get_text()
            
        raid_device = self.raid_device_menu.get_children()[0].get_text()
        raid_level = self.raid_level_menu.get_children()[0].get_text()

        raid_object = partEntry.partEntry()
        raid_object.mountPoint = mount_point
        raid_object.raidDevice = raid_device
        raid_object.raidLevel = raid_level
        raid_object.fsType = fsType
        raid_object.isRaidDevice = 1

        self.partition_list = []
        self.addRaidDeviceToTree(raid_object)

        self.raid_window.hide()

    def addRaidDeviceToTree(self, raid_object):        
        self.raid_partition_store.foreach(self.isRowToggled, raid_object)

        if raid_object.raidLevel == "0" or raid_object.raidLevel == "1":
            if len(self.partition_list) < 2:
                device_is_valid = self.deviceNotValid(_("You must select at least 2 partitions in order to use "
                                      "RAID %s" % raid_object.raidLevel))
            else:
                device_is_valid = 1
        elif raid_object.raidLevel == "5":
            if len(self.partition_list) < 3:
                device_is_valid = self.deviceNotValid(_("You must select at least 3 partitions in order to use "
                                      "RAID %s" % raid_object.raidLevel))
            else:
                device_is_valid = 1

        if device_is_valid:

            if not self.original_partitions:
                #then this is a new raid device, not one we're just editing
                self.raid_parent_iter = None
                self.part_store.foreach(self.checkForRaidParent)

                if self.raid_parent_iter == None:
                    self.raid_parent_iter = self.part_store.append(None)
                    self.part_store.set_value(self.raid_parent_iter, 0, (_("Raid Devices")))

                raid_device_iter = self.part_store.append(self.raid_parent_iter)
                self.part_store.set_value(raid_device_iter, 0, raid_object.mountPoint)

                self.num_raid_devices = None
                self.part_store.foreach(self.countRaidDevices)

            if self.original_iter:
                raid_device_iter = self.original_iter
                
            self.part_store.set_value(raid_device_iter, 0, raid_object.raidDevice)
            self.part_store.set_value(raid_device_iter, 1, raid_object.mountPoint)
            self.part_store.set_value(raid_device_iter, 2, raid_object.fsType)
            self.part_store.set_value(raid_device_iter, 5, raid_object)

            if self.raid_format_check.get_active() == gtk.TRUE:
                raid_object.doFormat = 1

            if raid_object.doFormat == 1:
                self.part_store.set_value(raid_device_iter, 3, (_("Yes")))
            else:
                self.part_store.set_value(raid_device_iter, 3, (_("No")))
        self.part_view.expand_all()

    def checkForRaidParent(self, store, data, iter):
        if self.part_store.get_value(iter, 0) == (_("Raid Devices")):
            self.raid_parent_iter = iter

    def isRowToggled(self, store, data, iter, raid_object):
        if self.raid_partition_store.get_value(iter, 0) == gtk.TRUE:
            self.partition_list.append(self.raid_partition_store.get_value(iter, 1))
            partition_iter = self.raid_partition_store.get_value(iter,2)
            part_object = self.raid_partition_store.get_value(iter, 3)

            raid_object.raidPartitions.append(part_object.raidNumber)
            raid_object.raidPartitionObjects.append(part_object)
            self.part_store.set_value(partition_iter, 1, raid_object.raidDevice)

        elif self.raid_partition_store.get_value(iter, 0) == gtk.FALSE:
            partition_iter = self.raid_partition_store.get_value(iter,2)
            part_object = self.raid_partition_store.get_value(iter, 3)            
            if self.original_partitions:
                if part_object.raidNumber in self.original_partitions:
                    part_object.raidDevice = ""
                    self.part_store.set_value(partition_iter, 1, "")

    def countRaidDevices(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)
        if part_object:
            if part_object.device and part_object.device[:2] == 'md':
                self.num_raid_devices = self.num_raid_devices + 1
        
    def deviceNotValid(self, label):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, label)
        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER)
        dlg.set_border_width(2)
        dlg.set_modal(gtk.TRUE)
        dlg.set_transient_for(self.raid_window)
        rc = dlg.run()
        if rc == gtk.RESPONSE_OK:
            dlg.hide()
        return None

    def destroy(self, *args):
        self.raid_window.hide()
        return gtk.TRUE

    def populateRaid(self, line):
        raid_object = partEntry.partEntry()
        raid_object.isRaidDevice = 1
        self.original_iter = None
        result = self.parseRaidLine(raid_object, line)

        if result is None:
            return
        else:
#            self.markRaidPartitions(raid_object)
            self.raid_partition_store.foreach(self.markRaidPartitions, raid_object)
            self.addRaidDeviceToTree(raid_object)

    def parseRaidLine(self, raid_object, line):
        opts, raidPartitions = getopt.getopt(line[1:], "d:h", ["level=", "device=", "spares=", "fstype=", "noformat"])

        for (opt, value) in opts:
            if line[0] == "swap":
                raid_object.fsType = "swap"
                raid_object.mountPoint = "swap"
            elif opt == "--fstype":
                raid_object.fsType = value
                raid_object.mountPoint = line[0]

            if opt == "--level":
                raid_object.raidLevel = value
            if opt == "--device":
                raid_object.raidDevice = value
            if opt == "--noformat":
                raid_object.doFormat = 0
            else:
                raid_object.doFormat = 1

        self.partition_list = raidPartitions
        raid_object.raidPartitions = raidPartitions

        self.raid_partition_store.clear()
        self.part_store.foreach(self.countRaidPartitions)

        return 0
    
    def markRaidPartitions(self, store, data, iter, raid_object):
        if self.raid_partition_store.get_value(iter, 1) in raid_object.raidPartitions:

            partition_iter = self.raid_partition_store.get_value(iter, 2)
            part_object = self.raid_partition_store.get_value(iter, 3)
            self.part_store.set_value(partition_iter, 1, raid_object.raidDevice)
