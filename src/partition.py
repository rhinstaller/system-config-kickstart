#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001 Red Hat, Inc.
## Copyright (C) 2000, 2001 Brent Fox <bfox@redhat.com>
##                          Tammy Fox <tfox@redhat.com>

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

#Kickstart Configurator Partitions Configuration

from gtk import *
import GtkExtra
import libglade
import partWindow

class partition:
    def __init__(self, xml):
        self.xml = xml
        self.num_rows = 0
        self.clear_mbr_yes_radiobutton = self.xml.get_widget("clear_mbr_yes_radiobutton")
        self.clear_mbr_no_radiobutton = self.xml.get_widget("clear_mbr_no_radiobutton")
        self.remove_parts_none_radiobutton = self.xml.get_widget("remove_parts_none_radiobutton")
        self.remove_parts_all_radiobutton = self.xml.get_widget("remove_parts_all_radiobutton")
        self.remove_parts_Linux_radiobutton = self.xml.get_widget("remove_parts_Linux_radiobutton")
        self.partClist = self.xml.get_widget("partClist")
        self.add_part_button = self.xml.get_widget("add_part_button")
        self.edit_part_button = self.xml.get_widget("edit_part_button")
        self.del_part_button = self.xml.get_widget("del_part_button")
#        self.partitionDialog = self.xml.get_widget("partition_dialog")
        self.checkbox = self.xml.get_widget("checkbox2")

        self.xml.signal_autoconnect (
            { "select_clist" : self.select_clist,
#              "unselect_clist" : self.unselect_clist,
              "addPartition" : self.addPartition,
              "editPartition" : self.editPartition,
              "delPartition" : self.delPartition,
              })

        #populate partitions table with default values
#        bootPartition = ["/boot", "ext2", "35", "No"]
#        self.partClist.append(bootPartition)
#        swapPartition = ["", "Linux Swap", "128", "No"]
#        self.partClist.append(swapPartition)
#        rootPartition = ["/", "ext2", "1000", "Yes"]
#        self.partClist.append(rootPartition)

        #keep track of the number of partitions
	class counterClass:
            def setCounter(self, start):
                self.rowCount = start
            def increment(self):
                self.rowCount = self.rowCount + 1
            def decrement(self):
                self.rowCount = self.rowCount - 1
            def currentVal(self):
                return self.rowCount
                    
        self.num_parts = counterClass()
        self.num_parts.setCounter(3)

#    def select_clist(self, r, c, event):
    def select_clist(self, *args ):
        widget, r, c, event = args
        self.selected_row = r
        self.edit_part_button.set_sensitive(TRUE)
        self.del_part_button.set_sensitive(TRUE)

#    def unselect_clist(self, *args):
#        print "item unselected"
#        self.edit_part_button.set_state(STATE_INSENSITIVE)
#        self.edit_part_button.set_state(STATE_INSENSITIVE)

    def delPartition(self, *args):
        self.num_rows = self.num_rows - 1
#        self.num_parts.decrement()
#        self.partClist.remove(selected[0])
        self.partClist.remove(self.selected_row)
        self.edit_part_button.set_state(STATE_INSENSITIVE)
        self.edit_part_button.set_state(STATE_INSENSITIVE)

    def addPartition(self, *args):
        self.num_rows = self.num_rows + 1
        self.partWindow = partWindow.partWindow(self.xml, self.partClist)
        self.edit_part_button.set_sensitive(TRUE)
        self.del_part_button.set_sensitive(TRUE)

    def editPartition(self, *args):
        pass


        def editEntry(args, editWindow=editWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, selected=s):
            a = mpCombo.entry.get_text()
            b = fsCombo.entry.get_text()
            c = sizeEntry.get_text()
            d = growCombo.entry.get_text()

            partClist.remove(selected[0])

            entry = [ a, b, c, d]
            partClist.insert(selected[0], entry)
            editWindow.destroy()

            editButton.set_state(STATE_INSENSITIVE)
            delButton.set_state(STATE_INSENSITIVE)
        

    def getData(self):
        buf = ""
        num_raid = 0
        print self.num_rows
        for row in range(self.num_rows):
            rowData = self.partClist.get_row_data(row)
            (mountPoint, fsType, size, fixedSize, setSize, setSizeVal, maxSize,
                       asPrimary, asPrimaryNum, asPrimaryVal, onDisk, onDiskVal, onPart, onPartVal, doFormat) = rowData

            if fsType == "RAID partition":
                num_raid = num_raid + 1
                if num_raid < 10:
                    buf = buf + "\n" + "part raid.%d%d" %(0, num_raid)
                else:
                    buf = buf + "\n" + "part raid.%d " %(num_raid)
            else:
                buf = buf + "\n" + "part %s " % (mountPoint)


            buf = buf + "--size %s " % (size)

            if setSize:
                buf = buf + "--grow --maxsize %s " % (setSizeVal)

            elif maxSize:
                buf = buf + "--grow "

            if asPrimary:
                buf = buf + "--asprimary "

            if asPrimaryNum:
                buf = buf + "--onprimary %s " % (asPrimaryVal)

            if onDisk:
                buf = buf + "--ondisk %s " % (onDiskVal)

            if onPart:
                buf = buf + "--onpart %s " % (onPartVal)

            if not doFormat:
                buf = buf + "--noformat "

        return buf


    









##     def getData(self):
##         buf = ""
##         if self.clear_mbr_yes_radiobutton.get_active():
##             buf = buf + "\n" + "zerombr yes"
##         elif self.clear_mbr_no_radiobutton.get_active():
##             buf = buf + "\n" + "zerombr no"			

##         if self.remove_parts_none_radiobutton.get_active():
##             buf = buf
##         elif self.remove_parts_all_radiobutton.get_active():
##             buf = buf + "\n" + "clearpart --all"
##         elif self.remove_parts_Linux_radiobutton.get_active():
##             buf = buf + "\n" + "clearpart --linux"

##         rows = self.num_parts.currentVal()

##         for n in range(rows):
##             print n
##             line = "part"
##             for i in range(4):
##                 if i == 0:
##                     mount = self.partClist.get_text(n, i)
##                     if mount == '':                    
##                         line = line
##                     else:
##                         line = line + " " + mount
##                 elif i == 1:
##                     fsType = self.partClist.get_text(n, i)
##                     if fsType == 'Linux Swap':
##                         line = line + " swap"
##                     elif fsType == 'ext2':
##                         line = line + " "
##                     else:
##                         line = line + " " + fsType
##                 elif i == 2:
##                     size = self.partClist.get_text(n, i)
##                     line = line + " --size " + size
##                 elif i == 3:
##                     grow = self.partClist.get_text(n, i)
##                     if grow == 'Yes':
##                         line = line + " --grow"
##                     else:
##                         line = line

##             buf = buf + "\n" + line
##         return buf
