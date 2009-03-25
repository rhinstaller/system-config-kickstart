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
import gobject
import socket
import string
import getopt
import gtk.glade
import firewall

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

class network:

    def __init__(self, xml, ksHandler):
        self.ks = ksHandler
        self.network_frame = xml.get_widget("network_frame")
        self.network_device_tree = xml.get_widget("network_device_tree")
        self.add_device_button = xml.get_widget("add_device_button")
        self.edit_device_button = xml.get_widget("edit_device_button")
        self.delete_device_button = xml.get_widget("delete_device_button")
        self.network_device_dialog = xml.get_widget("network_device_dialog")
        self.network_device_dialog.connect("delete-event", self.resetDialog)

        self.network_device_option_menu = xml.get_widget("network_device_option_menu")
        self.network_type_option_menu = xml.get_widget("network_type_option_menu")
        self.network_type_hbox = xml.get_widget("network_type_hbox")

        self.ip_entry = xml.get_widget("ip_entry")
        self.netmask_entry = xml.get_widget("netmask_entry")
        self.gw_entry = xml.get_widget("gw_entry")
        self.nameserver_entry = xml.get_widget("nameserver_entry")
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

        self.network_device_tree.set_property("headers-visible", True)
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
        self.network_frame.show_all()

    def updateKS(self, ksHandler):
        self.ks = ksHandler

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

                self.ip_entry.set_text(self.network_device_store.get_value(iter, 2))
                self.netmask_entry.set_text(self.network_device_store.get_value(iter, 3))

                if self.network_device_store.get_value(iter, 4) is not None:
                    self.gw_entry.set_text(self.network_device_store.get_value(iter, 4))
                else:
                    self.gw_entry.set_text("")

                if self.network_device_store.get_value(iter, 5) is not None:
                    self.nameserver_entry.set_text(self.network_device_store.get_value(iter, 5))
                else:
                    self.nameserver_entry.set_text("")

        self.handler = self.network_ok_button.connect("clicked", self.editDevice, iter)
        self.network_device_dialog.show_all()

    def deviceIsFilledIn(self):
        if self.ip_entry.get_text().strip() == "" or self.netmask_entry.get_text().strip() == "":
            return False

        try:
            socket.inet_pton(socket.AF_INET, self.ip_entry.get_text())
            socket.inet_pton(socket.AF_INET, self.netmask_entry.get_text())
            return True
        except:
            return False

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
            if not self.deviceIsFilledIn():
                text = (_("Please fill in the network information"))
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(True)
                rc = dlg.run()
                dlg.destroy()
                return None

            if self.gw_entry.get_text() != "":
                try:
                    socket.inet_pton(socket.AF_INET, self.gw_entry.get_text())
                except:
                    text = (_("Please enter a valid gateway address."))
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                    dlg.set_position(gtk.WIN_POS_CENTER)
                    dlg.set_modal(True)
                    rc = dlg.run()
                    dlg.destroy()
                    return None

            if self.nameserver_entry.get_text() != "":
                try:
                    socket.inet_pton(socket.AF_INET, self.nameserver_entry.get_text())
                except:
                    text = (_("Please enter a valid nameserver address."))
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                    dlg.set_position(gtk.WIN_POS_CENTER)
                    dlg.set_modal(True)
                    rc = dlg.run()
                    dlg.destroy()
                    return None

            iter = self.network_device_store.append()

            self.network_device_store.set_value(iter, 0, devName)
            self.network_device_store.set_value(iter, 1, _("Static IP"))
            self.network_device_store.set_value(iter, 2, self.ip_entry.get_text().strip())
            self.network_device_store.set_value(iter, 3, self.netmask_entry.get_text().strip())
            self.network_device_store.set_value(iter, 4, self.gw_entry.get_text().strip())
            self.network_device_store.set_value(iter, 5, self.nameserver_entry.get_text().strip())

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
            if not self.deviceIsFilledIn():
                text = (_("Please fill in the network information"))
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_modal(True)
                rc = dlg.run()
                dlg.destroy()
                return None

            if self.gw_entry.get_text() != "":
                try:
                    socket.inet_pton(socket.AF_INET, self.gw_entry.get_text())
                except:
                    text = (_("Please enter a valid gateway address."))
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                    dlg.set_position(gtk.WIN_POS_CENTER)
                    dlg.set_modal(True)
                    rc = dlg.run()
                    dlg.destroy()
                    return None

            if self.nameserver_entry.get_text() != "":
                try:
                    socket.inet_pton(socket.AF_INET, self.nameserver_entry.get_text())
                except:
                    text = (_("Please enter a valid nameserver address."))
                    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
                    dlg.set_position(gtk.WIN_POS_CENTER)
                    dlg.set_modal(True)
                    rc = dlg.run()
                    dlg.destroy()
                    return None

            self.network_device_store.set_value(iter, 1, _("Static IP"))
            self.network_device_store.set_value(iter, 2, self.ip_entry.get_text().strip())
            self.network_device_store.set_value(iter, 3, self.netmask_entry.get_text().strip())
            self.network_device_store.set_value(iter, 4, self.gw_entry.get_text().strip())
            self.network_device_store.set_value(iter, 5, self.nameserver_entry.get_text().strip())

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
                dlg.set_modal(True)
                rc = dlg.run()
                dlg.destroy()
                return None
            iter = self.network_device_store.iter_next(iter)

        return 0

    def resetDialog(self, *args):
        self.network_device_option_menu.set_history(0)
        self.network_type_option_menu.set_history(0)

        self.ip_entry.set_text("")
        self.netmask_entry.set_text("")
        self.gw_entry.set_text("")
        self.nameserver_entry.set_text("")

        self.network_ok_button.disconnect(self.handler)
        self.network_device_dialog.hide()
        return True

    def formToKickstart(self):
        self.ks.network(network=[])
        iter = self.network_device_store.get_iter_first()

        while iter:
            nd = self.ks.NetworkData()

            if self.network_device_store.get_value(iter, 1) == "DHCP":
                nd.bootProto = "dhcp"
            elif self.network_device_store.get_value(iter, 1) == "BOOTP":
                nd.bootProto = "bootp"
            else:
                nd.bootProto = "static"
                nd.ip = self.network_device_store.get_value(iter, 2) or ""
                nd.netmask = self.network_device_store.get_value(iter, 3) or ""
                nd.gateway = self.network_device_store.get_value(iter, 4) or ""
                nd.nameserver = self.network_device_store.get_value(iter, 5) or ""

            nd.device = self.network_device_store.get_value(iter, 0)
            self.ks.network.dataList().append(nd)
            iter = self.network_device_store.iter_next(iter)

    def typeChanged(self, *args):
        if self.network_type_option_menu.get_history() == 1:
            self.network_table.set_sensitive(True)
        else:
            self.network_table.set_sensitive(False)

    def rowSelected(self, *args):
        store, iter = self.network_device_tree.get_selection().get_selected()
        if iter == None:
            self.edit_device_button.set_sensitive(False)
            self.delete_device_button.set_sensitive(False)
        else:
            self.edit_device_button.set_sensitive(True)
            self.delete_device_button.set_sensitive(True)

    def applyKickstart(self):
        self.network_device_store.clear()

        for nic in self.ks.network.network:
            iter = self.network_device_store.append()

            if nic.device != "":
                self.network_device_store.set_value(iter, 0, nic.device)

            if nic.bootProto != "":
                if nic.bootProto == "dhcp":
                    self.network_device_store.set_value(iter, 1, "DHCP")
                elif nic.bootProto == "static":
                    self.network_device_store.set_value(iter, 1, (_("Static IP")))
                elif nic.bootProto == "bootp":
                    self.network_device_store.set_value(iter, 1, "BOOTP")

            if nic.ip != "":
                self.network_device_store.set_value(iter, 2, nic.ip)

            if nic.netmask != "":
                self.network_device_store.set_value(iter, 3, nic.netmask)

            if nic.gateway != "":
                self.network_device_store.set_value(iter, 4, nic.gateway)

            if nic.nameserver != "":
                self.network_device_store.set_value(iter, 5, nic.nameserver)
