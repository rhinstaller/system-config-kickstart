#!/usr/bin/python

## raidOptionWindow - code for redhat-config-kickstart's raid dialog
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
import signal
import partWindow

class raidOptionsWindow:
    def __init__(self, xml, part_store, part_view):
        self.xml = xml
        self.part_store = part_store
        self.part_view = part_view
        
        self.raid_options_window = xml.get_widget("raid_options_window")
        self.raid_partition_radio = xml.get_widget("raid_partition_radio")
        self.raid_device_radio = xml.get_widget("raid_device_radio")
        self.raid_options_ok_button = xml.get_widget("raid_options_ok_button")
        self.raid_options_cancel_button = xml.get_widget("raid_options_cancel_button")        
        self.raid_partition_radio.set_active(gtk.TRUE)

        self.raid_options_ok_button.connect("clicked", self.okClicked)
        self.raid_options_cancel_button.connect("clicked", self.destroy)

        self.raid_options_window.show_all()

    def okClicked(self, *args):
        if self.raid_partition_radio.get_active() == gtk.TRUE:
            self.partWindow = partWindow.partWindow(self.xml, self.part_store, self.part_view, "software RAID")
            self.partWindow.add_partition()

        self.raid_options_window.hide()

    def destroy(self, *args):
        self.raid_options_window.hide()
    
