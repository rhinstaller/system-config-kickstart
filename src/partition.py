#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002 Brent Fox <bfox@redhat.com>
##                                Tammy Fox <tfox@redhat.com>

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

import gtk
import gtk.glade
import gobject
import partWindow
#import raidWindow

##
## I18N
##
import gettext
gettext.bindtextdomain ("ksconfig", "/usr/share/locale")
gettext.textdomain ("ksconfig")
_=gettext.gettext

class partition:
    def __init__(self, xml):
        self.xml = xml
        self.num_rows = 0
        self.clear_mbr_yes_radiobutton = self.xml.get_widget("clear_mbr_yes_radiobutton")
        self.clear_mbr_no_radiobutton = self.xml.get_widget("clear_mbr_no_radiobutton")
        self.remove_parts_none_radiobutton = self.xml.get_widget("remove_parts_none_radiobutton")
        self.remove_parts_all_radiobutton = self.xml.get_widget("remove_parts_all_radiobutton")
        self.remove_parts_Linux_radiobutton = self.xml.get_widget("remove_parts_Linux_radiobutton")
        self.initlabel_yes_radiobutton = self.xml.get_widget("initlabel_yes_radiobutton")
        self.initlabel_no_radiobutton = self.xml.get_widget("initlabel_no_radiobutton")        
        self.part_view = self.xml.get_widget("part_view")
        self.add_part_button = self.xml.get_widget("add_part_button")
        self.edit_part_button = self.xml.get_widget("edit_part_button")
        self.del_part_button = self.xml.get_widget("del_part_button")
#        self.raid_part_button = self.xml.get_widget("raid_part_button")
#        self.partitionDialog = self.xml.get_widget("partition_dialog")
        self.checkbox = self.xml.get_widget("checkbox2")

        self.add_part_button.connect("clicked", self.addPartition)
        self.edit_part_button.connect("clicked", self.editPartition)
        self.del_part_button.connect("clicked", self.delPartition)

#         (mountPoint, fsType, size, fixedSize, setSize,
#             setSizeVal, maxSize, asPrimary, 
#             onDisk, onDiskVal, onPart, onPartVal,
#             doFormat, raidType, raidSpares, isRaidDevice)

        self.part_store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING)

        self.part_view.set_model(self.part_store)
        col = gtk.TreeViewColumn(_("Mount Point"), gtk.CellRendererText(), text=0)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Filesystem Type"), gtk.CellRendererText(), text=1)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Size"), gtk.CellRendererText(), text=2)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Device"), gtk.CellRendererText(), text=9)
        self.part_view.append_column(col)

        #temp until edit partitions finished
        self.partWindow = partWindow.partWindow(self.xml, self.part_store, self.part_view)
#        self.raidWindow = raidWindow.raidWindow(self.xml, self.part_view)



#        self.xml.signal_autoconnect (
#            { "select_clist" : self.select_clist,
#              "unselect_clist" : self.unselect_clist,
#              "addPartition" : self.addPartition,
#              "editPartition" : self.editPartition,
#              "delPartition" : self.delPartition,
#              "raidPartition" : self.raidPartition, 
#              })

#    def select_clist(self, r, c, event):
    def select_clist(self, *args ):
        widget, r, c, event = args
        self.selected_row = r
        self.edit_part_button.set_sensitive(gtk.TRUE)
        self.del_part_button.set_sensitive(gtk.TRUE)

    def delPartition(self, *args):
        self.num_rows = self.num_rows - 1
        self.partClist.remove(self.selected_row)
        self.edit_part_button.set_state(STATE_INSENSITIVE)
        self.del_part_button.set_state(STATE_INSENSITIVE)

    def addPartition(self, *args):
        self.num_rows = self.num_rows + 1
        self.partWindow.add_partition()
        self.edit_part_button.set_sensitive(gtk.TRUE)
        self.del_part_button.set_sensitive(gtk.TRUE)
#        self.raid_part_button.set_sensitive(gtk.TRUE)
#        self.partClist.unselect_all()
        self.part_view.get_selection().unselect_all()

    def editPartition(self, *args):
        rowData = self.partClist.get_row_data(self.selected_row)
        self.partWindow.edit_partition(rowData, self.selected_row)

#    def raidPartition(self, *args):
#        self.raidWindow.add_raid(self.num_rows)

    def getData(self):
        data = []
        data.append("")

        #zerombr and clearpart options
        if self.clear_mbr_yes_radiobutton.get_active():
            data.append("#Clear the Master Boot Record")
            data.append("zerombr yes")
        elif self.clear_mbr_no_radiobutton.get_active():
            pass
        if self.remove_parts_none_radiobutton.get_active():
            pass
        else:
            buf = "clearpart "
            data.append("")
            if self.remove_parts_all_radiobutton.get_active():
                data.append("#Clear all partitions from the disk")
                buf = buf + "--all "
            elif self.remove_parts_Linux_radiobutton.get_active():
                data.append("#Clear only Linux partitions from the disk")
                buf = buf + "--linux "
            if self.initlabel_yes_radiobutton.get_active():
                buf = buf + "--initlabel "
            elif self.initlabel_no_radiobutton.get_active():
                pass
            data.append(buf)

        data.append("")
        data.append("#Disk partitioning information")

        #partitioning table options
#        num_raid = 0
        for row in range(self.num_rows):
            rowData = self.partClist.get_row_data(row)
            (mountPoint, fsType, size, fixedSize, setSize,
             setSizeVal, maxSize, asPrimary, 
             onDisk, onDiskVal, onPart, onPartVal,
             doFormat, raidType, raidSpares, isRaidDevice) = rowData

##             if fsType == "RAID":
##                 num_raid = num_raid + 1
##                 if num_raid < 10:
##                     buf = buf + "\n" + "part raid.%d%d " %(0, num_raid)
##                 else:
##                     buf = buf + "\n" + "part raid.%d " %(num_raid)
##             else:
##                 buf = buf + "\n" + "part %s " % (mountPoint)
##                 buf = buf + "--fstype " + fsType + " " 

            buf = "part %s " % (mountPoint)

            if fsType == "swap":
                buf = buf + "swap "
            else:
                buf = buf + "--fstype " + fsType + " " 

            buf = buf + "--size %s " % (size)

            if setSize:
                buf = buf + "--grow --maxsize %s " % (setSizeVal)
            elif maxSize:
                buf = buf + "--grow "

            if asPrimary:
                buf = buf + "--asprimary "

#            if asPrimaryNum:
#                buf = buf + "--onprimary %s " % (asPrimaryVal)

            if onDisk:
                buf = buf + "--ondisk %s " % (onDiskVal)

            if onPart:
                buf = buf + "--onpart %s " % (onPartVal)

            if not doFormat:
                buf = buf + "--noformat "

            data.append(buf)

        return data
