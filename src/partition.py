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
import string

import partWindow
import raidOptionsWindow
import partEntry

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
        self.raid_part_button = self.xml.get_widget("raid_part_button")
        self.lvm_part_button = self.xml.get_widget("lvm_part_button")
        self.checkbox = self.xml.get_widget("checkbox2")

        self.add_part_button.connect("clicked", self.addPartition)
        self.edit_part_button.connect("clicked", self.editPartition)
        self.del_part_button.connect("clicked", self.delPartition)
        self.raid_part_button.connect("clicked", self.raidPartition)
        self.lvm_part_button.connect("clicked", self.lvmPartition)

        self.part_store = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        self.part_view.set_model(self.part_store)
        col = gtk.TreeViewColumn(_("Device/\nPartition Number"), gtk.CellRendererText(), text=0)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Mount Point/\nRAID/Volume"), gtk.CellRendererText(), text=1)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Type"), gtk.CellRendererText(), text=2)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Format"), gtk.CellRendererText(), text=3)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Size (MB)"), gtk.CellRendererText(), text=4)
        self.part_view.append_column(col)

        self.part_view.get_selection().connect("changed", self.rowSelected)

        #initialize the child classes
        self.partWindow = partWindow.partWindow(self.xml, self.part_store, self.part_view)
        self.raidOptionsWindow = raidOptionsWindow.raidOptionsWindow(self.xml, self.part_store, self.part_view, self.partWindow)


##         #XXX-FIXME-FOR TESTING ONLY
##         hard_drive_parent_iter = self.part_store.append(None)
##         self.part_store.set_value(hard_drive_parent_iter, 0, (_("Hard Drives")))

##         hda_iter = self.part_store.append(hard_drive_parent_iter)
##         self.part_store.set_value(hda_iter, 0, (_("hda")))

##         part_object = partEntry.partEntry()
##         part_object.fsType = "raid"
##         part_object.device = "Auto"
##         part_object.raidNumber = "raid.01"
##         part_object.format = 1
##         part_object.size = 1

##         part_iter = self.part_store.append(hda_iter)
##         self.part_store.set_value(part_iter, 0, part_object.raidNumber)
##         self.part_store.set_value(part_iter, 2, part_object.fsType)
##         self.part_store.set_value(part_iter, 3, part_object.format)
##         self.part_store.set_value(part_iter, 4, part_object.size)
##         self.part_store.set_value(part_iter, 5, part_object)

##         hdb_iter = self.part_store.append(hard_drive_parent_iter)
##         self.part_store.set_value(hdb_iter, 0, (_("hdb")))

##         part_object = partEntry.partEntry()
##         part_object.fsType = "raid"
##         part_object.device = "Auto"
##         part_object.format = 1
##         part_object.raidNumber = "raid.02"
##         part_object.size = 1

##         part_iter = self.part_store.append(hdb_iter)
##         self.part_store.set_value(part_iter, 0, part_object.raidNumber)
##         self.part_store.set_value(part_iter, 2, part_object.fsType)
##         self.part_store.set_value(part_iter, 3, part_object.format)
##         self.part_store.set_value(part_iter, 4, part_object.size)
##         self.part_store.set_value(part_iter, 5, part_object)

        self.part_view.expand_all()

    def delPartition(self, *args):
        try:
            data, iter = self.part_view.get_selection().get_selected()
        except:
            self.deviceNotValid(_("Please select a partition from the list."))

        self.part_store.remove(iter)
        self.part_view.get_selection().unselect_all()

    def addPartition(self, *args):
        self.partWindow.add_partition()
        self.part_view.get_selection().unselect_all()

    def editPartition(self, *args):
        try:
            data, iter = self.part_view.get_selection().get_selected()
        except:
            self.deviceNotValid(_("Please select a partition from the list."))

        self.partWindow.edit_partition(iter)
        self.part_view.get_selection().unselect_all()

    def raidPartition(self, *args):
        self.raidOptionsWindow.showOptionsWindow()

    def lvmPartition(self, *args):
        pass

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

        self.partDataBuf = []
        self.part_store.foreach(self.getPartData)

        data = data + self.partDataBuf
        
        return data

    def getPartData(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)

        if part_object:

            if part_object.isRaidDevice == None:
                buf = "part %s" % (part_object.mountPoint)
                
                if part_object.fsType == "swap":
                    buf = buf + "swap "
                elif part_object.fsType == "raid":
                    buf = buf + "raid.%s " % part_object.raidNumber
                else:
                    buf = buf + " --fstype " + part_object.fsType + " " 

                if part_object.size == "recommended":
                    buf = buf + "--recommended "
                else:
                    buf = buf + "--size %s " % (part_object.size)

                if part_object.sizeStrategy == "grow":
                    buf = buf + "--grow --maxsize %s " % (part_object.setSizeVal)
                elif part_object.sizeStrategy == "max":
                    buf = buf + "--grow "

                if part_object.asPrimary:
                    buf = buf + "--asprimary "

                if part_object.partition:
                    buf = buf + "--onpart %s " % (part_object.partition)

                elif part_object.device:
                    buf = buf + "--ondisk %s " % (part_object.device)

                if not part_object.doFormat:
                    buf = buf + "--noformat "

            else:
                #This is a raid device
                buf = "raid %s" % (part_object.mountPoint)

                if part_object.raidLevel:
                    buf = buf + " --level=%s" % part_object.raidLevel + " "

                if part_object.raidDevice:
                    buf = buf + " --device=%s" % part_object.raidDevice + " "

                if part_object.fsType:
                    buf = buf + " --fstype " + part_object.fsType + " " 

                if part_object.raidPartitions != None:
                    print part_object.raidPartitions
                    partitions = string.join(part_object.raidPartitions, " ")
                    buf = buf + partitions + " "

            self.partDataBuf.append(buf)
            
    def rowSelected(self, *args):
        store, selection = self.part_view.get_selection().get_selected()
        if selection == None:
            self.edit_part_button.set_sensitive(gtk.FALSE)
            self.del_part_button.set_sensitive(gtk.FALSE)
        else:
            self.edit_part_button.set_sensitive(gtk.TRUE)
            self.del_part_button.set_sensitive(gtk.TRUE)

    def deviceNotValid(self, label):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, label)
        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER)
        dlg.set_border_width(2)
        dlg.set_modal(gtk.TRUE)
        rc = dlg.run()
        if rc == gtk.RESPONSE_OK:
            dlg.hide()
        return None
