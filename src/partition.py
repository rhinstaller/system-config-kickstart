#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2008 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2 or, at your option, any later version.  This
# program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 

import gtk
import gtk.glade
import gobject
import string

import partWindow
import raidOptionsWindow
import raidWindow
import partEntry
import kickstartGui
from pykickstart.constants import *

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

class partition:
    def __init__(self, xml, ksHandler):
        self.xml = xml
        self.ks = ksHandler
        self.partition_vbox = self.xml.get_widget("partition_vbox")
        self.partition_label_box = self.xml.get_widget("partition_label_box")
        self.clear_mbr_yes_radiobutton = self.xml.get_widget("clear_mbr_yes_radiobutton")
        self.clear_mbr_no_radiobutton = self.xml.get_widget("clear_mbr_no_radiobutton")
        self.remove_parts_none_radiobutton = self.xml.get_widget("remove_parts_none_radiobutton")
        self.remove_parts_all_radiobutton = self.xml.get_widget("remove_parts_all_radiobutton")
        self.remove_parts_linux_radiobutton = self.xml.get_widget("remove_parts_linux_radiobutton")
        self.initlabel_yes_radiobutton = self.xml.get_widget("initlabel_yes_radiobutton")
        self.initlabel_no_radiobutton = self.xml.get_widget("initlabel_no_radiobutton")
        self.part_view = self.xml.get_widget("part_view")
        self.add_part_button = self.xml.get_widget("add_part_button")
        self.edit_part_button = self.xml.get_widget("edit_part_button")
        self.del_part_button = self.xml.get_widget("del_part_button")
        self.raid_part_button = self.xml.get_widget("raid_part_button")
        self.checkbox = self.xml.get_widget("checkbox2")

        self.remove_parts_none_radiobutton.connect("toggled", self.noneToggled)
        self.add_part_button.connect("clicked", self.addPartition)
        self.edit_part_button.connect("clicked", self.editPartition)
        self.del_part_button.connect("clicked", self.delPartition)
        self.raid_part_button.connect("clicked", self.raidPartition)

        self.part_store = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_STRING,
                                        gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        self.part_view.set_model(self.part_store)
        col = gtk.TreeViewColumn(_("Device/\nPartition Number"), gtk.CellRendererText(), text=0)
        self.part_view.append_column(col)
        col = gtk.TreeViewColumn(_("Mount Point/\nRAID"), gtk.CellRendererText(), text=1)
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
        self.raidWindow = raidWindow.raidWindow(self.xml, self.part_store, self.part_view)
        self.raidOptionsWindow = raidOptionsWindow.raidOptionsWindow(self.xml, self.part_store, self.part_view, self.partWindow, self.raidWindow)

        self.part_view.expand_all()

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def delPartition(self, *args):
        data, iter = self.part_view.get_selection().get_selected()
        if iter == None:
            self.deviceNotValid(_("Please select a partition from the list."))

        parent = self.part_store.iter_parent(iter)
        if parent:
            if self.part_store.iter_n_children(parent) == 1:
                 # Grab the key if the device we're deleting in the
                 # iter_dict so we can remove it later.
                 dev_name = data.get_value(iter, 5).device

                 # If the item is the only one in the list, remove it and
                 # the parent.
                 grandparent = self.part_store.iter_parent(parent)
                 self.part_store.remove(iter)
                 self.part_store.remove(parent)

                 # Delete the iter from the dict so that if we go to add
                 # more partitions later, we won't reference a bad iter
                 # and explode.
                 if self.partWindow.device_iter_dict.has_key(dev_name):
                     del(self.partWindow.device_iter_dict[dev_name])

                 if grandparent:
                     if self.part_store.iter_n_children(grandparent) == 0:
                         self.part_store.remove(grandparent)

            else:
                # If there are other items in that branch, only remove the
                # selected item
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

        part_object = self.part_store.get_value(iter, 5)

        if part_object.isRaidDevice:
            self.raidWindow.editDevice(iter, part_object)
        else:
            self.partWindow.edit_partition(iter)

        self.part_view.get_selection().unselect_all()

    def raidPartition(self, *args):
        self.raidOptionsWindow.showOptionsWindow()

    def formToKickstart(self):
        # Reset lists to empty.
        self.ks.partition(partitions=[])
        self.ks.raid(raidList=[])
        self.ks.logvol(lvList=[])
        self.ks.volgroup(vgList=[])

        # zerombr and clearpart options
        self.ks.zerombr(zerombr=self.clear_mbr_yes_radiobutton.get_active())

        if self.remove_parts_none_radiobutton.get_active():
            # We want to preserve all partitions, so don't write the
            # clearpart line
            self.ks.clearpart.drives = []
            self.ks.clearpart.type = CLEARPART_TYPE_NONE
            pass
        else:
            if self.remove_parts_all_radiobutton.get_active():
                self.ks.clearpart.type = CLEARPART_TYPE_ALL
            elif self.remove_parts_linux_radiobutton.get_active():
                self.ks.clearpart.type = CLEARPART_TYPE_LINUX

            if self.initlabel_yes_radiobutton.get_active():
                self.ks.clearpart.initAll = True
            elif self.initlabel_no_radiobutton.get_active():
                self.ks.clearpart.initAll = False

        self.partDataBuf = []
        self.part_store.foreach(self.getPartData)

        return None

    def getPartData(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)

        if part_object:
            if part_object.isRaidDevice == None:
                pd = self.ks.PartData()
                pd.mountpoint = part_object.mountPoint
                pd.fstype = part_object.fsType

                if part_object.size == "recommended":
                    pd.recommended = True
                else:
                    pd.size = int(part_object.size)

                if part_object.sizeStrategy == "grow":
                    pd.grow = True
                    pd.maxSizeMB = int(part_object.setSizeVal)
                elif part_object.sizeStrategy == "max":
                    pd.grow = True

                if part_object.asPrimary:
                    pd.primOnly = True

                if part_object.partition:
                    pd.onPart = part_object.partition
                elif part_object.device:
                    pd.disk = part_object.device

                if not part_object.doFormat:
                    pd.format = False

                self.ks.partition.dataList().append(pd)
            else:
                #This is a raid device
                rd = self.ks.RaidData()
                rd.mountpoint = part_object.mountPoint

                if part_object.raidLevel:
                    rd.level = part_object.raidLevel

                if part_object.raidDevice:
                    rd.device = part_object.raidDevice

                if part_object.fsType:
                    rd.fstype = part_object.fsType

                if not part_object.doFormat:
                    rd.format = False

                if part_object.raidPartitions != None:
                    rd.members = part_object.raidPartitions

                self.ks.raid.dataList().append(rd)

    def rowSelected(self, *args):
        store, iter = self.part_view.get_selection().get_selected()
        if iter == None:
            self.edit_part_button.set_sensitive(False)
            self.del_part_button.set_sensitive(False)
        else:
            part_object = self.part_store.get_value(iter, 5)
            # Check to see if the selection is actually a partition or
            # one of the parent roots
            if part_object == None:
                self.edit_part_button.set_sensitive(False)
                self.del_part_button.set_sensitive(False)
            else:
                self.edit_part_button.set_sensitive(True)
                self.del_part_button.set_sensitive(True)

    def deviceNotValid(self, label):
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, label)
        dlg.set_title(_("Error"))
        dlg.set_default_size(100, 100)
        dlg.set_position (gtk.WIN_POS_CENTER)
        dlg.set_border_width(2)
        dlg.set_modal(True)
        toplevel = self.xml.get_widget("main_window")
        dlg.set_transient_for(toplevel)
        dlg.set_icon(kickstartGui.iconPixbuf)
        rc = dlg.run()
        if rc == gtk.RESPONSE_OK:
            dlg.hide()
        return None

    def noneToggled(self, button):
        self.initlabel_yes_radiobutton.set_sensitive(not button.get_active())
        self.initlabel_no_radiobutton.set_sensitive(not button.get_active())

    def setSensitive(self, boolean):
        if boolean == False:
            self.partition_vbox.hide()
            self.partition_label_box.show_all()
        else:
            self.partition_vbox.show_all()
            self.partition_label_box.hide()

    def applyKickstart(self):
        if self.ks.zerombr.zerombr:
            self.clear_mbr_yes_radiobutton.set_active(True)
        else:
            self.clear_mbr_no_radiobutton.set_active(True)

        if self.ks.clearpart.type != CLEARPART_TYPE_NONE:
            if self.ks.clearpart.type == CLEARPART_TYPE_ALL:
                self.remove_parts_all_radiobutton.set_active(True)
            elif self.ks.clearpart.type == CLEARPART_TYPE_LINUX:
                self.remove_parts_linux_radiobutton.set_active(True)
            if self.ks.clearpart.initAll == True:
                self.initlabel_yes_radiobutton.set_active(True)
            else:
                self.initlabel_no_radiobutton.set_active(True)

        else:
            self.remove_parts_none_radiobutton.set_active(True)

        for part in self.ks.partition.partitions:
             self.partWindow.populateList(part)

        for part in self.ks.raid.raidList:
            self.raidWindow.populateRaid(part)
