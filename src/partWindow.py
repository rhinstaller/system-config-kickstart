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
import gnome.ui


class partWindow:
    def destroy(self, args):
        self.dialog.destroy()

    def __init__(self, xml, partClist):
        self.xml = xml
        self.partClist = partClist
        self.partitionDialog = self.xml.get_widget("partition_dialog")
        self.partitionDialog.connect ("destroy", self.destroy)
        self.mountPointCombo = self.xml.get_widget("mountPointCombo")
        self.fsTypeCombo = self.xml.get_widget("fsTypeCombo")
        self.sizeCombo = self.xml.get_widget("sizeCombo")
        self.asPrimaryCheck = self.xml.get_widget("asPrimaryCheck")
        self.asPrimaryNumCheck = self.xml.get_widget("asPrimaryNumCheck")
        self.asPrimaryNumCombo = self.xml.get_widget("asPrimaryNumCombo")
        self.asPrimaryNumBox = self.xml.get_widget("asPrimaryNumBox")
        self.onDiskCheck = self.xml.get_widget("onDiskCheck")
        self.onDiskEntry = self.xml.get_widget("onDiskEntry")
        self.onDiskBox = self.xml.get_widget("onDiskBox")
        self.onPartCheck = self.xml.get_widget("onPartCheck")
        self.onPartEntry = self.xml.get_widget("onPartEntry")
        self.onPartBox = self.xml.get_widget("onPartBox")
        self.sizeFixedRadio = self.xml.get_widget("sizeFixedRadio")
        self.sizeSetRadio = self.xml.get_widget("sizeSetRadio")
        self.sizeMaxRadio = self.xml.get_widget("sizeMaxRadio")
        self.maxSizeCombo = self.xml.get_widget("maxSizeCombo")
        self.formatRadio = self.xml.get_widget("formatRadio")

#        self.fsTypeCombo.list.connect("selection-changed", self.on_fsTypeCombo_set_focus_child)
#        self.fsTypeCombo.list.connect("key-release-event", self.on_fsTypeCombo_set_focus_child)
#        self.fsTypeCombo.list.connect("button-release-event", self.on_fsTypeCombo_set_focus_child)
        
        self.xml.signal_autoconnect (
            { "on_cancel_part_button_clicked" : self.on_cancel_part_button_clicked,
              "on_ok_button_clicked" : self.on_ok_button_clicked,
              "on_sizeSetRadio_toggled" : self.on_sizeSetRadio_toggled,
              "on_onPartCheck_toggled" : self.on_onPartCheck_toggled,
              "on_onDiskCheck_toggled" : self.on_onDiskCheck_toggled,
              "on_asPrimaryCheck_toggled" : self.on_asPrimaryCheck_toggled,
              "on_asPrimaryNumCheck_toggled" : self.on_asPrimaryNumCheck_toggled,
#              "on_fsTypeCombo_set_focus_child" : self.on_fsTypeCombo_set_focus_child,
              })

#        deviceList = ["/dev/hda", "/dev/hdb", "/dev/hdc", "/dev/hdb"]
#        self.deviceCombo.set_popdown_strings(deviceList)

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

        self.fileTypes = ["ext2", "ext3", "reiserFS", "RAID partition", "Linux Swap"]
        self.fsTypeCombo.set_popdown_strings(self.fileTypes)

        #if swap, disable mount points

        self.win_reset()
        self.partitionDialog.show_all()

##  FIXME --make this work later...no time now
##     def on_fsTypeCombo_set_focus_child(self, *args):
##         if self.mountPointCombo.entry.get_text() != "" and self.mountPointCombo.entry.get_text() != "<Not Applicable>":
##             print "here"
##             print self.mountPointCombo.entry.get_text()

##             self.data = ""
## #            self.data = self.mountPointCombo.entry.get_text()
##         else:
##             print "there"
## #            self.data = ""
##             self.data = self.mountPointCombo.entry.get_text()

##         item = self.fsTypeCombo.entry.get_text()
##         try:
##             if self.fileTypes.index(item) == 3:
##                 self.mountPointCombo.entry.set_text("<Not Applicable>")
##                 self.mountPointCombo.set_sensitive(FALSE)
##             else:
##                 self.mountPointCombo.entry.set_text(self.data)
##                 self.mountPointCombo.set_sensitive(TRUE)
##         except:
##             pass
            
    def on_sizeSetRadio_toggled(self, *args):
        self.maxSizeCombo.set_sensitive(self.sizeSetRadio.get_active())

    def on_onPartCheck_toggled(self, *args):
        self.onPartBox.set_sensitive(self.onPartCheck.get_active())

    def on_onDiskCheck_toggled(self, *args):
        self.onDiskBox.set_sensitive(self.onDiskCheck.get_active())

    def on_asPrimaryCheck_toggled(self, *args):
        self.asPrimaryNumBox.set_sensitive(self.asPrimaryCheck.get_active())

    def on_asPrimaryNumCheck_toggled(self, *args):
        self.asPrimaryNumCombo.set_sensitive(self.asPrimaryNumCheck.get_active())

    def win_reset(self):
        self.mountPointCombo.entry.set_text("")
        self.fsTypeCombo.entry.set_text("") 
        self.sizeCombo.set_text("") 
        self.asPrimaryCheck.set_active(FALSE)
        self.asPrimaryNumCheck.set_active(FALSE)
        self.onDiskCheck.set_active(FALSE)
        self.onDiskEntry.set_text("")
        self.onPartCheck.set_active(FALSE)
        self.onPartEntry.set_text("")
        self.sizeFixedRadio.set_active(TRUE)
        self.maxSizeCombo.set_text("1")
        self.formatRadio.set_active(TRUE)
        
    def on_cancel_part_button_clicked(self, *args):
        self.partitionDialog.hide()
        self.win_reset()

    def on_ok_button_clicked(self, *args):
        onDiskVal = 0
        onPartVal = 0
        setSizeVal = 0
        asPrimaryNum = 0
        asPrimaryVal = 0

        mountPoint = self.mountPointCombo.entry.get_text()
        fsType = self.fsTypeCombo.entry.get_text()
        size = self.sizeCombo.get_text()

        fixedSize = self.sizeFixedRadio.get_active()
        setSize = self.sizeSetRadio.get_active()
        if setSize == 1:
            setSizeVal = self.setSizeCombo.get_text()
        maxSize = self.sizeMaxRadio.get_active()

        asPrimary = self.asPrimaryCheck.get_active()
        if asPrimary:
            asPrimaryNum = self.asPrimaryNumCheck.get_active()
            if asPrimaryNum:
                asPrimary = 0
                asPrimaryVal = self.asPrimaryNumCombo.entry.get_text()

        onDisk = self.onDiskCheck.get_active()
        if onDisk == 1:
            onDiskVal = self.onDiskEntry.get_text()

        onPart = self.onPartCheck.get_active()
        if onPart == 1:
            onPartVal = self.onPartEntry.get_text()

        doFormat = self.formatRadio.get_active()

#        print mountPoint, fsType, size
#        print "asPrimary ", asPrimary
#        print "onDisk ", onDisk, " ", onDiskVal
#        print "onPart ", onPart, " ", onPartVal

        rowData = [mountPoint, fsType, size, fixedSize, setSize, setSizeVal, maxSize,
                   asPrimary, asPrimaryNum, asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal, doFormat]

        row = self.partClist.append([mountPoint, fsType, size, ""])
        self.partClist.set_row_data(row, rowData)

        self.partitionDialog.hide()
        self.win_reset()

#    def showWin (self):
#        print "showing win"
#        self.partitionDialog.show_all()









