#!/usr/bin/python2.2

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002 Red Hat, Inc.
## Copyright (C) 2000, 200, 20021 Brent Fox <bfox@redhat.com>
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

#Kickstart Configurator Firewall Configuration

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
domain = 'redhat-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class firewall:
    
    def __init__(self, xml, kickstartData):
        self.kickstartData = kickstartData
        self.securityHighRadio = xml.get_widget("securityHighRadio")
        self.securityMediumRadio = xml.get_widget("securityMediumRadio")
        self.securityNoneRadio = xml.get_widget("securityNoneRadio")
        self.firewallDefaultRadio = xml.get_widget("firewallDefaultRadio")
        self.firewallCustomizeRadio = xml.get_widget("firewallCustomizeRadio")        
        self.trusted_devices_label = xml.get_widget("trusted_devices_label")
        self.allow_incoming_label = xml.get_widget("allow_incoming_label")
        self.fnnirewall_ports_label = xml.get_widget("firewall_ports_label")
        self.firewall_ports_entry = xml.get_widget("firewall_ports_entry")
        self.customTable = xml.get_widget("customTable")
        self.customFrame = xml.get_widget("customFrame")
        self.customizeRadio = xml.get_widget("firewallCustomizeRadio")

        self.securityNoneRadio.connect("toggled", self.disable_firewall)
        self.customizeRadio.connect("toggled", self.enable_custom)

        #create table with custom checklists
        self.label1 = gtk.Label (_("Trusted devices:"))
        self.label1.set_alignment (0.0, 0.0)
        self.customTable.attach (self.label1, 0, 1, 2, 3, gtk.FILL, gtk.FILL, 5, 5)
        
        if os.access("/proc/net/dev", os.R_OK):
            f = open ("/proc/net/dev")
            lines = f.readlines()
            f.close ()
            
        # skip first two lines, they are header
        self.netdevices = []
        try:
            lines = lines[2:]
            for line in lines:
                dev = string.strip (line[0:6])
                if dev != "lo":
                    self.netdevices.append(dev)
        except:
            pass

        self.trustedStore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.trustedView = gtk.TreeView()
        self.trustedView.set_headers_visible(gtk.FALSE)
        self.trustedView.set_model(self.trustedStore)
        checkbox = gtk.CellRendererToggle()
        checkbox.connect("toggled", self.item_toggled, self.trustedStore)
        col = gtk.TreeViewColumn('', checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.trustedView.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.trustedView.append_column(col)

        for device in self.netdevices:
            iter = self.trustedStore.append()
            self.trustedStore.set_value(iter, 0, gtk.FALSE)
            self.trustedStore.set_value(iter, 1, device)

##         self.trusted = checklist.CheckList(1)
##         self.trusted.connect ('button_press_event', self.trusted_select_row)
##         self.trusted.connect ("key_press_event", self.trusted_key_press)
        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        viewport.add(self.trustedView)
        self.customTable.attach (viewport, 1, 2, 2, 3, gtk.EXPAND|gtk.FILL, gtk.FILL, 5, 5)

        self.label2 = gtk.Label (_("Allow incoming:"))
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
#        self.incoming.connect ('button_press_event', self.incoming_select_row)
#        self.incoming.connect ("key_press_event", self.incoming_key_press)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.incomingView.append_column(col)

        self.list = {"DHCP":"dhcp", "SSH":"ssh", "Telnet":"telnet", "WWW (HTTP)":"http",
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
        
        #initialize custom options to not sensitive
        self.customTable.set_sensitive(gtk.FALSE)

    def item_toggled(self, data, row, store):
        iter = store.get_iter((int(row),))
        val = store.get_value(iter, 0)
        store.set_value(iter, 0 , not val)

    def disable_firewall (self, widget):
        active = not (self.securityNoneRadio.get_active())
        self.firewallDefaultRadio.set_sensitive (active)
        self.customizeRadio.set_sensitive (active)        

        if self.securityNoneRadio.get_active() == gtk.TRUE:
            self.customTable.set_sensitive (gtk.FALSE)
        else:
            self.customTable.set_sensitive(self.firewallCustomizeRadio.get_active())

    def enable_custom (self, widget):
        self.customTable.set_sensitive(self.firewallCustomizeRadio.get_active())
    
    def toggle_row (self, list, row):
        (val, row_data, header) = list.get_row_data(row)
        val = not val
        list.set_row_data(row, (val, row_data, header))
        list._update_row (row)

    def getData(self):
        buf = ""
        if self.securityHighRadio.get_active():
            buf = "--high "
        elif self.securityMediumRadio.get_active():
            buf = "--medium "
        elif self.securityNoneRadio.get_active():
            buf = "--disabled "        

        if self.customizeRadio.get_active():

            iter = self.trustedStore.get_iter_first()

            while iter:
                if self.trustedStore.get_value(iter, 0) == gtk.TRUE:
                    buf = buf + "--trust=" + self.trustedStore.get_value(iter, 1) + " "
                iter = self.trustedStore.iter_next(iter)


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
            opts, args = getopt.getopt(self.kickstartData.getFirewall(), "d:h", ["high", "medium",
                                       "disabled", "trust=", "port=", "dhcp", "ssh", "telnet",
                                       "smtp", "http", "ftp"])

            for opt, value in opts:
                if opt == "--high":
                    self.securityHighRadio.set_active(gtk.TRUE)

                if opt == "--medium":
                    self.securityMediumRadio.set_active(gtk.TRUE)

                if opt == "--disabled":
                    self.securityNoneRadio.set_active(gtk.TRUE)

                if opt=="--dhcp" or opt=="--ssh" or opt=="--telnet" or opt=="--smtp" or opt=="--http" or opt=="--ftp":

                    iter = self.incomingStore.get_iter_first()

                    while iter:
                        service = self.list[self.incomingStore.get_value(iter, 1)]
                        if service == opt[2:]:
                            self.incomingStore.set_value(iter, 0, gtk.TRUE)
                        iter = self.incomingStore.iter_next(iter)

                if opt == "--trust":
                    self.firewallCustomizeRadio.set_active(gtk.TRUE)

                    iter = self.trustedStore.get_iter_first()

                    while iter:
                        device = self.trustedStore.get_value(iter, 1) 
                        if device == value:
                            self.trustedStore.set_value(iter, 0, gtk.TRUE)
                        iter = self.trustedStore.iter_next(iter)

                if opt == "--port":
                    self.firewallCustomizeRadio.set_active(gtk.TRUE)                    
                    current = self.portsEntry.get_text()
                    self.portsEntry.set_text(value)
