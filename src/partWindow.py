#!/usr/bin/python

## partWindow - event handling code for ksconfig's partitioning dialog
## Copyright (C) 2001 Red Hat, Inc.
## Copyright (C) 2001 Brent Fox <bfox@redhat.com>
## Copyright (C) 2001 Tammy Fox <tfox@redhat.com>

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
import gtk
import signal
import gnome.ui


class partWindow:
    def __init__(self, xml, partClist):
        self.xml = xml
        self.partClist = partClist
        self.partitionDialog = self.xml.get_widget("partition_dialog")
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
        self.formatCheck = self.xml.get_widget("formatCheck")

        self.ok_button = self.xml.get_widget("ok_part_button")

        self.fsTypeCombo.list.connect("selection-changed", self.on_fsTypeCombo_set_focus_child)
#        self.fsTypeCombo.list.connect("key-release-event", self.on_fsTypeCombo_set_focus_child)
#        self.fsTypeCombo.list.connect("button-release-event", self.on_fsTypeCombo_set_focus_child)
        
        self.xml.signal_autoconnect (
            { "on_cancel_part_button_clicked" : self.on_cancel_part_button_clicked,
              "on_sizeSetRadio_toggled" : self.on_sizeSetRadio_toggled,
              "on_onPartCheck_toggled" : self.on_onPartCheck_toggled,
              "on_onDiskCheck_toggled" : self.on_onDiskCheck_toggled,
              "on_asPrimaryCheck_toggled" : self.on_asPrimaryCheck_toggled,
              "on_asPrimaryNumCheck_toggled" : self.on_asPrimaryNumCheck_toggled,
              })

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

#        self.fileTypes = ["ext2", "ext3", "RAID", "Linux Swap", "vfat"]
        self.fileTypes = ["ext2", "ext3", "Linux Swap", "vfat"]
        self.fsTypeCombo.set_popdown_strings(self.fileTypes)
        self.fsTypeCombo.list.select_item(0)

    def on_fsTypeCombo_set_focus_child(self, *args):
        curr = self.fsTypeCombo.entry.get_text()
        if curr in self.fileTypes:
            index = self.fileTypes.index(curr)

            if index == 2:
                self.mountPointCombo.set_sensitive(FALSE)
                self.formatCheck.set_sensitive(FALSE)
#            elif index == 3:
#                self.mountPointCombo.set_sensitive(FALSE)
#                self.formatCheck.set_sensitive(TRUE)
            else:
                self.mountPointCombo.set_sensitive(TRUE)
                self.formatCheck.set_sensitive(TRUE)

    def on_sizeSetRadio_toggled(self, *args):
        self.maxSizeCombo.set_sensitive(self.sizeSetRadio.get_active())

    def on_onPartCheck_toggled(self, *args):
        self.onPartBox.set_sensitive(self.onPartCheck.get_active())
        self.onDiskCheck.set_sensitive(not self.onPartCheck.get_active())

    def on_onDiskCheck_toggled(self, *args):
        self.onDiskBox.set_sensitive(self.onDiskCheck.get_active())
        self.onPartCheck.set_sensitive(not self.onDiskCheck.get_active())

    def on_asPrimaryCheck_toggled(self, *args):
        self.asPrimaryNumBox.set_sensitive(self.asPrimaryCheck.get_active())

    def on_asPrimaryNumCheck_toggled(self, *args):
        self.asPrimaryNumCombo.set_sensitive(self.asPrimaryNumCheck.get_active())

    def add_partition(self):
        self.ok_handler = self.ok_button.connect("clicked", self.on_ok_button_clicked)
        self.win_reset()
        self.partitionDialog.show_all()

    def edit_partition(self, rowData, selected_row):
        self.selected_row = selected_row
        self.ok_handler = self.ok_button.connect("clicked", self.on_edit_ok_button_clicked)
        self.win_reset()

        (mountPoint, fsType, size, fixedSize, setSize, setSizeVal, maxSize,
         asPrimary, asPrimaryNum, asPrimaryVal, onDisk, onDiskVal, onPart,
         onPartVal, doFormat, None, None, None) = rowData
        self.mountPointCombo.entry.set_text(mountPoint)
        self.fsTypeCombo.entry.set_text(fsType) 
        self.sizeCombo.set_text(size) 
        self.asPrimaryCheck.set_active(asPrimary)
        self.asPrimaryNumCheck.set_active(asPrimaryNum)
        self.onDiskCheck.set_active(onDisk)
        self.onDiskEntry.set_text(str(onDiskVal))
        self.onPartCheck.set_active(onPart)
        self.onPartEntry.set_text(str(onPartVal))
        self.sizeFixedRadio.set_active(fixedSize)
        self.maxSizeCombo.set_text(str(maxSize))
        self.formatCheck.set_active(doFormat)        
        self.partitionDialog.show_all()

    def win_reset(self):
        self.mountPointCombo.entry.set_text("")
        self.mountPointCombo.set_sensitive(TRUE)
#        self.fsTypeCombo.entry.set_text("") 
        self.fsTypeCombo.list.select_item(1)
        self.sizeCombo.set_text("") 
        self.asPrimaryCheck.set_active(FALSE)
        self.asPrimaryNumCheck.set_active(FALSE)
        self.onDiskCheck.set_active(FALSE)
        self.onDiskEntry.set_text("")
        self.onPartCheck.set_active(FALSE)
        self.onPartEntry.set_text("")
        self.sizeFixedRadio.set_active(TRUE)
        self.maxSizeCombo.set_text("1")
        self.formatCheck.set_active(TRUE)
        
    def on_cancel_part_button_clicked(self, *args):
        self.ok_button.disconnect(self.ok_handler)
        self.partitionDialog.hide()
        self.win_reset()

    def on_edit_ok_button_clicked(self, *args):
        rowData = self.getData()

        if rowData:
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, asPrimaryNum,
             asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData

            self.partClist.set_text(self.selected_row, 0, mountPoint)
            self.partClist.set_text(self.selected_row, 1, fsType)
            self.partClist.set_text(self.selected_row, 2, size)
            self.partClist.set_text(self.selected_row, 3, onDiskVal)
            self.partClist.set_row_data(self.selected_row, rowData)
            
            self.ok_button.disconnect(self.ok_handler)
            self.partitionDialog.hide()
            self.win_reset()

    def on_ok_button_clicked(self, *args):
        rowData = self.getData()

        if rowData:
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, asPrimaryNum,
             asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData
        
            row = self.partClist.append([mountPoint, fsType, size, onDiskVal])
            self.partClist.set_row_data(row, rowData)

            self.ok_button.disconnect(self.ok_handler)
            self.partitionDialog.hide()
            self.win_reset()

    def getData(self):
        onDiskVal = ""
        onPartVal = ""
        setSizeVal = ""
        asPrimaryNum = 0
        asPrimaryVal = ""

        mountPoint = self.mountPointCombo.entry.get_text()
        fsType = self.fsTypeCombo.entry.get_text()
        size = self.sizeCombo.get_text()

        fixedSize = self.sizeFixedRadio.get_active()
        setSize = self.sizeSetRadio.get_active()
        if setSize == 1:
            setSizeVal = self.maxSizeCombo.get_text()
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

        doFormat = self.formatCheck.get_active()

        if size < 1 or size == "":
            dlg = GnomeMessageBox("You must specify a size for the partition",
                                  MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
            dlg.run_and_close()            
            return

        if fsType == "RAID":
            mountPoint = ""            
            if not onDisk and not onPart:
                dlg = GnomeMessageBox("To create a new RAID partition, "
                                      "you must specify either a hard drive "
                                      "or an existing partition.",
                                      MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
                dlg.run_and_close()
                return
                
            elif onDisk and onPart:
                dlg = GnomeMessageBox("You cannot use onPart and onDisk at the same time",
                                      MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
                dlg.run_and_close()
                return                

            elif onDisk and onDiskVal == "":
                dlg = GnomeMessageBox("You must specify a device to create "
                                      "the RAID partition on.",
                                      MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
                dlg.run_and_close()
                return

            elif onPart and onPartVal == "":
                dlg = GnomeMessageBox("You must specify an existing partition to create "
                                      "the RAID partition on.",
                                      MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
                dlg.run_and_close()
                return

        elif fsType != "RAID":
            if fsType != "Linux Swap":
                if mountPoint == "":
                    dlg = GnomeMessageBox("You must specify a mount point for the partition.",
                                          MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
                    dlg.run_and_close()
                    return
#                return

        if fsType == "Linux Swap":
            fsType = "swap"
            mountPoint = ""

        if onDisk and onPart:
            dlg = GnomeMessageBox("You cannot use onPart and onDisk at the same time",
                                  MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
            dlg.run_and_close()
            return                

        if onDisk and onDiskVal == "":
            dlg = GnomeMessageBox("You must specify a device to create "
                                  "the partition on.",
                                  MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
            dlg.run_and_close()
            return

        elif onPart and onPartVal == "":
            dlg = GnomeMessageBox("You must specify an existing partition to use.",
                                  MESSAGE_BOX_ERROR, STOCK_BUTTON_OK, None)
            dlg.run_and_close()
            return

        rowData = [mountPoint, fsType, size, fixedSize, setSize,
                   setSizeVal, maxSize, asPrimary, asPrimaryNum,
                   asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal,
                   doFormat, "", "", ""]

        return rowData
