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

#Kickstart Configurator Network Configuration

from gtk import *
import GtkExtra
import libglade

class network:

    def __init__(self, xml):
        self.ip_radiobutton = xml.get_widget("ip_radiobutton")
        self.ip_entry1 = xml.get_widget("ip_entry1")
        self.ip_entry2 = xml.get_widget("ip_entry2")
        self.ip_entry3 = xml.get_widget("ip_entry3")
        self.ip_entry4 = xml.get_widget("ip_entry4")
        self.netmask_entry1 = xml.get_widget("netmask_entry1")
        self.netmask_entry2 = xml.get_widget("netmask_entry2")
        self.netmask_entry3 = xml.get_widget("netmask_entry3")
        self.netmask_entry4 = xml.get_widget("netmask_entry4")
        self.gw_entry1 = xml.get_widget("gw_entry1")
        self.gw_entry2 = xml.get_widget("gw_entry2")
        self.gw_entry3 = xml.get_widget("gw_entry3")
        self.gw_entry4 = xml.get_widget("gw_entry4")
        self.nameserver_entry1 = xml.get_widget("nameserver_entry1")
        self.nameserver_entry2 = xml.get_widget("nameserver_entry2")
        self.nameserver_entry3 = xml.get_widget("nameserver_entry3")
        self.nameserver_entry4 = xml.get_widget("nameserver_entry4")

        xml.signal_autoconnect (
            { "toggleIP" : self.toggleIP,
          } )

    def getData(self):
        buf = ""
        if self.networkRadio1.get_active():
            buf = buf + "\n" + "network --bootproto dhcp"
            return buf
        elif self.networkRadio2.get_active():
            buf = buf + "\n" + "network --bootproto static "
            
            ipBuf = (" --ip %s.%s.%s.%s " % (self.ipEntry1.get_text(),
                                             self.ipEntry2.get_text(),
                                             self.ipEntry3.get_text(),
                                             self.ipEntry4.get_text())) 

            netmaskBuf = (" --netmask %s.%s.%s.%s " %
                                           (self.netmaskEntry1.get_text(),
                                           self.netmaskEntry2.get_text(),
                                           self.netmaskEntry3.get_text(),
                                           self.netmaskEntry4.get_text()))

            gatewayBuf = (" --gateway %s.%s.%s.%s " %
                                           (self.gatewayEntry1.get_text(),
                                           self.gatewayEntry2.get_text(),
                                           self.gatewayEntry3.get_text(),
                                           self.gatewayEntry4.get_text()))

            nameserverBuf = (" --nameserver %s.%s.%s.%s " %
                                           (self.dnsEntry1.get_text(),
                                           self.dnsEntry2.get_text(),
                                           self.dnsEntry3.get_text(),
                                           self.dnsEntry4.get_text()))
            buf = buf + ipBuf + netmaskBuf + gatewayBuf + nameserverBuf
            return buf

    def toggleIP(self, args):
        self.ip_entry1.set_sensitive(self.ip_radiobutton.get_active())
        self.ip_entry2.set_sensitive(self.ip_radiobutton.get_active())
        self.ip_entry3.set_sensitive(self.ip_radiobutton.get_active())
        self.ip_entry4.set_sensitive(self.ip_radiobutton.get_active())
        self.netmask_entry1.set_sensitive(self.ip_radiobutton.get_active())
        self.netmask_entry2.set_sensitive(self.ip_radiobutton.get_active())
        self.netmask_entry3.set_sensitive(self.ip_radiobutton.get_active())
        self.netmask_entry4.set_sensitive(self.ip_radiobutton.get_active())
        self.gw_entry1.set_sensitive(self.ip_radiobutton.get_active())
        self.gw_entry2.set_sensitive(self.ip_radiobutton.get_active())
        self.gw_entry3.set_sensitive(self.ip_radiobutton.get_active())
        self.gw_entry4.set_sensitive(self.ip_radiobutton.get_active())
        self.nameserver_entry1.set_sensitive(self.ip_radiobutton.get_active())
        self.nameserver_entry2.set_sensitive(self.ip_radiobutton.get_active())
        self.nameserver_entry3.set_sensitive(self.ip_radiobutton.get_active())
        self.nameserver_entry4.set_sensitive(self.ip_radiobutton.get_active())
