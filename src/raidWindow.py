#!/usr/bin/python

## raidWindow - event handling code for ksconfig's raid dialog
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

class raidWindow:
    def __init__(self, xml, partClist):
        self.xml = xml
        self.partClist = partClist
        self.raidDialog = xml.get_widget("raid_dialog")
        self.raid_mp_combo = xml.get_widget("raid_mp_combo")
        self.raid_fstype_combo = xml.get_widget("raid_fstype_combo")
        self.raid_type_combo = xml.get_widget("raid_type_combo")
        self.raid_members_clist = xml.get_widget("raid_members_clist")
        self.raid_spares_combo = xml.get_widget("raid_spares_combo")
        self.raid_format_check = xml.get_widget("raid_format_check")
        self.raid_format_check.set_active(FALSE)
        self.raid_members_selected = []

        mountPoints = ["/", "/boot", "/home", "/var", "/tmp", "/usr", "/opt"]
        self.raid_mp_combo.set_popdown_strings(mountPoints)

        self.fileTypes = ["ext2", "ext3", "Linux Swap"]
        self.raid_fstype_combo.set_popdown_strings(self.fileTypes)

        self.raidLevels = ["RAID 0", "RAID 1", "RAID 5"]
        self.raid_type_combo.set_popdown_strings(self.raidLevels)

        self.xml.signal_autoconnect (
            { "on_raid_cancel_button_clicked" : self.on_raid_cancel_button_clicked,
              "on_raid_ok_button_clicked" : self.on_raid_ok_button_clicked,
              "on_raid_members_clist_select_row" : self.on_raid_members_clist_select_row,
              "on_raid_members_clist_unselect_row" : self.on_raid_members_clist_unselect_row,
              })

    def on_raid_cancel_button_clicked(self, *args):
        self.win_reset()
        self.raidDialog.hide()

    def on_raid_ok_button_clicked(self, *args):
        print self.get_data()

        self.win_reset()
        self.raidDialog.hide()

    def on_raid_members_clist_select_row(self, data, row, col, event):
        print row
        device = self.raid_members_clist.get_text(row, 0)
        self.raid_members_selected.append(device)
        print self.raid_members_selected
        
    def on_raid_members_clist_unselect_row(self, data, row, col, event):
        device = self.raid_members_clist.get_text(row, 0)
        self.raid_members_selected.remove(device)
        print self.raid_members_selected

    def win_reset(self):
        self.raid_mp_combo.entry.set_text("") 
        self.raid_fstype_combo.entry.set_text("")
        self.raid_fstype_combo.list.select_item(1)
#        self.raid_type_combo.entry.set_text("")  
        self.raid_type_combo.list.select_item(0)
        self.raid_members_clist.clear()
        self.raid_spares_combo.set_text("")
        self.raid_format_check.set_active(TRUE)
                
    def add_raid(self, num_rows):
        self.win_reset()
        self.num_raid_members = 0

        for i in range(num_rows):
#            print i
#            print self.partClist.get_row_data(0)
            rowData = self.partClist.get_row_data(i)
        
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, asPrimaryNum,
             asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData

            if fsType == "RAID":
                print "raid partition found"
                self.num_raid_members = self.num_raid_members + 1
                if onDiskVal != "":
                    self.raid_members_clist.append([onDiskVal])
                elif onPartVal != "":
                    self.raid_members_clist.append([onPartVal])


        self.raidDialog.show_all()

    def get_data(self):
        mountPoint = self.raid_mp_combo.entry.get_text()
        fsType = self.raid_fstype_combo.entry.get_text()
        raidType = self.raid_type_combo.entry.get_text()
#        self.raid_members_clist
        raidSpares = self.raid_spares_combo.get_text()
        doFormat = self.raid_format_check.get_active()
        isRaidDevice = 1

        size = None 
        fixedSize = None 
        setSize = None 
        setSizeVal = None
        maxSize = None
        asPrimary = None
        asPrimaryNum = None
        asPrimaryVal = None
        onDisk = None
        onDiskVal = None
        onPart = None
        onPartVal = None

        for i in range(self.num_raid_members):
            print self.raid_members_clist.get_text(i, 0)




        rowData = [mountPoint, fsType, size, fixedSize, setSize,
                   setSizeVal, maxSize, asPrimary, asPrimaryNum,
                   asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal,
                   doFormat, raidType, raidSpares, isRaidDevice]
        
        return rowData
