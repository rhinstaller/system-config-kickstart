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
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class partition:
    def __init__(self, xml):
        self.xml = xml
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

        self.part_store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)


        self.part_view.set_model(self.part_store)
        col = gtk.TreeViewColumn(_("Mount Point"), gtk.CellRendererText(), text=0)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("File System Type"), gtk.CellRendererText(), text=1)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Size"), gtk.CellRendererText(), text=2)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Device"), gtk.CellRendererText(), text=3)
        self.part_view.append_column(col)

        #initialize the child classes
        self.partWindow = partWindow.partWindow(self.xml, self.part_store, self.part_view)
#        self.raidWindow = raidWindow.raidWindow(self.xml, self.part_view)


    def delPartition(self, *args):
        try:
            data, iter = self.part_view.get_selection().get_selected()
        except:
            selectDialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, _("Please select a partition from the list."))
            selectDialog.set_title(_("Message"))
            selectDialog.set_default_size(100, 100)
            selectDialog.set_position (gtk.WIN_POS_CENTER)
            selectDialog.set_border_width(2)
            selectDialog.set_modal(gtk.TRUE)
            rc = selectDialog.run()
            if rc == gtk.RESPONSE_OK:
                selectDialog.hide()
            return
        self.part_store.remove(iter)
        self.edit_part_button.set_sensitive(gtk.FALSE)
        self.del_part_button.set_sensitive(gtk.FALSE)

    def addPartition(self, *args):
        self.partWindow.add_partition()
        self.edit_part_button.set_sensitive(gtk.TRUE)
        self.del_part_button.set_sensitive(gtk.TRUE)
#        self.raid_part_button.set_sensitive(gtk.TRUE)
        self.part_view.get_selection().unselect_all()

    def editPartition(self, *args):
        try:
            data, iter = self.part_view.get_selection().get_selected()
        except:
            selectDialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, _("Please select a partition from the list."))
            selectDialog.set_title(_("Message"))
            selectDialog.set_default_size(100, 100)
            selectDialog.set_position (gtk.WIN_POS_CENTER)
            selectDialog.set_border_width(2)
            selectDialog.set_modal(gtk.TRUE)
            rc = selectDialog.run()
            if rc == gtk.RESPONSE_OK:
                selectDialog.hide()
            return
            
        self.partWindow.edit_partition(iter)

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

        iter = self.part_store.get_iter_first()

        while iter:
            part_object = self.part_store.get_value(iter, 4)

##             if fsType == "RAID":
##                 num_raid = num_raid + 1
##                 if num_raid < 10:
##                     buf = buf + "\n" + "part raid.%d%d " %(0, num_raid)
##                 else:
##                     buf = buf + "\n" + "part raid.%d " %(num_raid)
##             else:
##                 buf = buf + "\n" + "part %s " % (mountPoint)
##                 buf = buf + "--fstype " + fsType + " " 

            buf = "part %s " % (part_object.mountPoint)

            if part_object.fsType == "swap":
                buf = buf + "swap "
            else:
                buf = buf + "--fstype " + part_object.fsType + " " 
                
            if part_object.size == "recommended":
                buf = buf + "--recommended"
            else:
                buf = buf + "--size %s " % (part_object.size)

            if part_object.sizeStrategy == "grow":
                buf = buf + "--grow --maxsize %s " % (part_object.setSizeVal)
            elif part_object.sizeStrategy == "max":
                buf = buf + "--grow "

            if part_object.asPrimary:
                buf = buf + "--asprimary "

#            if asPrimaryNum:
#                buf = buf + "--onprimary %s " % (asPrimaryVal)

            if part_object.onDisk:
                buf = buf + "--ondisk %s " % (part_object.onDiskVal)

            if part_object.onPart:
                buf = buf + "--onpart %s " % (part_object.onPartVal)

            if not part_object.doFormat:
                buf = buf + "--noformat "

            data.append(buf)
            iter = self.part_store.iter_next(iter)

        return data
