#!/usr/bin/env python
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


from gtk import *
import GtkExtra

class nisData:
    def __init__(self, quit_cb=None):
        global nisdomain
        global nisserver
        self.nisdomain = ''
        self.nisserver = ''
        self.broadcast = "OFF"
        self.disabled = "TRUE"
    def set_domain(self, name):
        self.nisdomain = name
    def set_server(self, name):
        self.nisserver = name
    def set_disabled(self):
        self.disabled = "TRUE"
    def set_enabled(self):
        self.disabled = "FALSE"
    def set_broadcast(self, name):
        self.broadcast = name
    def return_domain(self):
        return self.nisdomain
    def return_server(self):
        return self.nisserver
    def return_status(self):
        return self.disabled
    def return_broadcast(self):
        return self.broadcast
    def return_data(self):
        if (self.disabled == 'TRUE'):
            return ""
        else:
            if (self.return_broadcast() == 'ON'):
                return " --enablenis --nisdomain " + self.nisdomain
            else:				
                return " --enablenis --nisdomain " + self.nisdomain + " --nisserver " + self.nisserver
			
class ldapData:
    def __init__(self, quit_cb=None):
        global ldapAuth
        global ldapServer
        global ldapDN
        self.ldapAuth = "YES"
        self.ldapServer = ''
        self.ldapDN = ''
        self.disabled = "TRUE"
    def set_auth(self, name):
        self.ldapAuth = name
    def set_server(self, name):
        self.ldapServer = name
    def set_DN(self, name):
        self.ldapDN = name
    def set_disabled(self):
        self.disabled = "TRUE"
    def set_enabled(self):
        self.disabled = "FALSE"
    def return_auth(self):
        return self.ldapAuth
    def return_server(self):
        return self.ldapServer
    def return_DN(self):
        return self.ldapDN
    def return_status(self):
        return self.disabled
    def return_data(self):
        if (self.disabled == 'TRUE'):
            return ""
        else:
            if (self.ldapAuth == 'YES'):
                return " --enableldap --enableldapauth --ldapserver " + self.ldapServer + " --ldapbasedn " + self.ldapDN
            else:
                return " --enableldap --ldapserver " + self.ldapServer + " --ldapbasedn " + self.ldapDN

class kerberosData:
    def __init__(self, quit_cb=None):
        global kerberosRealm
        global kerberosKDC
        global kerberosMaster
        self.kerberosRealm = " "
        self.kerberosKDC = " "
        self.kerberosMaster = " "
        self.disabled = "TRUE"		
    def set_realm(self, name):
        self.kerberosRealm = name
    def set_KDC(self, name):
        self.kerberosKDC = name
    def set_master(self, name):
        self.kerberosMaster = name
    def set_disabled(self):
        self.disabled = "TRUE"
    def set_enabled(self):
        self.disabled = "FALSE"
    def return_realm(self):
        return self.kerberosRealm
    def return_KDC(self):
        return self.kerberosKDC
    def return_master(self):
        return self.kerberosMaster
    def return_status(self):
        return self.disabled
    def return_data(self):
        if (self.disabled == 'TRUE'):
            return ""
        else:
            return " --enablekrb5 --krb5realm " + self.kerberosRealm + " --krb5kdc " + self.kerberosKDC + " --krb5adminserver " + self.kerberosMaster
            
class hesiodData:
    def __init__(self, quit_cb=None):
        global hesiodLHS
        global hesiodRHS
        self.hesiodLHS = " "
        self.hesiodRHS = " "
        self.disabled = "TRUE"		
    def set_LHS(self, name):
        self.hesiodLHS = name
    def set_RHS(self, name):
        self.hesiodRHS = name
    def set_disabled(self):
        self.disabled = "TRUE"
    def set_enabled(self):
        self.disabled = "FALSE"
    def return_LHS(self):
        return self.hesiodLHS
    def return_RHS(self):
        return self.hesiodRHS
    def return_status(self):
        return self.disabled
    def return_data(self):
        if (self.disabled == 'TRUE'):
            return ""
        else:
            return " --enablehesiod --hesiodlhs " + self.hesiodLHS + " --hesiodRHS " + self.hesiodRHS
        
class authWindow(GtkWindow):
    def getData(self):
        buf = ""
        buf = buf + self.myNisClass.return_data()
        buf = buf + self.myLDAPClass.return_data()
        buf = buf + self.myKerberosClass.return_data()
        buf = buf + self.myHesiodClass.return_data()
        return buf

    def okClicked(self, args):
        if (self.nisCheck.get_active()):
            self.myNisClass.set_domain(self.nisDomainEntry.get_text())
            self.myNisClass.set_server(self.nisServerEntry.get_text())

            if (self.nisBroadcastCheck.get_active()):
                self.myNisClass.set_broadcast("ON")
            else:
                self.myNisClass.set_broadcast("OFF")

        else:
            self.myNisClass.set_disabled()

        if (self.ldapCheck.get_active()):
            self.myLDAPClass.set_server(self.ldapServerEntry.get_text())
            self.myLDAPClass.set_DN(self.ldapDNEntry.get_text())
        else:
            self.myLDAPClass.set_disabled()


        if (self.kerberosCheck.get_active()):
            self.myKerberosClass.set_realm(self.kerberosRealmEntry.get_text())
            self.myKerberosClass.set_KDC(self.kerberosKDCEntry.get_text())
            self.myKerberosClass.set_master(self.kerberosMasterEntry.get_text())
        else:
            self.myKerberosClass.set_disabled()


        if (self.hesiodCheck.get_active()):
            self.myHesiodClass.set_LHS(self.hesiodLHSEntry.get_text())
            self.myHesiodClass.set_RHS(self.hesiodRHSEntry.get_text())
        else:
            self.myHesiodClass.set_disabled()

        self.destroy()

    def cancelClicked(self, args):
            self.myNisClass.set_disabled()
            self.myKerberosClass.set_disabled()
            self.destroy()

    def __init__(self, quit_cb=None):
        GtkWindow.__init__(self, WINDOW_TOPLEVEL)
        self.set_modal(TRUE)
        self.set_border_width(6)
        self.set_default_size(400, 100)		
        self.set_title("Advanced Authentication")

        self.connect("destroy", self.destroy)
	
        self.vbox = GtkVBox()
        self.add(self.vbox)
        
        self.myNisClass = nisData()
        self.myLDAPClass = ldapData()
        self.myKerberosClass = kerberosData()
        self.myHesiodClass = hesiodData()

        #----------NIS----------#
        self.nisFrame = GtkFrame("NIS Configuration")
        self.vbox.pack_start(self.nisFrame)

        self.nisCheck = GtkCheckButton("Enable NIS")

        self.nisDomainLabel = GtkLabel("NIS Domain:")

        self.nisDomainEntry = GtkEntry()
        self.nisDomainEntry.set_state(STATE_INSENSITIVE)	

        self.nisBroadcastCheck = GtkCheckButton("Use broadcast to find NIS server")
        self.nisBroadcastCheck.connect("clicked", self.BroadcastCheck_cb)

        self.nisServerLabel = GtkLabel("NIS Server:")
        self.nisServerEntry = GtkEntry()

        hbox1 = GtkHBox ()
        hbox1.pack_start (self.nisDomainLabel, FALSE)
        hbox1.pack_start (self.nisDomainEntry)

        hbox2 = GtkHBox ()
        hbox2.pack_start (self.nisServerLabel, FALSE)
        hbox2.pack_start (self.nisServerEntry)
        
        a = GtkAlignment (0, 0)
        a.add (self.nisBroadcastCheck)

        nistable = GtkTable (10, 4)
        nistable.attach (self.nisCheck, 0, 10, 0, 1)
        nistable.attach (hbox1, 2, 10, 1, 2)
        nistable.attach (a, 2, 10, 2, 3, xoptions = EXPAND|FILL)
        nistable.attach (hbox2, 4, 10, 3, 4)
        
        self.nisFrame.add(nistable)

        if (self.myNisClass.return_status() == "TRUE"):
            self.nisCheck.set_active(FALSE)
        else:
            self.nisDomainEntry.set_text(self.myNisClass.return_domain())

            if (self.myNisClass.return_broadcast() == 'OFF'):
                self.nisBroadcastCheck.set_active(FALSE)
                self.nisServerEntry.set_state(STATE_INSENSITIVE)
                self.nisServerEntry.set_text(self.myNisClass.return_server())
                self.nisBroadcastCheck.set_sensitive(TRUE)
                self.nisServerEntry.set_sensitive(TRUE)

            else:		
                self.nisBroadcastCheck.set_sensitive(TRUE)	
                self.nisBroadcastCheck.set_active(TRUE)
                self.nisServerEntry.set_state(STATE_INSENSITIVE)


        self.nisCheck.set_active(FALSE)				
        self.nisDomainLabel.set_sensitive(self.nisCheck.get_active())
        self.nisDomainEntry.set_sensitive(self.nisCheck.get_active())
        self.nisServerLabel.set_sensitive(self.nisCheck.get_active())
        self.nisServerEntry.set_sensitive(self.nisCheck.get_active())
        self.nisBroadcastCheck.set_sensitive(self.nisCheck.get_active())
        self.myNisClass.set_enabled()

        self.nisCheck.connect("toggled", self.enableNIS)

        #------------LDAP------------#

        self.ldapFrame = GtkFrame("LDAP Configuration")
        self.vbox.pack_start(self.ldapFrame)

        self.ldapTable = GtkTable(5, 3, FALSE)
        self.ldapFrame.add(self.ldapTable)

        self.ldapCheck = GtkCheckButton("Enable LDAP")
        self.ldapTable.attach(self.ldapCheck, 0, 1, 0, 1)

        self.ldapHbox = GtkHBox()
        self.ldapTable.attach(self.ldapHbox, 0, 1, 1, 2)

        self.ldapLabel1 = GtkLabel("Use LDAP authentication:")
        self.ldapLabel1.set_state(STATE_INSENSITIVE)	
        self.ldapHbox.pack_start(self.ldapLabel1)

        self.ldapRadio1 = GtkRadioButton(None, "Yes")
        self.ldapRadio1.set_state(STATE_INSENSITIVE)			
        self.ldapHbox.pack_start(self.ldapRadio1)
        self.ldapRadio1.connect("toggled", self.toggleLDAP)

        self.ldapRadio2 = GtkRadioButton(self.ldapRadio1, "No")
        self.ldapRadio2.set_state(STATE_INSENSITIVE)					
        self.ldapHbox.pack_start(self.ldapRadio2)
        self.ldapRadio2.connect("toggled", self.toggleLDAP)

        self.ldapLabel2 = GtkLabel("LDAP Server:")
        self.ldapLabel2.set_state(STATE_INSENSITIVE)	
        self.ldapTable.attach(self.ldapLabel2, 0, 1, 2, 3)

        self.ldapServerEntry = GtkEntry()
        self.ldapServerEntry.set_state(STATE_INSENSITIVE)	
        self.ldapTable.attach(self.ldapServerEntry, 1, 2, 2, 3)


        self.ldapLabel3 = GtkLabel("LDAP Distinguished Name (DN):")
        self.ldapLabel3.set_state(STATE_INSENSITIVE)	
        self.ldapTable.attach(self.ldapLabel3, 0, 1, 3, 4)

        self.ldapDNEntry = GtkEntry()
        self.ldapDNEntry.set_state(STATE_INSENSITIVE)	
        self.ldapTable.attach(self.ldapDNEntry, 1, 2, 3, 4)

        if (self.myLDAPClass.return_status() == "TRUE"):
            self.ldapCheck.set_active(FALSE)
        else:
            self.ldapCheck.set_active(TRUE)
            self.ldapServerEntry.set_text(self.myLDAPClass.return_server())
            self.ldapDNEntry.set_text(self.myLDAPClass.return_DN())

            self.ldapLabel1.set_sensitive(self.ldapCheck.get_active())		
            self.ldapRadio1.set_sensitive(self.ldapCheck.get_active())
            self.ldapRadio2.set_sensitive(self.ldapCheck.get_active())
            self.ldapLabel2.set_sensitive(self.ldapCheck.get_active())		
            self.ldapLabel3.set_sensitive(self.ldapCheck.get_active())
            self.ldapServerEntry.set_sensitive(self.ldapCheck.get_active())
            self.ldapDNEntry.set_sensitive(self.ldapCheck.get_active())			

        if (self.myLDAPClass.return_auth() == "YES"):
            self.ldapRadio1.set_active(TRUE)
        else:		
            self.ldapRadio2.set_active(TRUE)

        self.ldapCheck.connect("toggled", self.enableLDAP)


        #------------Kerberos-------------------#

        self.kerberosFrame = GtkFrame("Kerberos 5 Configuration")
        self.vbox.pack_start(self.kerberosFrame)

        self.kerberosTable = GtkTable(5, 3, FALSE)
        self.kerberosFrame.add(self.kerberosTable)

        self.kerberosCheck = GtkCheckButton("Enable Kerberos 5 Authentication")
        self.kerberosTable.attach(self.kerberosCheck, 0, 1, 0, 1)

        self.kerberosLabel1 = GtkLabel("Kerberos Realm:")
        self.kerberosLabel1.set_state(STATE_INSENSITIVE)	
        self.kerberosTable.attach(self.kerberosLabel1, 0, 1, 1, 2)

        self.kerberosRealmEntry = GtkEntry()
        self.kerberosRealmEntry.set_state(STATE_INSENSITIVE)	
        self.kerberosTable.attach(self.kerberosRealmEntry, 1, 2, 1, 2)

        self.kerberosLabel2 = GtkLabel("Kerberos Domain Controller (KDC):")
        self.kerberosLabel2.set_state(STATE_INSENSITIVE)	
        self.kerberosTable.attach(self.kerberosLabel2, 0, 1, 2, 3)

        self.kerberosKDCEntry = GtkEntry()
        self.kerberosKDCEntry.set_state(STATE_INSENSITIVE)
        self.kerberosTable.attach(self.kerberosKDCEntry, 1, 2, 2, 3)

        self.kerberosLabel3 = GtkLabel("Kerberos Master Server:")
        self.kerberosLabel3.set_state(STATE_INSENSITIVE)	
        self.kerberosTable.attach(self.kerberosLabel3, 0, 1, 3, 4)

        self.kerberosMasterEntry = GtkEntry()
        self.kerberosMasterEntry.set_state(STATE_INSENSITIVE)
        self.kerberosTable.attach(self.kerberosMasterEntry, 1, 2, 3, 4)

        if (self.myKerberosClass.return_status() == "TRUE"):
            self.kerberosCheck.set_active(FALSE)
        else:
            self.kerberosCheck.set_active(TRUE)
            self.kerberosRealmEntry.set_text(self.myKerberosClass.return_realm())
            self.kerberosKDCEntry.set_text(self.myKerberosClass.return_KDC())
            self.kerberosMasterEntry.set_text(self.myKerberosClass.return_master())
            self.kerberosRealmEntry.set_sensitive(TRUE)
            self.kerberosKDCEntry.set_sensitive(TRUE)
            self.kerberosMasterEntry.set_sensitive(TRUE)
            self.kerberosLabel1.set_sensitive(TRUE)
            self.kerberosLabel2.set_sensitive(TRUE)
            self.kerberosLabel3.set_sensitive(TRUE)

        self.kerberosCheck.connect("toggled", self.enableKerberos)

        #---------Hesiod--------#

        self.hesiodFrame = GtkFrame("Hesiod Configuration")
        self.vbox.pack_start(self.hesiodFrame)

        self.hesiodTable = GtkTable(5, 3, FALSE)
        self.hesiodFrame.add(self.hesiodTable)

        self.hesiodCheck = GtkCheckButton("Enable Hesiod Support")
        self.hesiodTable.attach(self.hesiodCheck, 0, 1, 0, 1)

        self.hesiodLabel1 = GtkLabel("Hesiod LHS : ")
        self.hesiodLabel1.set_state(STATE_INSENSITIVE)	
        self.hesiodTable.attach(self.hesiodLabel1, 0, 1, 1, 2)

        self.hesiodLHSEntry = GtkEntry()
        self.hesiodLHSEntry.set_state(STATE_INSENSITIVE)	
        self.hesiodTable.attach(self.hesiodLHSEntry, 1, 2, 1, 2)

        self.hesiodLabel2 = GtkLabel("Hesiod RHS : ")
        self.hesiodLabel2.set_state(STATE_INSENSITIVE)	
        self.hesiodTable.attach(self.hesiodLabel2, 0, 1, 2, 3)

        self.hesiodRHSEntry = GtkEntry()
        self.hesiodRHSEntry.set_state(STATE_INSENSITIVE)
        self.hesiodTable.attach(self.hesiodRHSEntry, 1, 2, 2, 3)

        if (self.myHesiodClass.return_status() == "TRUE"):
            self.hesiodCheck.set_active(FALSE)
        else:
            self.hesiodCheck.set_active(TRUE)
            self.hesiodLHSEntry.set_text(self.myHesiodClass.return_LHS())
            self.hesiodRHSEntry.set_text(self.myHesiodClass.return_RHS())
            self.hesiodLHSEntry.set_sensitive(TRUE)
            self.hesiodRHSEntry.set_sensitive(TRUE)
            self.hesiodLabel1.set_sensitive(TRUE)
            self.hesiodLabel2.set_sensitive(TRUE)

        self.hesiodCheck.connect("toggled", self.enableHesiod)

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

        #-------------END-------------------------------------------------#

    def enableNIS(self, args):
        self.nisDomainLabel.set_sensitive(self.nisCheck.get_active())
        self.nisDomainEntry.set_sensitive(self.nisCheck.get_active())
        self.nisServerLabel.set_sensitive(self.nisCheck.get_active())
        self.nisBroadcastCheck.set_sensitive(self.nisCheck.get_active())	
        self.nisServerEntry.set_sensitive(self.nisCheck.get_active())
        self.myNisClass.set_enabled()

    def BroadcastCheck_cb(self, args):
        if (self.nisBroadcastCheck.get_active() == 1):
            self.nisServerEntry.set_sensitive(FALSE)
            self.nisServerEntry.set_text("")
        elif (self.nisBroadcastCheck.get_active() == 0):
            self.nisServerEntry.set_sensitive(TRUE)

    def enableLDAP(self, args):
        self.ldapLabel1.set_sensitive(self.ldapCheck.get_active())		
        self.ldapRadio1.set_sensitive(self.ldapCheck.get_active())
        self.ldapRadio2.set_sensitive(self.ldapCheck.get_active())
        self.ldapLabel2.set_sensitive(self.ldapCheck.get_active())		
        self.ldapLabel3.set_sensitive(self.ldapCheck.get_active())
        self.ldapServerEntry.set_sensitive(self.ldapCheck.get_active())
        self.ldapDNEntry.set_sensitive(self.ldapCheck.get_active())				
        self.myLDAPClass.set_enabled()

    def enableKerberos(self, args):
        self.kerberosLabel1.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosLabel2.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosLabel3.set_sensitive(self.kerberosCheck.get_active())				

        self.kerberosRealmEntry.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosKDCEntry.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosMasterEntry.set_sensitive(self.kerberosCheck.get_active())				
        self.myKerberosClass.set_enabled()			

    def enableHesiod(self, args):
        self.hesiodLabel1.set_sensitive(self.hesiodCheck.get_active())		
        self.hesiodLabel2.set_sensitive(self.hesiodCheck.get_active())		
        self.hesiodLHSEntry.set_sensitive(self.hesiodCheck.get_active())
        self.hesiodRHSEntry.set_sensitive(self.hesiodCheck.get_active())	
        self.myHesiodClass.set_enabled()

    def toggleLDAP(self, args):
        if (self.ldapRadio1.get_active()):
            self.myLDAPClass.set_auth("YES")
        else:
            self.myLDAPClass.set_auth("No")

	
        
