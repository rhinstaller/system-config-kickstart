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

#Kickstart Configurator Firewall Configuration

from gtk import *
import GtkExtra
import string
import checklist
import libglade

class firewall:
    
    def __init__(self, xml):

        self.securityRadio1 = xml.get_widget("securityRadio1")
        self.securityRadio2 = xml.get_widget("securityRadio2")
        self.securityRadio3 = xml.get_widget("securityRadio3")
        self.firewallDefaultRadio = xml.get_widget("firewallDefaultRadio")
        self.firewallCustomizeRadio = xml.get_widget("firewallCustomizeRadio")        
        self.trusted_devices_label = xml.get_widget("trusted_devices_label")
        self.allow_incoming_label = xml.get_widget("allow_incoming_label")
        self.firewall_ports_label = xml.get_widget("firewall_ports_label")
        self.firewall_ports_entry = xml.get_widget("firewall_ports_entry")
        self.customTable = xml.get_widget("customTable")
        self.customFrame = xml.get_widget("customFrame")

        xml.signal_autoconnect (
            { "disable_firewall" : self.disable_firewall,
              "enable_custom" : self.enable_custom,
              })

        #create table with custom checklists
        self.label1 = GtkLabel ("Trusted devices:")
        self.label1.set_alignment (0.2, 0.0)
        self.customTable.attach (self.label1, 0, 1, 2, 3, FILL, FILL, 5, 5)
        
        f = open ("/proc/net/dev")
        lines = f.readlines()
        f.close ()
        # skip first two lines, they are header
        lines = lines[2:]
        self.netdevices = []
        for line in lines:
            dev = string.strip (line[0:6])
            if dev != "lo":
                self.netdevices.append(dev)

        self.trusted = checklist.CheckList(1)
        self.trusted.connect ('button_press_event', self.trusted_select_row)
        self.trusted.connect ("key_press_event", self.trusted_key_press)
        self.customTable.attach (self.trusted, 1, 2, 2, 3, EXPAND|FILL, FILL, 5, 5)

        for device in self.netdevices:
            self.trusted.append_row((device, device), FALSE)

        self.label2 = GtkLabel ("Allow incoming:")
        self.label2.set_alignment (0.2, 0.0)
        self.incoming = checklist.CheckList(1)
        self.incoming.connect ('button_press_event', self.incoming_select_row)
        self.incoming.connect ("key_press_event", self.incoming_key_press)
        self.customTable.attach (self.label2, 0, 1, 3, 4, FILL, FILL, 5, 5)
        self.customTable.attach (self.incoming, 1, 2, 3, 4, EXPAND|FILL, FILL, 5, 5)

        self.list = {"DHCP":"dhcp", "SSH":"ssh", "Telnet":"telnet", "WWW (HTTP)":"http",
                     "Mail (SMTP)":"smtp", "FTP":"ftp"}

        for item in self.list.keys():
            self.incoming.append_row ((item, item), FALSE)


        self.label3 = GtkLabel ("Other ports:")
        self.label3.set_alignment (0.2, 0.0)
        self.ports = GtkEntry ()
        self.customTable.attach (self.label3, 0, 1, 4, 5, FILL, FILL, 5, 5)
        self.customTable.attach (self.ports, 1, 2, 4, 5, EXPAND|FILL, FILL, 5, 5)
        
        #initialize custom options to not sensitive
        self.label1.set_sensitive(FALSE)
        self.label2.set_sensitive(FALSE)
        self.label3.set_sensitive(FALSE)        
        self.trusted.set_sensitive(FALSE)
        self.incoming.set_sensitive(FALSE)
        self.ports.set_sensitive(FALSE)
        
    def disable_firewall (self, widget):
        active = not (self.securityRadio3.get_active())
        self.customFrame.set_sensitive (active)

    def enable_custom (self, widget):
        self.label1.set_sensitive(self.firewallCustomizeRadio.get_active())
        self.label2.set_sensitive(self.firewallCustomizeRadio.get_active())
        self.label3.set_sensitive(self.firewallCustomizeRadio.get_active())        
        self.trusted.set_sensitive(self.firewallCustomizeRadio.get_active())
        self.incoming.set_sensitive(self.firewallCustomizeRadio.get_active())
        self.ports.set_sensitive(self.firewallCustomizeRadio.get_active())
    
    def trusted_select_row(self, clist, event):
        try:
            row, col  = self.trusted.get_selection_info (event.x, event.y)
            self.toggle_row(self.trusted, row)
        except:
            pass

    def trusted_key_press (self, list, event):
        if event.keyval == ord(" ") and self.trusted.focus_row != -1:
            self.toggle_row (self.trusted, self.trusted.focus_row)
            
    def incoming_select_row(self, clist, event):
        try:
            row, col  = self.incoming.get_selection_info (event.x, event.y)
            self.toggle_row(self.incoming, row)
        except:
            pass    
        
    def incoming_key_press (self, list, event):
        if event.keyval == ord(" ") and self.incoming.focus_row != -1:
            self.toggle_row (self.incoming, self.incoming.focus_row)   

    def toggle_row (self, list, row):
        (val, row_data, header) = list.get_row_data(row)
        val = not val
        list.set_row_data(row, (val, row_data, header))
        list._update_row (row)

    def getData(self):
        return self.data

    def grabData(self):
        buf = "firewall "
        if self.securityRadio1.get_active():
            buf = buf + "--high "
        elif self.securityRadio2.get_active():
            buf = buf + "--medium "
        elif self.securityRadio3.get_active():
            buf = buf + "--disabled "        

        if self.customize.get_active():

            numdev = len(self.netdevices)
            for i in range(numdev):
                (val, row_data, header) = self.trusted.get_row_data (i)
                    
                if val == 1:
                    buf = buf + "--trust " + self.netdevices[i] + " "
                elif val == 0:
                    pass

            list_keys = self.list.keys()
            numserv = len(self.list)
            for i in list_keys:
                (val, row_data, header) = self.incoming.get_row_data (list_keys.index(i))
                if val == 1:
                    buf = buf + "--" + self.list[i] + " "
                elif val == 0:
                    pass

        self.data = buf
