#!/usr/bin/python

## userWindow - event handling code for userconf's user window
## Copyright (C) 2001 Red Hat, Inc.
## Copyright (C) 2001 Brent Fox <bfox@redhat.com>

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

from gtk import *
from gnome.ui import *
import GtkExtra
import string
import savedialog

import gtk
import signal
import libglade
import gnome.ui

xml = libglade.GladeXML ("./ksconfig.glade", "partition_dialog", domain="ksconfig")

class partWindow:

    def destroy(self, args):
        self.dialog.destroy()

    def __init__(self):
        print "init"
        self.partitionDialog = xml.get_widget("partition_dialog")
        self.partitionDialog.connect ("destroy", self.destroy)
        self.deviceCombo = xml.get_widget("deviceCombo")
        self.mountPointCombo = xml.get_widget("mountPointCombo")
        self.fsTypeCombo = xml.get_widget("fsTypeCombo")

        xml.signal_autoconnect (
            { "on_cancel_part_clicked" : self.on_cancel_part_clicked,
              })

        deviceList = ["/dev/hda", "/dev/hdb", "/dev/hdc", "/dev/hdb"]
        self.deviceCombo.set_popdown_strings(deviceList)

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

        fileTypes = ["ext2", "ext3", "Linux Swap"]
        self.fsTypeCombo.set_popdown_strings(fileTypes)

        #if swap, disable mount points

        self.partitionDialog.show_all()

    def on_cancel_part_clicked(self, *args):
        self.partitionDialog.hide()

#    def showWin (self):
#        print "showing win"
#        self.partitionDialog.show_all()



