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

class partition:

    def __init__(self, xml):
        self.clear_mbr_yes_radiobutton = xml.get_widget("clear_mbr_yes_radiobutton")
        self.clear_mbr_no_radiobutton = xml.get_widget("clear_mbr_no_radiobutton")
        self.remove_parts_none_radiobutton = xml.get_widget("remove_parts_none_radiobutton")
        self.remove_parts_all_radiobutton = xml.get_widget("remove_parts_all_radiobutton")
        self.remove_parts_Linux_radiobutton = xml.get_widget("remove_parts_Linux_radiobutton")
        self.partClist = xml.get_widget("partClist")
        self.add_part_button = xml.get_widget("add_part_button")
        self.edit_part_button = xml.get_widget("edit_part_button")
        self.del_part_button = xml.get_widget("del_part_button")

        xml.signal_autoconnect (
            { "select_clist" : self.select_clist,
              "unselect_clist" : self.unselect_clist,
              "addPartition" : self.addPartition,
              "editPartition" : self.editPartition,
              "delPartition" : self.delPartition,
              })

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

    def select_clist(_clist, r, c, event):
            selected[0] = r
            self.edit_part_button.set_sensitive(TRUE)
            self.del_part_button.set_sensitive(TRUE)

    def unselect_clist(self, args):
            self.edit_part_button.set_state(STATE_INSENSITIVE)
            self.edit_part_button.set_state(STATE_INSENSITIVE)

    def delPartition(self, args):
            self.num_parts.decrement()
            self.partClist.remove(selected[0])
            self.edit_part_button.set_state(STATE_INSENSITIVE)
            self.edit_part_button.set_state(STATE_INSENSITIVE)

    def addPartition(args):

            addWindow = GtkWindow()
            addWindow.connect("delete_event", deleteEvent)
            addWindow.set_title('Add Partition Entry')
            addWindow.set_border_width(6)
            addWindow.set_default_size(100, 50)

            addTable = GtkTable(5, 2, FALSE)
            addWindow.add(addTable)

            addLabel1 = GtkLabel("Mount Point:")
            addTable.attach(addLabel1, 0, 1, 0, 1)

            mpCombo = GtkCombo()
            addTable.attach(mpCombo, 1, 2, 0, 1)
            list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
            mpCombo.set_popdown_strings(list_items)
            mpCombo.entry.set_editable(TRUE)

            addLabel2 = GtkLabel("Filesystem Type:")
            addTable.attach(addLabel2, 0, 1, 1, 2)

            fsCombo = GtkCombo()
            addTable.attach(fsCombo, 1, 2, 1, 2)
            list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
            fsCombo.set_popdown_strings(list_items)
            fsCombo.entry.set_text("")
            fsCombo.entry.set_editable(TRUE)

            addLabel3 = GtkLabel("Size (M):")
            addTable.attach(addLabel3, 0, 1, 2, 3)

            sizeEntry = GtkEntry()
            addTable.attach(sizeEntry, 1, 2, 2, 3)

            addLabel4 = GtkLabel("Growable:")
            addTable.attach(addLabel4, 0, 1, 3, 4)

            growCombo = GtkCombo()
            addTable.attach(growCombo, 1, 2, 3, 4)
            list_items = [ "No", "Yes" ]			
            growCombo.set_popdown_strings(list_items)
            growCombo.list.select_item(0)
            growCombo.entry.set_editable(FALSE)

            def addEntry(args, addWindow=addWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, num_parts=num_parts):
                    a = mpCombo.entry.get_text()
                    b = fsCombo.entry.get_text()
                    c = sizeEntry.get_text()
                    d = growCombo.entry.get_text()

                    entry = [ a, b, c, d]
                    partClist.append(entry)
                    addWindow.destroy()
                    num_partst.increment()

            ok = GtkButton("OK")
            addTable.attach(ok, 0, 1, 4, 5)
            ok.connect("clicked", addEntry)

            cancelAdd = GtkButton("Cancel")
            addTable.attach(cancelAdd, 1, 2, 4, 5)
            cancelAdd.connect("clicked", addWindow.hide)

            addWindow.show_all()


    def editPartition(self, args):

            editWindow = GtkWindow()
            editWindow.connect("delete_event", deleteEvent)
            editWindow.set_title('Edit Partition Entry')
            editWindow.set_border_width(6)
            editWindow.set_default_size(100, 50)

            editTable = GtkTable(5, 2, FALSE)
            editWindow.add(editTable)

            editLabel1 = GtkLabel("Mount Point:")
            editTable.attach(editLabel1, 0, 1, 0, 1)

            mpCombo = GtkCombo()
            editTable.attach(mpCombo, 1, 2, 0, 1)
            list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
            mpCombo.set_popdown_strings(list_items)
            mpCombo.entry.set_text("")
            mpCombo.entry.set_editable(TRUE)

            editLabel2 = GtkLabel("Filesystem Type:")
            editTable.attach(editLabel2, 0, 1, 1, 2)

            fsCombo = GtkCombo()
            editTable.attach(fsCombo, 1, 2, 1, 2)
            list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
            fsCombo.set_popdown_strings(list_items)
            fsCombo.entry.set_text("")
            fsCombo.entry.set_editable(FALSE)

            editLabel3 = GtkLabel("Size (M):")
            editTable.attach(editLabel3, 0, 1, 2, 3)

            sizeEntry = GtkEntry()
            editTable.attach(sizeEntry, 1, 2, 2, 3)

            editLabel4 = GtkLabel("Growable:")
            editTable.attach(editLabel4, 0, 1, 3, 4)

            growCombo = GtkCombo()
            editTable.attach(growCombo, 1, 2, 3, 4)
            list_items = [ "No", "Yes" ]			
            growCombo.set_popdown_strings(list_items)
            growCombo.entry.set_editable(FALSE)

            for i in range(4):
                    if i == 0:
                            mpCombo.entry.set_text(partClist.get_text(s[0], i))
                    elif i == 1:
                            fsCombo.entry.set_text(partClist.get_text(s[0], i))
                    elif i == 2:
                            sizeEntry.set_text(partClist.get_text(s[0], i))
                    elif i == 3:
                            growCombo.entry.set_text(partClist.get_text(s[0], i))


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
        if mbrRadio1.get_active():
                buf = buf + "\n" + "zerombr yes"
        elif mbrRadio2.get_active():
                buf = buf + "\n" + "zerombr no"			

        if clearRadio1.get_active():
                buf = buf
        elif clearRadio2.get_active():
                buf = buf + "\n" + "clearpart --all"
        elif clearRadio3.get_active():
                buf = buf + "\n" + "clearpart --linux"

        rows = self.num_parts.currentVal()

        for n in range(rows):
                line = "part"
                for i in range(4):

                        if i == 0:
                                mount = self.partClist.get_text(n, i)
                                if mount == '':
                                        line = line
                                else:
                                        line = line + " " + mount
                        elif i == 1:
                                fsType = self.partClist.get_text(n, i)
                                if fsType == 'Linux Swap':
                                        line = line + " swap"
                                elif fsType == 'ext2':
                                        line = line + " "
                                else:
                                        line = line + " " + fsType
                        elif i == 2:
                                size = self.partClist.get_text(n, i)
                                line = line + " --size " + size
                        elif i == 3:
                                grow = self.partClist.get_text(n, i)
                                if grow == 'Yes':
                                        line = line + " --grow"
                                else:
                                        line = line

			buf = buf + "\n" + line
        return buf
