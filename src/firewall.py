## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                      Tammy Fox <tfox@redhat.com>

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

import gtk
import gtk.glade
import gobject
import string
import os
import getopt

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

trustedStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)


class firewall:
    
    def __init__(self, xml, kickstartData):
        self.kickstartData = kickstartData
        self.firewall_frame = xml.get_widget("firewall_frame")
        self.firewall_vbox = xml.get_widget("firewall_vbox")
        self.firewall_label_box = xml.get_widget("firewall_label_box")
        self.securityOptionMenu = xml.get_widget("securityOptionMenu")
        self.firewallDefaultRadio = xml.get_widget("firewallDefaultRadio")
        self.trusted_devices_label = xml.get_widget("trusted_devices_label")
        self.allow_incoming_label = xml.get_widget("allow_incoming_label")
        self.fnnirewall_ports_label = xml.get_widget("firewall_ports_label")
        self.firewall_ports_entry = xml.get_widget("firewall_ports_entry")
        self.customTable = xml.get_widget("customTable")
        self.customFrame = xml.get_widget("customFrame")
        self.upgrade_flag = gtk.FALSE

        self.securityOptionMenu.connect("changed", self.disable_firewall)

        #create table with custom checklists
        self.label1 = gtk.Label (_("Trusted devices:"))
        self.label1.set_alignment (0.0, 0.0)
        self.customTable.attach (self.label1, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 5, 5)
        
        self.trustedView = gtk.TreeView()
        self.trustedView.set_headers_visible(gtk.FALSE)
        self.trustedView.set_model(trustedStore)
        checkbox = gtk.CellRendererToggle()
        checkbox.connect("toggled", self.item_toggled, trustedStore)
        col = gtk.TreeViewColumn('', checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.trustedView.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.trustedView.append_column(col)

        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.trustedView)
        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        viewport.add(sw)
        self.customTable.attach (viewport, 1, 2, 2, 3, gtk.EXPAND|gtk.FILL, gtk.FILL, 5, 5)

        self.label2 = gtk.Label (_("Trusted services:"))
        self.label2.set_alignment (0.0, 0.0)

        self.incomingStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.incomingView = gtk.TreeView()
        self.incomingView.set_headers_visible(gtk.FALSE)        
        self.incomingView.set_model(self.incomingStore)
        checkbox = gtk.CellRendererToggle()
        checkbox.connect("toggled", self.item_toggled, self.incomingStore)
        col = gtk.TreeViewColumn('', checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.incomingView.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.incomingView.append_column(col)

        self.list = {"SSH":"ssh", "Telnet":"telnet", "WWW (HTTP)":"http",
                     "Mail (SMTP)":"smtp", "FTP":"ftp"}

        for item in self.list.keys():
            iter = self.incomingStore.append()
            self.incomingStore.set_value(iter, 0, gtk.FALSE)
            self.incomingStore.set_value(iter, 1, item)

        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        viewport.add(self.incomingView)

        self.customTable.attach (self.label2, 0, 1, 3, 4, gtk.FILL, gtk.FILL, 5, 5)
        self.customTable.attach (viewport, 1, 2, 3, 4, gtk.EXPAND|gtk.FILL, gtk.FILL, 5, 5)

        self.label3 = gtk.Label (_("Other ports: (1029:tcp)"))
        self.label3.set_alignment (0.0, 0.0)
        self.portsEntry = gtk.Entry ()
        self.customTable.attach (self.label3, 0, 1, 4, 5, gtk.FILL, gtk.FILL, 5, 5)
        self.customTable.attach (self.portsEntry, 1, 2, 4, 5, gtk.EXPAND|gtk.FILL, gtk.FILL, 5, 5)

        self.firewall_vbox.show_all()

    def item_toggled(self, data, row, store):
        iter = store.get_iter((int(row),))
        val = store.get_value(iter, 0)
        store.set_value(iter, 0 , not val)

    def disable_firewall (self, widget):
        state = self.securityOptionMenu.get_history()
        
        if state == 0:
            self.customTable.set_sensitive (gtk.TRUE)
        else:
            self.customTable.set_sensitive (gtk.FALSE)

    def toggle_row (self, list, row):
        (val, row_data, header) = list.get_row_data(row)
        val = not val
        list.set_row_data(row, (val, row_data, header))
        list._update_row (row)

    def setSensitive(self, boolean):
        if boolean == gtk.FALSE:
            self.firewall_vbox.hide()
            self.firewall_label_box.show()
            self.upgrade_flag = gtk.TRUE
        else:
            self.firewall_vbox.show()
            self.firewall_label_box.hide()
            self.upgrade_flag = gtk.FALSE

    def getData(self):
        if self.upgrade_flag == gtk.TRUE:
            self.kickstartData.setFirewall(None)
            return

        buf = ""

        if self.securityOptionMenu.get_history() == 0:
            buf = "--enabled "
        elif self.securityOptionMenu.get_history() == 1:
            buf = "--disabled "

        iter = trustedStore.get_iter_first()

        while iter:
            if trustedStore.get_value(iter, 0) == gtk.TRUE:
                buf = buf + "--trust=" + trustedStore.get_value(iter, 1) + " "
            iter = trustedStore.iter_next(iter)


        iter = self.incomingStore.get_iter_first()

        while iter:
            if self.incomingStore.get_value(iter, 0) == gtk.TRUE:
                service = self.list[self.incomingStore.get_value(iter, 1)]
                buf = buf + "--" + service + " "
            iter = self.incomingStore.iter_next(iter)

        portlist = self.portsEntry.get_text()
        ports = []

        if portlist != "":
            buf = buf + '--port=' + portlist
            
        self.kickstartData.setFirewall([buf])
        
    def fillData(self):
        if self.kickstartData.getFirewall():
            opts, args = getopt.getopt(self.kickstartData.getFirewall(), "d:h", ["high", "medium", "enabled",
                                       "disabled", "trust=", "port=", "dhcp", "ssh", "telnet",
                                       "smtp", "http", "ftp"])

            for opt, value in opts:
                if opt == "--high":
                    self.securityOptionMenu.set_history(0)

                if opt == "--medium":
                    self.securityOptionMenu.set_history(0)

                if opt == "--enabled":
                    self.securityOptionMenu.set_history(0)

                if opt == "--disabled":
                    self.securityOptionMenu.set_history(1)

                if opt=="--dhcp" or opt=="--ssh" or opt=="--telnet" or opt=="--smtp" or opt=="--http" or opt=="--ftp":
                    iter = self.incomingStore.get_iter_first()

                    while iter:
                        service = self.list[self.incomingStore.get_value(iter, 1)]
                        if service == opt[2:]:
                            self.incomingStore.set_value(iter, 0, gtk.TRUE)
                        iter = self.incomingStore.iter_next(iter)

                if opt == "--trust":
                    iter = trustedStore.get_iter_first()

                    while iter:
                        device = trustedStore.get_value(iter, 1) 
                        if device == value:
                            trustedStore.set_value(iter, 0, gtk.TRUE)
                        iter = trustedStore.iter_next(iter)

                if opt == "--port":
                    current = self.portsEntry.get_text()
                    self.portsEntry.set_text(value)
