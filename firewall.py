#!/usr/bin/env python

#Kickstart Configurator Firewall Options
#Copyright Red Hat, Inc. 2001
#Written by Brent Fox (bfox@redhat.com) and Tammy Fox (tfox@redhat.com)
#This file created January 31, 2001 Tammy Fox
#Last Modified: January 31, 2001 Brent Fox


from gtk import *
import GtkExtra
import string
import checklist

class firewallWindow (GtkWindow):
    def okClicked(self, args):
        self.grabData()
        self.destroy()

    def cancelClicked(self, args):
        self.destroy()    


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


    def activate_firewall (self, widget):
        active = not (self.securityRadio3.get_active())
        self.customFrame.set_sensitive (active)

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

        
    def __init__(self):
        GtkWindow.__init__(self, WINDOW_TOPLEVEL)
        self.set_modal(TRUE)
        self.set_border_width(6)
        self.set_default_size(400, 100)		
        self.set_title("Firewall Configuration")

        self.vbox = GtkVBox()
        self.add(self.vbox)
			
        securityFrame = GtkFrame("Security Level")
        self.vbox.pack_start(securityFrame)

        securityHbox = GtkHBox()
        securityFrame.add(securityHbox)

        self.securityRadio1 = GtkRadioButton(None, "High")
        securityHbox.pack_start(self.securityRadio1)

        self.securityRadio2 = GtkRadioButton(self.securityRadio1, "Medium")
        securityHbox.pack_start(self.securityRadio2)

        self.securityRadio3 = GtkRadioButton(self.securityRadio1, "Disabled")
        securityHbox.pack_start(self.securityRadio3)
        self.securityRadio3.connect("toggled", self.activate_firewall)

#        securityTable = GtkTable(4, 2, FALSE)
#        securityHbox.pack_start(securityTable)

        self.customFrame = GtkFrame("Customize")
        self.vbox.pack_start(self.customFrame)

        customTable = GtkTable(2, 2)
        self.customFrame.add(customTable)

        self.default = GtkRadioButton(None, "Use default firewall rules")
        customTable.attach (self.default, 0, 1, 0, 1, EXPAND|FILL, FILL, 5, 5)

        self.customize = GtkRadioButton(self.default, "Customize")
        customTable.attach (self.customize, 0, 1, 1, 2, EXPAND|FILL, FILL, 5, 5)
        

        label = GtkLabel ("Trusted devices:")
        label.set_alignment (0.2, 0.0)
        customTable.attach (label, 0, 1, 2, 3, FILL, FILL, 5, 5)
        
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
        customTable.attach (self.trusted, 1, 2, 2, 3, EXPAND|FILL, FILL, 5, 5)

        for device in self.netdevices:
            self.trusted.append_row((device, device), FALSE)

        label = GtkLabel ("Allow incoming:")
        label.set_alignment (0.2, 0.0)
        self.incoming = checklist.CheckList(1)
        self.incoming.connect ('button_press_event', self.incoming_select_row)
        self.incoming.connect ("key_press_event", self.incoming_key_press)
        customTable.attach (label, 0, 1, 3, 4, FILL, FILL, 5, 5)
        customTable.attach (self.incoming, 1, 2, 3, 4, EXPAND|FILL, FILL, 5, 5)

        self.list = {"DHCP":"dhcp", "SSH":"ssh", "Telnet":"telnet", "WWW (HTTP)":"http",
                     "Mail (SMTP)":"smtp", "FTP":"ftp"}

        for item in self.list.keys():
            self.incoming.append_row ((item, item), FALSE)


        label = GtkLabel ("Other ports:")
        label.set_alignment (0.2, 0.0)
        self.ports = GtkEntry ()

        customTable.attach (label, 0, 1, 4, 5, FILL, FILL, 5, 5)
        customTable.attach (self.ports, 1, 2, 4, 5, EXPAND|FILL, FILL, 5, 5)


        #----------Ok and Cancel Buttons for Authenication window--------#
        self.hbox = GtkHBox()
        self.vbox.pack_start(self.hbox)

        self.okButton = GtkButton("Ok")
        self.okButton.connect("clicked", self.okClicked)
        self.hbox.pack_start(self.okButton)

        self.cancelButton = GtkButton("Cancel")
        self.cancelButton.connect("clicked", self.cancelClicked)
        self.hbox.pack_start(self.cancelButton)


        #custom check lists
        
        self.show_all()
