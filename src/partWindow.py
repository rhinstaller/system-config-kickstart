#!/usr/bin/python2.2

## partWindow - event handling code for ksconfig's partitioning dialog
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

##
## I18N
##
import gettext
gettext.bindtextdomain ("ksconfig", "/usr/share/locale")
gettext.textdomain ("ksconfig")
_=gettext.gettext

class partWindow:
    def __init__(self, xml, part_store, part_view):
#        self.partClist = partClist
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
        self.sizeMaxRadio = xml.get_widget("sizeMaxRadio")
        self.maxSizeCombo = xml.get_widget("maxSizeCombo")
        self.formatCheck = xml.get_widget("formatCheck")
        self.partCancelButton = xml.get_widget("part_cancel_button")
        self.partOkButton = xml.get_widget("part_ok_button")
        self.sizeOptionsTable = xml.get_widget("size_options_table")
        self.swap_checkbutton = xml.get_widget("swap_checkbutton")

        self.fsTypeCombo.list.connect("selection-changed", self.on_fsTypeCombo_set_focus_child)
        self.partCancelButton.connect("clicked", self.on_part_cancel_button_clicked)
        self.sizeSetRadio.connect("toggled", self.on_sizeSetRadio_toggled)
        self.onPartCheck.connect("toggled", self.on_onPartCheck_toggled)
        self.onDiskCheck.connect("toggled", self.on_onDiskCheck_toggled)
        self.swap_checkbutton.connect("toggled", self.on_swap_recommended_toggled)
        
        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.mountPointCombo.set_popdown_strings(mountPoints)

#        self.fileTypes = ["ext2", "ext3", "RAID", "Linux Swap", "vfat"]
        self.fileTypes = ["ext2", "ext3", "swap", "vfat"]
        self.fsTypeCombo.set_popdown_strings(self.fileTypes)
        self.fsTypeCombo.list.select_item(0)

    def on_fsTypeCombo_set_focus_child(self, *args):
        curr = self.fsTypeCombo.entry.get_text()
        if curr in self.fileTypes:
            index = self.fileTypes.index(curr)

            if index == 2:
                self.mountPointCombo.set_sensitive(gtk.FALSE)
                self.formatCheck.set_sensitive(gtk.FALSE)
                self.swap_checkbutton.set_sensitive(gtk.TRUE)
#            elif index == 3:
#                self.mountPointCombo.set_sensitive(gtk.FALSE)
#                self.formatCheck.set_sensitive(gtk.TRUE)
            else:
                self.mountPointCombo.set_sensitive(gtk.TRUE)
                self.formatCheck.set_sensitive(gtk.TRUE)
                self.swap_checkbutton.set_sensitive(gtk.FALSE)

    def on_sizeSetRadio_toggled(self, *args):
        self.maxSizeCombo.set_sensitive(self.sizeSetRadio.get_active())

    def on_onPartCheck_toggled(self, *args):
        self.onPartBox.set_sensitive(self.onPartCheck.get_active())
        self.onDiskCheck.set_sensitive(not self.onPartCheck.get_active())

    def on_onDiskCheck_toggled(self, *args):
        self.onDiskBox.set_sensitive(self.onDiskCheck.get_active())
        self.onPartCheck.set_sensitive(not self.onDiskCheck.get_active())

    def add_partition(self):
        self.ok_handler = self.partOkButton.connect("clicked", self.on_ok_button_clicked)
        self.win_reset()
        self.partitionDialog.show_all()

    def edit_partition(self, rowData, selected_row):
        self.selected_row = selected_row
        self.ok_handler = self.partOkButton.connect("clicked", self.on_edit_ok_button_clicked)
        self.win_reset()

        (mountPoint, fsType, size, fixedSize, setSize, setSizeVal, maxSize,
         asPrimary, onDisk, onDiskVal, onPart,
         onPartVal, doFormat, None, None, None) = rowData
        self.mountPointCombo.entry.set_text(mountPoint)
        self.fsTypeCombo.entry.set_text(fsType) 
        self.sizeCombo.set_text(size) 
        self.asPrimaryCheck.set_active(asPrimary)
        self.onDiskCheck.set_active(onDisk)
        self.onDiskEntry.set_text(str(onDiskVal))
        self.onPartCheck.set_active(onPart)
        self.onPartEntry.set_text(str(onPartVal))
        self.sizeFixedRadio.set_active(fixedSize)
        self.maxSizeCombo.set_text(str(maxSize))
        self.formatCheck.set_active(doFormat)        

        curr = self.fsTypeCombo.entry.get_text()
        if curr in self.fileTypes:
            index = self.fileTypes.index(curr)
        
            if index == 2:
                self.mountPointCombo.set_sensitive(gtk.FALSE)
                self.formatCheck.set_sensitive(gtk.FALSE)


        self.partitionDialog.show_all()

    def win_reset(self):
        self.mountPointCombo.entry.set_text("")
        self.mountPointCombo.set_sensitive(gtk.TRUE)
#        self.fsTypeCombo.entry.set_text("") 
        self.fsTypeCombo.list.select_item(1)
        self.sizeCombo.set_text("") 
        self.asPrimaryCheck.set_active(gtk.FALSE)
        self.onDiskCheck.set_active(gtk.FALSE)
        self.onDiskEntry.set_text("")
        self.onPartCheck.set_active(gtk.FALSE)
        self.onPartEntry.set_text("")
        self.sizeFixedRadio.set_active(gtk.TRUE)
        self.maxSizeCombo.set_text("1")
        self.formatCheck.set_active(gtk.TRUE)
        
    def on_part_cancel_button_clicked(self, *args):
        self.partOkButton.disconnect(self.ok_handler)
        self.partitionDialog.hide()
        self.win_reset()

    def on_edit_ok_button_clicked(self, *args):
        rowData = self.getData()

        if rowData:
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, 
             onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData

            self.partClist.set_text(self.selected_row, 0, mountPoint)
            self.partClist.set_text(self.selected_row, 1, fsType)
            self.partClist.set_text(self.selected_row, 2, size)
            self.partClist.set_text(self.selected_row, 3, onDiskVal)
            self.partClist.set_row_data(self.selected_row, rowData)
            
            self.partOkButton.disconnect(self.ok_handler)
            self.partitionDialog.hide()
            self.win_reset()

    def on_ok_button_clicked(self, *args):
        rowData = self.getData()

        if rowData:
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, 
             onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData

            iter = self.part_store.append()
            self.part_store.set_value(iter, 0, mountPoint)
            self.part_store.set_value(iter, 1, fsType)
            self.part_store.set_value(iter, 2, size)
            self.part_store.set_value(iter, 3, fixedSize)
            self.part_store.set_value(iter, 4, setSize)
            self.part_store.set_value(iter, 5, setSizeVal)
            self.part_store.set_value(iter, 6, maxSize)
            self.part_store.set_value(iter, 7, asPrimary)
            self.part_store.set_value(iter, 8, onDisk)
            self.part_store.set_value(iter, 9, onDiskVal)
            self.part_store.set_value(iter, 10, onPart)
            self.part_store.set_value(iter, 11, onPartVal)
            self.part_store.set_value(iter, 12, doFormat)
            self.part_store.set_value(iter, 13, raidType)
            self.part_store.set_value(iter, 14, raidSpares)
            self.part_store.set_value(iter, 15, isRaidDevice)
            
#            row = self.partClist.append([mountPoint, fsType, size, onDiskVal])
#            self.partClist.set_row_data(row, rowData)

            self.partOkButton.disconnect(self.ok_handler)
            self.partitionDialog.hide()
            self.win_reset()

    def on_swap_recommended_toggled(self, *args):
        active = self.swap_checkbutton.get_active()
        self.sizeOptionsTable.set_sensitive(not active)

    def getData(self):
        onDiskVal = ""
        onPartVal = ""
        setSizeVal = ""

        mountPoint = self.mountPointCombo.entry.get_text()
        fsType = self.fsTypeCombo.entry.get_text()

##      size stuff

        size = self.sizeCombo.get_text()

        if self.swap_checkbutton.get_active() == 1:
            size = "recommended"

        fixedSize = self.sizeFixedRadio.get_active()
        setSize = self.sizeSetRadio.get_active()
        if setSize == 1:
            setSizeVal = self.maxSizeCombo.get_text()
        maxSize = self.sizeMaxRadio.get_active()

##

        asPrimary = self.asPrimaryCheck.get_active()

        onDisk = self.onDiskCheck.get_active()
        if onDisk == 1:
            onDiskVal = self.onDiskEntry.get_text()

        onPart = self.onPartCheck.get_active()
        if onPart == 1:
            onPartVal = self.onPartEntry.get_text()

        doFormat = self.formatCheck.get_active()

        if size < 1 or size == "" and onPart == gtk.FALSE:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, _("You must specify a size for the partition."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                selectDialog.hide()
            return

        if fsType == "RAID":
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
                return
                
            elif onDisk and onPart:
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        _("onPart and onDisk can not be used at the same time."))
                dlg.set_title(_("Error"))
                dlg.set_default_size(100, 100)
                dlg.set_position (gtk.WIN_POS_CENTER)
                dlg.set_border_width(2)
                dlg.set_modal(gtk.TRUE)
                rc = dlg.run()
                if rc == gtk.RESPONSE_OK:
                    dlg.hide()
                return                

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
                return

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
                return

        elif fsType != "RAID":
            if fsType != "swap":
                if mountPoint == "":
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
                    return

        if fsType == "swap":   
            fsType = "swap"
            mountPoint = ""

        if onDisk and onPart:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                                        _("onPart and onDisk can not be used at the same time."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            return                

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
            return

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
            return

        rowData = [mountPoint, fsType, size, fixedSize, setSize,
                   setSizeVal, maxSize, asPrimary, 
                   onDisk, onDiskVal, onPart, onPartVal,
                   doFormat, "", "", ""]

        return rowData
