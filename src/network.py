#!/usr/bin/env python

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

#Kickstart Configurator Network Configuration

import gtk
import gobject
import string
import getopt
import gtk.glade

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'redhat-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class network:

    def __init__(self, xml, kickstartData):
        self.kickstartData = kickstartData
        self.network_device_tree = xml.get_widget("network_device_tree")
        self.add_device_button = xml.get_widget("add_device_button")
        self.edit_device_button = xml.get_widget("edit_device_button")
        self.delete_device_button = xml.get_widget("delete_device_button")
        self.network_device_dialog = xml.get_widget("network_device_dialog")
        self.network_device_dialog.connect("delete-event", self.resetDialog)

        self.network_device_option_menu = xml.get_widget("network_device_option_menu")
        self.network_type_option_menu = xml.get_widget("network_type_option_menu")        
        self.network_type_hbox = xml.get_widget("network_type_hbox")

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
        self.network_table = xml.get_widget("network_table")
        self.network_ok_button = xml.get_widget("network_ok_button")
        self.network_cancel_button = xml.get_widget("network_cancel_button")

        self.network_device_tree.get_selection().connect("changed", self.rowSelected)
        self.add_device_button.connect("clicked", self.showAddNetworkDialog)
        self.edit_device_button.connect("clicked", self.showEditNetworkDialog)        
        self.delete_device_button.connect("clicked", self.deleteDevice)

        self.network_device_store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                                                  gobject.TYPE_STRING, gobject.TYPE_STRING,
                                                  gobject.TYPE_STRING, gobject.TYPE_STRING,)

        self.network_device_tree.set_model(self.network_device_store)

        self.network_device_tree.set_property("headers-visible", gtk.TRUE)
        col = gtk.TreeViewColumn(_("Device"), gtk.CellRendererText(), text = 0)
        self.network_device_tree.append_column(col)

        col = gtk.TreeViewColumn(_("Network Type"), gtk.CellRendererText(), text = 1)
        self.network_device_tree.append_column(col)
        

        self.deviceMenu = gtk.Menu()
        self.deviceList = []

        for i in range(17):
            dev = "eth%d" %i
            item = gtk.MenuItem(dev)
            self.deviceList.append(dev)
            self.deviceMenu.append(item)

        self.network_device_option_menu.set_menu(self.deviceMenu)
        self.network_device_option_menu.show_all()

        self.typeMenu = gtk.Menu()
        item = gtk.MenuItem("DHCP")
        self.typeMenu.append(item)
        item = gtk.MenuItem(_("Static IP"))
        self.typeMenu.append(item)
        item = gtk.MenuItem("BOOTP")
        self.typeMenu.append(item)

        self.network_type_option_menu.set_menu(self.typeMenu)
        self.network_type_hbox.show_all()

        self.network_type_option_menu.connect("changed", self.typeChanged)
        self.network_cancel_button.connect("clicked", self.resetDialog)
        
    def showAddNetworkDialog(self, *args):
        self.handler = self.network_ok_button.connect("clicked", self.addDevice)

        #Let's find the last eth device in the list and increment by one to
        #fill in the option menu with the next device
        device = None
        iter = self.network_device_store.get_iter_first()
        while iter:
            device = self.network_device_store.get_value(iter, 0)
            iter = self.network_device_store.iter_next(iter)

        if device == None:
            num = 0
        else:
            num = int(device[3:])
            if num < 15:
                num = num + 1

        self.network_device_option_menu.set_history(num)
        self.network_device_dialog.show_all()

    def showEditNetworkDialog(self, *args):
        rc = self.network_device_tree.get_selection().get_selected()

        if rc:
            store, iter = rc

            device = self.network_device_store.get_value(iter, 0)
            num = self.deviceList.index(device)
            self.network_device_option_menu.set_history(num)

            type = self.network_device_store.get_value(iter, 1)
            if type == "DHCP":
                self.network_type_option_menu.set_history(0)
            elif type == (_("Static IP")):
                self.network_type_option_menu.set_history(1)
                
                ip = self.network_device_store.get_value(iter, 2)
                ip1, ip2, ip3, ip4 = string.split(ip, ".")
                self.ip_entry1.set_text(ip1)
                self.ip_entry2.set_text(ip2)
                self.ip_entry3.set_text(ip3)
                self.ip_entry4.set_text(ip4)

                ip = self.network_device_store.get_value(iter, 3)
                ip1, ip2, ip3, ip4 = string.split(ip, ".")
                self.netmask_entry1.set_text(ip1)
                self.netmask_entry2.set_text(ip2)
                self.netmask_entry3.set_text(ip3)
                self.netmask_entry4.set_text(ip4)

                ip = self.network_device_store.get_value(iter, 4)
                ip1, ip2, ip3, ip4 = string.split(ip, ".")
                self.gw_entry1.set_text(ip1)
                self.gw_entry2.set_text(ip2)
                self.gw_entry3.set_text(ip3)
                self.gw_entry4.set_text(ip4)

                ip = self.network_device_store.get_value(iter, 5)
                ip1, ip2, ip3, ip4 = string.split(ip, ".")
                self.nameserver_entry1.set_text(ip1)
                self.nameserver_entry2.set_text(ip2)
                self.nameserver_entry3.set_text(ip3)
                self.nameserver_entry4.set_text(ip4)            

        self.handler = self.network_ok_button.connect("clicked", self.editDevice, iter)
        self.network_device_dialog.show_all()

    def addDevice(self, *args):
        devNum = self.network_device_option_menu.get_history()
        devName = self.deviceList[devNum]

        if self.doesDeviceExist(devName) is None:
            return

        if self.network_type_option_menu.get_history() == 0:
            iter = self.network_device_store.append()
            self.network_device_store.set_value(iter, 0, devName)
            self.network_device_store.set_value(iter, 1, "DHCP")
        elif self.network_type_option_menu.get_history() == 2:
            iter = self.network_device_store.append()
            self.network_device_store.set_value(iter, 0, devName)
            self.network_device_store.set_value(iter, 1, "BOOTP")
        else:
            if self.ip_entry1.get_text() == "" or self.ip_entry2.get_text() == "" or \
            self.ip_entry3.get_text() == "" or self.ip_entry4.get_text() == "" or \
            self.netmask_entry1.get_text() == "" or self.netmask_entry2.get_text() == "" or \
            self.netmask_entry3.get_text() == "" or self.netmask_entry4.get_text() == "" or \
            self.gw_entry1.get_text() == "" or self.gw_entry2.get_text() == "" or \
            self.gw_entry3.get_text() == "" or self.gw_entry4.get_text() == "" or \
            self.nameserver_entry1.get_text() == "" or self.nameserver_entry2.get_text() == "" or \
            self.nameserver_entry3.get_text() == "" or self.nameserver_entry4.get_text() == "":
                print "uh uh"

                text = (_("Please fill in the network information"))
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(gtk.TRUE)
                rc = dlg.run()
                dlg.destroy()
                return None

            iter = self.network_device_store.append()
            self.network_device_store.set_value(iter, 0, devName)
            self.network_device_store.set_value(iter, 1, _("Static IP"))
        
            ipBuf = ("%s.%s.%s.%s" %
                     (self.ip_entry1.get_text(),
                      self.ip_entry2.get_text(),
                      self.ip_entry3.get_text(),
                      self.ip_entry4.get_text())) 
            self.network_device_store.set_value(iter, 2, ipBuf)

            netmaskBuf = ("%s.%s.%s.%s" %
                          (self.netmask_entry1.get_text(),
                           self.netmask_entry2.get_text(),
                           self.netmask_entry3.get_text(),
                           self.netmask_entry4.get_text()))
            self.network_device_store.set_value(iter, 3, netmaskBuf)

            gatewayBuf = ("%s.%s.%s.%s" %
                          (self.gw_entry1.get_text(),
                           self.gw_entry2.get_text(),
                           self.gw_entry3.get_text(),
                           self.gw_entry4.get_text()))
            self.network_device_store.set_value(iter, 4, gatewayBuf)

            nameserverBuf = ("%s.%s.%s.%s" %
                             (self.nameserver_entry1.get_text(),
                              self.nameserver_entry2.get_text(),
                              self.nameserver_entry3.get_text(),
                              self.nameserver_entry4.get_text()))     
            self.network_device_store.set_value(iter, 5, nameserverBuf)

        self.resetDialog()
        
    def editDevice(self, button, iter):
        devNum = self.network_device_option_menu.get_history()
        devName = self.deviceList[devNum]
        
        if self.network_device_store.get_value(iter, 0) != devName:
            if self.doesDeviceExist(devName) is None:
                return

        self.network_device_store.set_value(iter, 0, devName)

        if self.network_type_option_menu.get_history() == 0:
            self.network_device_store.set_value(iter, 1, "DHCP")
        elif self.network_type_option_menu.get_history() == 2:
            self.network_device_store.set_value(iter, 1, "BOOTP")
        else:
            self.network_device_store.set_value(iter, 1, _("Static IP"))
        
            ipBuf = ("%s.%s.%s.%s" %
                     (self.ip_entry1.get_text(),
                      self.ip_entry2.get_text(),
                      self.ip_entry3.get_text(),
                      self.ip_entry4.get_text())) 
            self.network_device_store.set_value(iter, 2, ipBuf)

            netmaskBuf = ("%s.%s.%s.%s" %
                          (self.netmask_entry1.get_text(),
                           self.netmask_entry2.get_text(),
                           self.netmask_entry3.get_text(),
                           self.netmask_entry4.get_text()))
            self.network_device_store.set_value(iter, 3, netmaskBuf)

            gatewayBuf = ("%s.%s.%s.%s" %
                          (self.gw_entry1.get_text(),
                           self.gw_entry2.get_text(),
                           self.gw_entry3.get_text(),
                           self.gw_entry4.get_text()))
            self.network_device_store.set_value(iter, 4, gatewayBuf)

            nameserverBuf = ("%s.%s.%s.%s" %
                             (self.nameserver_entry1.get_text(),
                              self.nameserver_entry2.get_text(),
                              self.nameserver_entry3.get_text(),
                              self.nameserver_entry4.get_text()))     
            self.network_device_store.set_value(iter, 5, nameserverBuf)

        self.resetDialog()
        
    def deleteDevice(self, *args):
        rc = self.network_device_tree.get_selection().get_selected()

        if rc:
            store, iter = rc
            self.network_device_store.remove(iter)

    def doesDeviceExist(self, devName):
        iter = self.network_device_store.get_iter_first()

        while iter:
            if devName == self.network_device_store.get_value(iter, 0):
                text = (_("A network device with the name %s already exists.  Please "\
                          "choose another device name" % devName))
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(gtk.TRUE)
                rc = dlg.run()
                dlg.destroy()
                return None
            iter = self.network_device_store.iter_next(iter)
            
        return 0

    def resetDialog(self, *args):
        self.network_device_option_menu.set_history(0)
        self.network_type_option_menu.set_history(0)        
        self.ip_entry1.set_text("")
        self.ip_entry2.set_text("")
        self.ip_entry3.set_text("")
        self.ip_entry4.set_text("")

        self.netmask_entry1.set_text("")
        self.netmask_entry2.set_text("")
        self.netmask_entry3.set_text("")
        self.netmask_entry4.set_text("")

        self.gw_entry1.set_text("")
        self.gw_entry2.set_text("")
        self.gw_entry3.set_text("")
        self.gw_entry4.set_text("")

        self.nameserver_entry1.set_text("")
        self.nameserver_entry2.set_text("")
        self.nameserver_entry3.set_text("")
        self.nameserver_entry4.set_text("")            

        self.network_ok_button.disconnect(self.handler)
        self.network_device_dialog.hide()
        return gtk.TRUE

    def getData(self):
        self.kickstartData.clearNetwork()
        iter = self.network_device_store.get_iter_first()
        while iter:
            data = []
            if self.network_device_store.get_value(iter, 1) == "DHCP":
                data.append("--bootproto=dhcp")
            elif self.network_device_store.get_value(iter, 1) == "BOOTP":
                data.append("--bootproto=bootp")
            else:
                data.append("--bootproto=static")
                data.append("--ip=%s" %self.network_device_store.get_value(iter, 2))
                data.append("--netmask=%s" % self.network_device_store.get_value(iter, 3))
                data.append("--gateway=%s" % self.network_device_store.get_value(iter, 4))
                data.append("--nameserver=%s" % self.network_device_store.get_value(iter, 5))

            data.append("--device=%s" % self.network_device_store.get_value(iter, 0))
            self.kickstartData.setNetwork(data)                    
            iter = self.network_device_store.iter_next(iter)

    def typeChanged(self, *args):
        if self.network_type_option_menu.get_history() == 1:
            self.network_table.set_sensitive(gtk.TRUE)
        else:
            self.network_table.set_sensitive(gtk.FALSE)            

    def rowSelected(self, *args):
        store, iter = self.network_device_tree.get_selection().get_selected()
        if iter == None:
            self.edit_device_button.set_sensitive(gtk.FALSE)
            self.delete_device_button.set_sensitive(gtk.FALSE)
        else:
            self.edit_device_button.set_sensitive(gtk.TRUE)
            self.delete_device_button.set_sensitive(gtk.TRUE)
            
    def fillData(self):
        networkList = self.kickstartData.getNetwork()

        for line in networkList:
            iter = self.network_device_store.append()
            opts, args = getopt.getopt(line, "d:h", ["bootproto=", "device=", "ip=", "gateway=",
                                                     "nameserver=", "nodns=", "netmask=",
                                                     "hostname="])
            
            for opt, value in opts:
                if opt == "--device":
                    self.network_device_store.set_value(iter, 0, value)

                if opt == "--bootproto":
                    if value == "dhcp":
                        self.network_device_store.set_value(iter, 1, "DHCP")
                    elif value == "static":
                        self.network_device_store.set_value(iter, 1, (_("Static IP")))
                    elif value == "bootp":
                        self.network_device_store.set_value(iter, 1, "BOOTP")

                if opt == "--ip":
                    self.network_device_store.set_value(iter, 2, value)

                if opt == "--netmask":
                    self.network_device_store.set_value(iter, 3, value)

                if opt == "--gateway":
                    self.network_device_store.set_value(iter, 4, value)

                if opt == "--nameserver":
                    self.network_device_store.set_value(iter, 5, value)

