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

        self.raid_partition_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING,
                                                  gobject.TYPE_STRING)

        self.checkbox = gtk.CellRendererToggle()
        col = gtk.TreeViewColumn('', self.checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.checkbox.connect("toggled", self.partitionToggled)
        self.raid_partitions_view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.raid_partitions_view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=2)
        self.raid_partitions_view.append_column(col)

        self.raid_partitions_view.set_model(self.raid_partition_store)

        self.raid_ok_button.connect("clicked", self.okClicked)
        self.raid_cancel_button.connect("clicked", self.destroy)

    def addPartition(self):
        self.raid_partition_store.clear()
        iter = self.part_store.get_iter_first()
        while iter:
            part_object = self.part_store.get_value(iter, 5)
            if part_object.raidNumber:
                new_iter = self.raid_partition_store.append()
                self.raid_partition_store.set_value(new_iter, 0, gtk.FALSE)
                self.raid_partition_store.set_value(new_iter, 1, part_object.fsType)
                self.raid_partition_store.set_value(new_iter, 2, part_object.raidNumber)
            iter = self.part_store.iter_next(iter)
        self.raid_window.show_all()

    def partitionToggled(self, data, row):
        iter = self.raid_partition_store.get_iter((int(row),))
        val = self.raid_partition_store.get_value(iter, 0)
        self.raid_partition_store.set_value(iter, 0 , not val)

    def okClicked(self, *args):
        self.raid_window.hide()

    def destroy(self, *args):
        self.raid_window.hide()
    
