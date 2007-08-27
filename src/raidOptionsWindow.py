#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2007 Red Hat, Inc.
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

import string
import gtk
import signal
import partWindow
#import raidWindow
import kickstartGui

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class raidOptionsWindow:
    def __init__(self, xml, part_store, part_view, partWindow, raidWindow):
        self.xml = xml
        self.part_store = part_store
        self.part_view = part_view
        self.partWindow = partWindow
        self.raidWindow = raidWindow

        self.raid_options_window = xml.get_widget("raid_options_window")
        self.raid_options_window.connect("delete-event", self.destroy)
        toplevel = self.xml.get_widget("main_window")
        self.raid_options_window.set_transient_for(toplevel)
        self.raid_options_window.set_icon(kickstartGui.iconPixbuf)

        self.raid_partition_radio = xml.get_widget("raid_partition_radio")
        self.raid_device_radio = xml.get_widget("raid_device_radio")
        self.raid_options_ok_button = xml.get_widget("raid_options_ok_button")
        self.raid_options_cancel_button = xml.get_widget("raid_options_cancel_button")
        self.message_label = xml.get_widget("message_label")
        self.raid_partition_radio.set_active(True)

#        self.raidWindow = raidWindow.raidWindow(self.xml, self.part_store, self.part_view)

        self.raid_options_ok_button.connect("clicked", self.okClicked)
        self.raid_options_cancel_button.connect("clicked", self.destroy)

    def showOptionsWindow(self):
        self.countRaidPartitions()
        self.raid_options_window.show_all()

    def countRaidPartitions(self):
        self.list = []

        self.part_store.foreach(self.walkStore)

        num = len(self.list)
        self.message_label.set_text(_("You currently have %d software RAID partition(s) "
                                      "free to use.") % num)
        if num > 1:
            self.raid_device_radio.set_active(True)
            self.raid_device_radio.set_sensitive(True)
        else:
            self.raid_partition_radio.set_active(True)
            self.raid_device_radio.set_sensitive(False)

    def walkStore(self, store, data, iter):
        part_object = self.part_store.get_value(iter, 5)
        if part_object and part_object.raidNumber:
            self.list.append(part_object.raidNumber)

    def okClicked(self, *args):
        if self.raid_partition_radio.get_active() == True:
            self.partWindow.add_partition("TYPE_RAID")
        else:
            self.raidWindow.addPartition()

        self.raid_options_window.hide()

    def destroy(self, *args):
        self.raid_options_window.hide()
        return True
