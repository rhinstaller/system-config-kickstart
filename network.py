#!/usr/bin/env python

#Kickstart Configurator Authentication Options
#Copyright Red Hat, Inc. 2001
#Written by Brent Fox (bfox@redhat.com) and Tammy Fox (tfox@redhat.com)
#Created August 10, 2000 Brent Fox
#Last Modified: January 27, 2001 Tammy Fox

from gtk import *
import GtkExtra

class networkWindow(GtkWindow):
    def okClicked(self, args):        
#        print self.getData()
        self.destroy()

    def cancelClicked(self, args):
#        self.myNisClass.set_disabled()
#        self.myKerberosClass.set_disabled()
        self.destroy()

    def getData(self):
        buf = ""
        if self.networkRadio1.get_active():
            buf = buf + "\n" + "network --bootproto dhcp"
            return buf
        elif self.networkRadio2.get_active():
            buf = buf + "\n" + "network --bootproto static "
            
            ipBuf = (" --ip %s.%s.%s.%s " % (self.ipEntry1.get_text(), self.ipEntry2.get_text(),
                                           self.ipEntry3.get_text(), self.ipEntry4.get_text())) 

            netmaskBuf = (" --netmask %s.%s.%s.%s " % (self.netmaskEntry1.get_text(), self.netmaskEntry2.get_text(),
                                           self.netmaskEntry3.get_text(), self.netmaskEntry4.get_text()))

            gatewayBuf = (" --gateway %s.%s.%s.%s " % (self.gatewayEntry1.get_text(), self.gatewayEntry2.get_text(),
                                           self.gatewayEntry3.get_text(), self.gatewayEntry4.get_text()))

            nameserverBuf = (" --nameserver %s.%s.%s.%s " % (self.dnsEntry1.get_text(), self.dnsEntry2.get_text(),
                                           self.dnsEntry3.get_text(), self.dnsEntry4.get_text())) 
            buf = buf + ipBuf + netmaskBuf + gatewayBuf + nameserverBuf
            return buf

    def toggleIP(self, args):
        self.ipEntry1.set_sensitive(self.networkRadio2.get_active())
        self.ipEntry2.set_sensitive(self.networkRadio2.get_active())
        self.ipEntry3.set_sensitive(self.networkRadio2.get_active())
        self.ipEntry4.set_sensitive(self.networkRadio2.get_active())
        self.netmaskEntry1.set_sensitive(self.networkRadio2.get_active())
        self.netmaskEntry2.set_sensitive(self.networkRadio2.get_active())
        self.netmaskEntry3.set_sensitive(self.networkRadio2.get_active())
        self.netmaskEntry4.set_sensitive(self.networkRadio2.get_active())
        self.gatewayEntry1.set_sensitive(self.networkRadio2.get_active())
        self.gatewayEntry2.set_sensitive(self.networkRadio2.get_active())
        self.gatewayEntry3.set_sensitive(self.networkRadio2.get_active())
        self.gatewayEntry4.set_sensitive(self.networkRadio2.get_active())
        self.dnsEntry1.set_sensitive(self.networkRadio2.get_active())
        self.dnsEntry2.set_sensitive(self.networkRadio2.get_active())
        self.dnsEntry3.set_sensitive(self.networkRadio2.get_active())
        self.dnsEntry4.set_sensitive(self.networkRadio2.get_active())


    def __init__(self, quit_cb=None):
        GtkWindow.__init__(self, WINDOW_TOPLEVEL)
        self.set_modal(TRUE)
        self.set_border_width(6)
        self.set_default_size(400, 100)		
        self.set_title("Network Configuration")

        self.vbox = GtkVBox()
        self.add(self.vbox)
        
        #-------------------Network settings----------------#
        frame3 = GtkFrame("Network Configuration")
        frame3.set_label("Network Configuration")
        self.vbox.pack_start(frame3)

        networkVbox = GtkVBox()
        frame3.add(networkVbox)


        networkHbox = GtkHBox()
        networkVbox.pack_start(networkHbox)

        networkLabel = GtkLabel("Network Configuration:")
        networkHbox.pack_start(networkLabel)

        self.networkRadio1 = GtkRadioButton(None, "DHCP")
        networkHbox.pack_start(self.networkRadio1)
        self.networkRadio1.connect("toggled", self.toggleIP)

        self.networkRadio2 = GtkRadioButton(self.networkRadio1, "Static IP")
        networkHbox.pack_start(self.networkRadio2)
        self.networkRadio2.connect("toggled", self.toggleIP)

        networkRadio3 = GtkRadioButton(self.networkRadio1, "None")
        networkHbox.pack_start(networkRadio3)
        networkRadio3.connect("toggled", self.toggleIP)


        table2 = GtkTable(4, 2, FALSE)
        networkVbox.pack_start(table2) 

        #---ip---#
        ipHBox = GtkHBox()

        ipLabel = GtkLabel("IP Address:")
        table2.attach(ipLabel, 0, 1, 0, 1)
        table2.attach(ipHBox, 1, 2, 0, 1)


        ipDot1 = GtkLabel(".")
        ipDot2 = GtkLabel(".")
        ipDot3 = GtkLabel(".")

        self.ipEntry1 = GtkEntry()
        self.ipEntry1.set_max_length(3)
        self.ipEntry1.set_usize(15, 20)
        ipHBox.pack_start(self.ipEntry1)
        self.ipEntry1.set_state(STATE_INSENSITIVE)

        ipHBox.pack_start(ipDot1)

        self.ipEntry2 = GtkEntry(3)
        self.ipEntry2.set_max_length(3)
        self.ipEntry2.set_usize(15, 20)
        ipHBox.pack_start(self.ipEntry2)
        self.ipEntry2.set_state(STATE_INSENSITIVE)

        ipHBox.pack_start(ipDot2)

        self.ipEntry3 = GtkEntry()
        self.ipEntry3.set_max_length(3)
        self.ipEntry3.set_usize(15, 20)
        ipHBox.pack_start(self.ipEntry3)
        self.ipEntry3.set_state(STATE_INSENSITIVE)

        ipHBox.pack_start(ipDot3)

        self.ipEntry4 = GtkEntry()
        self.ipEntry4.set_max_length(3)
        self.ipEntry4.set_usize(15, 20)
        ipHBox.pack_start(self.ipEntry4)
        self.ipEntry4.set_state(STATE_INSENSITIVE)

        #---netmask---#
        netmaskHBox = GtkHBox()
        netmaskLabel = GtkLabel("Netmask:")
        table2.attach(netmaskLabel, 0, 1, 1, 2)
        table2.attach(netmaskHBox, 1, 2, 1, 2)


        netmaskDot1 = GtkLabel(".")
        netmaskDot2 = GtkLabel(".")
        netmaskDot3 = GtkLabel(".")

        self.netmaskEntry1 = GtkEntry()
        self.netmaskEntry1.set_max_length(3)
        self.netmaskEntry1.set_usize(15, 20)
        netmaskHBox.pack_start(self.netmaskEntry1)
        self.netmaskEntry1.set_state(STATE_INSENSITIVE)

        netmaskHBox.pack_start(netmaskDot1)

        self.netmaskEntry2 = GtkEntry(3)
        self.netmaskEntry2.set_max_length(3)
        self.netmaskEntry2.set_usize(15, 20)
        netmaskHBox.pack_start(self.netmaskEntry2)
        self.netmaskEntry2.set_state(STATE_INSENSITIVE)

        netmaskHBox.pack_start(netmaskDot2)

        self.netmaskEntry3 = GtkEntry()
        self.netmaskEntry3.set_max_length(3)
        self.netmaskEntry3.set_usize(15, 20)
        netmaskHBox.pack_start(self.netmaskEntry3)
        self.netmaskEntry3.set_state(STATE_INSENSITIVE)

        netmaskHBox.pack_start(netmaskDot3)

        self.netmaskEntry4 = GtkEntry()
        self.netmaskEntry4.set_max_length(3)
        self.netmaskEntry4.set_usize(15, 20)
        netmaskHBox.pack_start(self.netmaskEntry4)
        self.netmaskEntry4.set_state(STATE_INSENSITIVE)

        #---gateway---#
        gatewayHBox = GtkHBox()

        gatewayLabel = GtkLabel("Gateway:")
        table2.attach(gatewayLabel, 0, 1, 2, 3)
        table2.attach(gatewayHBox, 1, 2, 2, 3)


        gatewayDot1 = GtkLabel(".")
        gatewayDot2 = GtkLabel(".")
        gatewayDot3 = GtkLabel(".")

        self.gatewayEntry1 = GtkEntry()
        self.gatewayEntry1.set_max_length(3)
        self.gatewayEntry1.set_usize(15, 20)
        gatewayHBox.pack_start(self.gatewayEntry1)
        self.gatewayEntry1.set_state(STATE_INSENSITIVE)

        gatewayHBox.pack_start(gatewayDot1)

        self.gatewayEntry2 = GtkEntry(3)
        self.gatewayEntry2.set_max_length(3)
        self.gatewayEntry2.set_usize(15, 20)
        gatewayHBox.pack_start(self.gatewayEntry2)
        self.gatewayEntry2.set_state(STATE_INSENSITIVE)

        gatewayHBox.pack_start(gatewayDot2)

        self.gatewayEntry3 = GtkEntry()
        self.gatewayEntry3.set_max_length(3)
        self.gatewayEntry3.set_usize(15, 20)
        gatewayHBox.pack_start(self.gatewayEntry3)
        self.gatewayEntry3.set_state(STATE_INSENSITIVE)

        gatewayHBox.pack_start(gatewayDot3)

        self.gatewayEntry4 = GtkEntry()
        self.gatewayEntry4.set_max_length(3)
        self.gatewayEntry4.set_usize(15, 20)
        gatewayHBox.pack_start(self.gatewayEntry4)
        self.gatewayEntry4.set_state(STATE_INSENSITIVE)

        #---Nameserver---#
        dnsHBox = GtkHBox()

        dnsLabel = GtkLabel("Nameserver:")
        table2.attach(dnsLabel, 0, 1, 3, 4)
        table2.attach(dnsHBox, 1, 2, 3, 4)


        dnsDot1 = GtkLabel(".")
        dnsDot2 = GtkLabel(".")
        dnsDot3 = GtkLabel(".")

        self.dnsEntry1 = GtkEntry()
        self.dnsEntry1.set_max_length(3)
        self.dnsEntry1.set_usize(15, 20)
        dnsHBox.pack_start(self.dnsEntry1)
        self.dnsEntry1.set_state(STATE_INSENSITIVE)

        dnsHBox.pack_start(dnsDot1)

        self.dnsEntry2 = GtkEntry(3)
        self.dnsEntry2.set_max_length(3)
        self.dnsEntry2.set_usize(15, 20)
        dnsHBox.pack_start(self.dnsEntry2)
        self.dnsEntry2.set_state(STATE_INSENSITIVE)

        dnsHBox.pack_start(dnsDot2)

        self.dnsEntry3 = GtkEntry()
        self.dnsEntry3.set_max_length(3)
        self.dnsEntry3.set_usize(15, 20)
        dnsHBox.pack_start(self.dnsEntry3)
        self.dnsEntry3.set_state(STATE_INSENSITIVE)

        dnsHBox.pack_start(dnsDot3)

        self.dnsEntry4 = GtkEntry()
        self.dnsEntry4.set_max_length(3)
        self.dnsEntry4.set_usize(15, 20)
        dnsHBox.pack_start(self.dnsEntry4)
        self.dnsEntry4.set_state(STATE_INSENSITIVE)


        #----------Ok and Cancel Buttons for Authenication window--------#
        self.hbox = GtkHBox()
        self.vbox.pack_start(self.hbox)

        self.okButton = GtkButton("Ok")
        self.okButton.connect("clicked", self.okClicked)
        self.hbox.pack_start(self.okButton)

        self.cancelButton = GtkButton("Cancel")
        self.cancelButton.connect("clicked", self.cancelClicked)
        self.hbox.pack_start(self.cancelButton)
        

        self.show_all()
