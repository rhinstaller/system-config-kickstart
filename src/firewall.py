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
import os
import getopt
from pykickstart.constants import *

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

trustedStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)

class Firewall:
    def __init__(self, xml, ksHandler):
        self.ks = ksHandler
        self.firewall_frame = xml.get_widget("firewall_frame")
        self.firewall_vbox = xml.get_widget("firewall_vbox")
        self.firewall_label_box = xml.get_widget("firewall_label_box")
        self.securityOptionMenu = xml.get_widget("securityOptionMenu")
        self.selinuxOptionMenu = xml.get_widget("selinuxOptionMenu")
        self.selinuxOptionMenu.set_active(0)
        self.firewallDefaultRadio = xml.get_widget("firewallDefaultRadio")
        self.trusted_devices_label = xml.get_widget("trusted_devices_label")
        self.allow_incoming_label = xml.get_widget("allow_incoming_label")
        self.fnnirewall_ports_label = xml.get_widget("firewall_ports_label")
        self.firewall_ports_entry = xml.get_widget("firewall_ports_entry")
        self.customTable = xml.get_widget("customTable")
        self.customFrame = xml.get_widget("customFrame")

        self.securityOptionMenu.connect("changed", self.disable_firewall)
        self.securityOptionMenu.set_active(0)

        self.label2 = gtk.Label (_("Trusted services:"))
        self.label2.set_alignment (0.0, 0.0)

        self.incomingStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.incomingView = gtk.TreeView()
        self.incomingView.set_headers_visible(False)
        self.incomingView.set_model(self.incomingStore)
        checkbox = gtk.CellRendererToggle()
        checkbox.connect("toggled", self.item_toggled, self.incomingStore)
        col = gtk.TreeViewColumn('', checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(True)
        self.incomingView.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.incomingView.append_column(col)

        self.list = {"SSH":"ssh", "Telnet":"telnet", "WWW (HTTP)":"http",
                     "Mail (SMTP)":"smtp", "FTP":"ftp"}

        for item in self.list.keys():
            iter = self.incomingStore.append()
            self.incomingStore.set_value(iter, 0, False)
            self.incomingStore.set_value(iter, 1, item)

        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        viewport.add(self.incomingView)

        self.customTable.attach (self.label2, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
        self.customTable.attach (viewport, 1, 2, 0, 1, gtk.EXPAND|gtk.FILL, gtk.FILL)

        self.label3 = gtk.Label (_("Other ports (1029:tcp):"))
        self.label3.set_alignment (0.0, 0.5)
        self.portsEntry = gtk.Entry ()
        self.customTable.attach (self.label3, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
        self.customTable.attach (self.portsEntry, 1, 2, 2, 3, gtk.EXPAND|gtk.FILL, gtk.FILL)

        self.firewall_vbox.show_all()

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def item_toggled(self, data, row, store):
        iter = store.get_iter((int(row),))
        val = store.get_value(iter, 0)
        store.set_value(iter, 0 , not val)

    def disable_firewall (self, widget):
        state = self.securityOptionMenu.get_active()

        if state == 0:
            self.customTable.set_sensitive (True)
        else:
            self.customTable.set_sensitive (False)

    def toggle_row (self, list, row):
        (val, row_data, header) = list.get_row_data(row)
        val = not val
        list.set_row_data(row, (val, row_data, header))
        list._update_row (row)

    def setSensitive(self, boolean):
        if boolean == False:
            self.firewall_vbox.hide()
            self.firewall_label_box.show()
        else:
            self.firewall_vbox.show()
            self.firewall_label_box.hide()

    def formToKickstart(self):
        if self.ks.upgrade.upgrade == True:
            return

        self.ks.firewall(trusts=[], ports=[],
                         enabled=self.securityOptionMenu.get_active() == 0)

        iter = self.incomingStore.get_iter_first()

        while iter:
            if self.incomingStore.get_value(iter, 0) == True:
                service = self.list[self.incomingStore.get_value(iter, 1)]
                self.ks.firewall.ports.append(service)
            iter = self.incomingStore.iter_next(iter)

        self.ks.firewall.ports.extend(string.split(self.portsEntry.get_text()))

        if self.selinuxOptionMenu.get_active() == 0:
            self.ks.selinux(selinux=SELINUX_ENFORCING)
        elif self.selinuxOptionMenu.get_active() == 1:
            self.ks.selinux(selinux=SELINUX_PERMISSIVE)
        elif self.selinuxOptionMenu.get_active() == 2:
            self.ks.selinux(selinux=SELINUX_DISABLED)

    def applyKickstart(self):
        if self.ks.firewall.enabled == True:
            self.securityOptionMenu.set_active(0)
        else:
            self.securityOptionMenu.set_active(1)

        iter = self.incomingStore.get_iter_first()

        filteredPorts = self.ks.firewall.ports

        while iter:
            service = self.list[self.incomingStore.get_value(iter, 1)]

            if service == "ssh" and "22:tcp" in filteredPorts:
                self.incomingStore.set_value(iter, 0, True)
                filteredPorts.remove("22:tcp")
            elif service == "telnet" and "23:tcp" in filteredPorts:
                self.incomingStore.set_value(iter, 0, True)
                filteredPorts.remove("23:tcp")
            elif service == "http" and "80:tcp" in filteredPorts:
                self.incomingStore.set_value(iter, 0, True)
                filteredPorts.remove("80:tcp")
                filteredPorts.remove("443:tcp")
            elif service == "smtp" and "25:tcp" in filteredPorts:
                self.incomingStore.set_value(iter, 0, True)
                filteredPorts.remove("25:tcp")
            elif service == "ftp" and "21:tcp" in filteredPorts:
                self.incomingStore.set_value(iter, 0, True)
                filteredPorts.remove("21:tcp")

            iter = self.incomingStore.iter_next(iter)

        if len(self.ks.firewall.ports) > 0:
            self.portsEntry.set_text(string.join(filteredPorts, ","))

        if self.ks.selinux.selinux == SELINUX_DISABLED:
            self.selinuxOptionMenu.set_active(2)
        elif self.ks.selinux.selinux == SELINUX_ENFORCING:
            self.selinuxOptionMenu.set_active(0)
        elif self.ks.selinux.selinux == SELINUX_PERMISSIVE:
            self.selinuxOptionMenu.set_active(1)
