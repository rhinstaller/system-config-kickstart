#!/usr/bin/python2.2

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
import raidWindow

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class raidOptionsWindow:
    def __init__(self, xml, part_store, part_view, partWindow):
        self.xml = xml
        self.part_store = part_store
        self.part_view = part_view
        self.partWindow = partWindow

        self.raid_options_window = xml.get_widget("raid_options_window")
        self.raid_partition_radio = xml.get_widget("raid_partition_radio")
        self.raid_device_radio = xml.get_widget("raid_device_radio")
        self.raid_options_ok_button = xml.get_widget("raid_options_ok_button")
        self.raid_options_cancel_button = xml.get_widget("raid_options_cancel_button")        
        self.message_label = xml.get_widget("message_label")
        self.raid_partition_radio.set_active(gtk.TRUE)

        self.raidWindow = raidWindow.raidWindow(self.xml, self.part_store, self.part_view)

        self.raid_options_ok_button.connect("clicked", self.okClicked)
        self.raid_options_cancel_button.connect("clicked", self.destroy)

    def showOptionsWindow(self):
        self.countRaidPartitions()
        self.raid_options_window.show_all()

    def countRaidPartitions(self):
        self.list = []

        self.part_store.foreach(self.walkStore)

        num = len(self.list)
        self.message_label.set_text(_("You currently have %d software RAID partition(s) "
                                      "free to use." % num))
        if num > 1:
            self.raid_device_radio.set_active(gtk.TRUE)
            self.raid_device_radio.set_sensitive(gtk.TRUE)
        else:
            self.raid_partition_radio.set_active(gtk.TRUE)
            self.raid_device_radio.set_sensitive(gtk.FALSE)

    def walkStore(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)
        if part_object and part_object.raidNumber:
            self.list.append(part_object.raidNumber)
        
    def okClicked(self, *args):
        if self.raid_partition_radio.get_active() == gtk.TRUE:
            self.partWindow.add_partition("TYPE_RAID")
        else:
            self.raidWindow.addPartition()

        self.raid_options_window.hide()

    def destroy(self, *args):
        self.raid_options_window.hide()
    
