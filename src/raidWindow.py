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
import signal
import partWindow
import raidWindow
import partEntry

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class raidWindow:
    def __init__(self, xml, part_store, part_view):
        self.xml = xml
        self.part_store = part_store
        self.part_view = part_view
        
        self.raid_window = xml.get_widget("raid_window")
        self.raid_mp_combo = xml.get_widget("raid_mp_combo")
        self.raid_fsType_menu = xml.get_widget("raid_fsType_menu")
        self.raid_device_menu = xml.get_widget("raid_device_menu")
        self.raid_level_menu = xml.get_widget("raid_level_menu")
        self.raid_partitions_view = xml.get_widget("raid_partitions_view")
        self.raid_spares_spin = xml.get_widget("raid_spares_spin")
        self.raid_ok_button = xml.get_widget("raid_ok_button")
        self.raid_cancel_button = xml.get_widget("raid_cancel_button")        

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
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

    def addPartition(self):
        self.raid_partition_store.clear()
        self.part_store.foreach(self.countRaidPartitions)
        self.raid_window.show_all()

    def countRaidPartitions(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)
        if part_object and part_object.raidNumber:
            new_iter = self.raid_partition_store.append()
            self.raid_partition_store.set_value(new_iter, 0, gtk.FALSE)
            self.raid_partition_store.set_value(new_iter, 1, part_object.raidNumber)
            self.raid_partition_store.set_value(new_iter, 2, iter)
            self.raid_partition_store.set_value(new_iter, 3, part_object)

    def partitionToggled(self, data, row):
        iter = self.raid_partition_store.get_iter((int(row),))
        val = self.raid_partition_store.get_value(iter, 0)
        self.raid_partition_store.set_value(iter, 0 , not val)

    def okClicked(self, *args):
        self.partition_list = []
        mount_point = self.raid_mp_combo.entry.get_text()
        fsType = self.raid_fsType_menu.get_children()[0].get_text()
        raid_device = self.raid_device_menu.get_children()[0].get_text()
        raid_level = self.raid_level_menu.get_children()[0].get_text()

        self.raid_object = partEntry.partEntry()
        self.raid_object.mountPoint = mount_point
        self.raid_object.raidDevice = raid_device
        self.raid_object.raidLevel = raid_level
        self.raid_object.fsType = fsType
        self.raid_object.doFormat = 1
        self.raid_object.isRaidDevice = 1
        
        self.raid_partition_store.foreach(self.isRowToggled, mount_point)

        print "raid level is", raid_level
        print len(self.partition_list)

        if raid_level == "0" or raid_level == "1":
            if len(self.partition_list) < 2:
                device_is_valid = self.deviceNotValid(_("You must select at least 2 partitions in order to use "
                                      "RAID %s" % raid_level))
            else:
                device_is_valid = 1
        elif raid_level == "5":
            if len(self.partition_list) < 3:
                device_is_valid = self.deviceNotValid(_("You must select at least 3 partitions in order to use "
                                      "RAID %s" % raid_level))
            else:
                device_is_valid = 1

        if device_is_valid:
            self.raid_parent_iter = None
            self.part_store.foreach(self.checkForRaidParent)

            if self.raid_parent_iter == None:
                self.raid_parent_iter = self.part_store.append(None)
                self.part_store.set_value(self.raid_parent_iter, 0, (_("Raid Devices")))


            raid_device_iter = self.part_store.append(self.raid_parent_iter)
            self.part_store.set_value(raid_device_iter, 0, mount_point)


            self.num_raid_devices = None
            self.part_store.foreach(self.countRaidDevices)

            self.part_store.set_value(raid_device_iter, 0, self.raid_object.raidDevice)
            self.part_store.set_value(raid_device_iter, 1, self.raid_object.mountPoint)
            self.part_store.set_value(raid_device_iter, 2, self.raid_object.fsType)
            self.part_store.set_value(raid_device_iter, 5, self.raid_object)

            if self.raid_object.doFormat == 1:
                self.part_store.set_value(raid_device_iter, 3, (_("Yes")))
            else:
                self.part_store.set_value(raid_device_iter, 3, (_("No")))

            self.part_view.expand_all()

            self.raid_window.hide()

    def checkForRaidParent(self, store, data, iter):
        if self.part_store.get_value(iter, 0) == (_("Raid Devices")):
            self.raid_parent_iter = iter

    def isRowToggled(self, store, data, iter, mount_point):
        if self.raid_partition_store.get_value(iter, 0) == gtk.TRUE:
            print "row is true"
            self.partition_list.append(self.raid_partition_store.get_value(iter, 1))
            partition_iter = self.raid_partition_store.get_value(iter,2)
            part_object = self.raid_partition_store.get_value(iter, 3)
            print part_object

#            raid_number = part_object.raidNumber
            self.raid_object.raidPartitions.append(part_object.raidNumber)
            self.raid_object.raidPartitionObjects.append(part_object)
            self.part_store.set_value(partition_iter, 1, self.raid_object.raidDevice)

    def countRaidDevices(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)
        if part_object:
            print part_object.device

            if part_object.device[:2] == 'md':
                print "raid object found"
                self.num_raid_devices = self.num_raid_devices + 1
        
    def deviceNotValid(self, label):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, label)
        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER)
        dlg.set_border_width(2)
        dlg.set_modal(gtk.TRUE)
        rc = dlg.run()
        if rc == gtk.RESPONSE_OK:
            dlg.hide()
        return None

    def destroy(self, *args):
        self.raid_window.hide()
    
