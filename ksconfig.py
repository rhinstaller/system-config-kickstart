#!/usr/bin/env python

#Kickstart Configurator
#Copyright Red Hat, Inc. 2001
#Written by Brent Fox (bfox@redhat.com) and Tammy Fox (tfox@redhat.com)
#Created August 10, 2000 Brent Fox
#Last Modified: January 27, 2001 Tammy Fox

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




class counterClass:
	
	def setCounter(self, start):
		self.rowCount = start
	def increment(self):
		self.rowCount = self.rowCount + 1
	def decrement(self):
		self.rowCount = self.rowCount - 1
	def currentVal(self):
		return self.rowCount
		
class authWindow(GtkWindow):
	def __init__(self, quit_cb=None):
		GtkWindow.__init__(self, WINDOW_TOPLEVEL)
		self.set_border_width(6)
		self.set_default_size(400, 10)		
		self.set_title("Advanced Authentication")

		self.connect("destroy", self.destroy)
	
		self.vbox = GtkVBox()
		self.vbox.show()
		self.add(self.vbox)

	
		#----------NIS----------#
		self.nisFrame = GtkFrame("NIS Configuration")
		self.nisFrame.show()
		self.vbox.pack_start(self.nisFrame)

		self.nisTable = GtkTable(5, 3, FALSE)
		self.nisTable.show()
		self.nisFrame.add(self.nisTable)
	
		self.nisCheck = GtkCheckButton("Enable NIS")
		self.nisCheck.show()
		self.nisTable.attach(self.nisCheck, 0, 1, 0, 1)

		self.nisLabel1 = GtkLabel("NIS Domain:")
		self.nisLabel1.show()
		self.nisLabel1.set_state(STATE_INSENSITIVE)	
		self.nisTable.attach(self.nisLabel1, 0, 1, 1, 2)

		self.nisDomainEntry = GtkEntry()
		self.nisDomainEntry.show()
		self.nisDomainEntry.set_state(STATE_INSENSITIVE)	
		self.nisTable.attach(self.nisDomainEntry, 1, 2, 1, 2)
		
		self.nisLabel2 = GtkLabel("NIS Server:")
		self.nisLabel2.show()
		self.nisLabel2.set_state(STATE_INSENSITIVE)	
		self.nisTable.attach(self.nisLabel2, 0, 1, 2, 3)
	
		self.nisBroadcastCheck = GtkCheckButton("Broadcast")
		self.nisBroadcastCheck.show()
		self.nisBroadcastCheck.set_state(STATE_INSENSITIVE)
		self.nisBroadcastCheck.connect("clicked", self.disableBroadcast)
		self.nisTable.attach(self.nisBroadcastCheck, 0, 1, 3, 4)
	
		self.nisServerEntry = GtkEntry()
		self.nisServerEntry.show()
		self.nisServerEntry.set_state(STATE_INSENSITIVE)
		self.nisTable.attach(self.nisServerEntry, 1, 2, 3, 4)


		if (myNisClass.return_status() == "TRUE"):
			self.nisCheck.set_active(FALSE)
		else:
			self.nisDomainEntry.set_text(myNisClass.return_domain())

			if (myNisClass.return_broadcast() == 'OFF'):
				self.nisBroadcastCheck.set_active(FALSE)
				self.nisServerEntry.set_state(STATE_INSENSITIVE)
				self.nisServerEntry.set_text(myNisClass.return_server())
				self.nisBroadcastCheck.set_sensitive(TRUE)
				self.nisServerEntry.set_sensitive(TRUE)

			else:		
				self.nisBroadcastCheck.set_sensitive(TRUE)	
				self.nisBroadcastCheck.set_active(TRUE)
				self.nisServerEntry.set_state(STATE_INSENSITIVE)


			self.nisCheck.set_active(TRUE)				
			self.nisLabel1.set_sensitive(self.nisCheck.get_active())
			self.nisDomainEntry.set_sensitive(self.nisCheck.get_active())
			self.nisLabel2.set_sensitive(self.nisCheck.get_active())
			myNisClass.set_enabled()
	
		self.nisCheck.connect("toggled", self.enableNIS)


		#------------LDAP------------#

		self.ldapFrame = GtkFrame("LDAP Configuration")
		self.ldapFrame.show()
		self.vbox.pack_start(self.ldapFrame)

		self.ldapTable = GtkTable(5, 3, FALSE)
		self.ldapTable.show()
		self.ldapFrame.add(self.ldapTable)
	
		self.ldapCheck = GtkCheckButton("Enable LDAP")
		self.ldapCheck.show()
		self.ldapTable.attach(self.ldapCheck, 0, 1, 0, 1)

		self.ldapHbox = GtkHBox()
		self.ldapHbox.show()
		self.ldapTable.attach(self.ldapHbox, 0, 1, 1, 2)

		self.ldapLabel1 = GtkLabel("Use LDAP authentication:")
		self.ldapLabel1.show()
		self.ldapLabel1.set_state(STATE_INSENSITIVE)	
		self.ldapHbox.pack_start(self.ldapLabel1)

		self.ldapRadio1 = GtkRadioButton(None, "Yes")
		self.ldapRadio1.show()
		self.ldapRadio1.set_state(STATE_INSENSITIVE)			
		self.ldapHbox.pack_start(self.ldapRadio1)
		self.ldapRadio1.connect("toggled", self.toggleLDAP)

		self.ldapRadio2 = GtkRadioButton(self.ldapRadio1, "No")
		self.ldapRadio2.show()
		self.ldapRadio2.set_state(STATE_INSENSITIVE)					
		self.ldapHbox.pack_start(self.ldapRadio2)
		self.ldapRadio2.connect("toggled", self.toggleLDAP)
		
		self.ldapLabel2 = GtkLabel("LDAP Server:")
		self.ldapLabel2.show()
		self.ldapLabel2.set_state(STATE_INSENSITIVE)	
		self.ldapTable.attach(self.ldapLabel2, 0, 1, 2, 3)

		self.ldapServerEntry = GtkEntry()
		self.ldapServerEntry.show()
		self.ldapServerEntry.set_state(STATE_INSENSITIVE)	
		self.ldapTable.attach(self.ldapServerEntry, 1, 2, 2, 3)
		

		self.ldapLabel3 = GtkLabel("LDAP Distinguished Name (DN):")
		self.ldapLabel3.show()
		self.ldapLabel3.set_state(STATE_INSENSITIVE)	
		self.ldapTable.attach(self.ldapLabel3, 0, 1, 3, 4)

		self.ldapDNEntry = GtkEntry()
		self.ldapDNEntry.show()
		self.ldapDNEntry.set_state(STATE_INSENSITIVE)	
		self.ldapTable.attach(self.ldapDNEntry, 1, 2, 3, 4)

		if (myLDAPClass.return_status() == "TRUE"):
			self.ldapCheck.set_active(FALSE)
		else:
			self.ldapCheck.set_active(TRUE)
			self.ldapServerEntry.set_text(myLDAPClass.return_server())
			self.ldapDNEntry.set_text(myLDAPClass.return_DN())

			self.ldapLabel1.set_sensitive(self.ldapCheck.get_active())		
			self.ldapRadio1.set_sensitive(self.ldapCheck.get_active())
			self.ldapRadio2.set_sensitive(self.ldapCheck.get_active())
			self.ldapLabel2.set_sensitive(self.ldapCheck.get_active())		
			self.ldapLabel3.set_sensitive(self.ldapCheck.get_active())
			self.ldapServerEntry.set_sensitive(self.ldapCheck.get_active())
			self.ldapDNEntry.set_sensitive(self.ldapCheck.get_active())			
				
			if (myLDAPClass.return_auth() == "YES"):
				self.ldapRadio1.set_active(TRUE)
			else:		
				self.ldapRadio2.set_active(TRUE)

		self.ldapCheck.connect("toggled", self.enableLDAP)
		

		#------------Kerberos-------------------#

		self.kerberosFrame = GtkFrame("Kerberos 5 Configuration")
		self.kerberosFrame.show()
		self.vbox.pack_start(self.kerberosFrame)

		self.kerberosTable = GtkTable(5, 3, FALSE)
		self.kerberosTable.show()
		self.kerberosFrame.add(self.kerberosTable)
	
		self.kerberosCheck = GtkCheckButton("Enable Kerberos 5 Authentication")
		self.kerberosCheck.show()
		self.kerberosTable.attach(self.kerberosCheck, 0, 1, 0, 1)
	
		self.kerberosLabel1 = GtkLabel("Kerberos Realm:")
		self.kerberosLabel1.show()
		self.kerberosLabel1.set_state(STATE_INSENSITIVE)	
		self.kerberosTable.attach(self.kerberosLabel1, 0, 1, 1, 2)

		self.kerberosRealmEntry = GtkEntry()
		self.kerberosRealmEntry.show()
		self.kerberosRealmEntry.set_state(STATE_INSENSITIVE)	
		self.kerberosTable.attach(self.kerberosRealmEntry, 1, 2, 1, 2)

		self.kerberosLabel2 = GtkLabel("Kerberos Domain Controller (KDC):")
		self.kerberosLabel2.show()
		self.kerberosLabel2.set_state(STATE_INSENSITIVE)	
		self.kerberosTable.attach(self.kerberosLabel2, 0, 1, 2, 3)
	
		self.kerberosKDCEntry = GtkEntry()
		self.kerberosKDCEntry.show()
		self.kerberosKDCEntry.set_state(STATE_INSENSITIVE)
		self.kerberosTable.attach(self.kerberosKDCEntry, 1, 2, 2, 3)

		self.kerberosLabel3 = GtkLabel("Kerberos Master Server:")
		self.kerberosLabel3.show()
		self.kerberosLabel3.set_state(STATE_INSENSITIVE)	
		self.kerberosTable.attach(self.kerberosLabel3, 0, 1, 3, 4)
	
		self.kerberosMasterEntry = GtkEntry()
		self.kerberosMasterEntry.show()
		self.kerberosMasterEntry.set_state(STATE_INSENSITIVE)
		self.kerberosTable.attach(self.kerberosMasterEntry, 1, 2, 3, 4)

		if (myKerberosClass.return_status() == "TRUE"):
			self.kerberosCheck.set_active(FALSE)
		else:
			self.kerberosCheck.set_active(TRUE)
			self.kerberosRealmEntry.set_text(myKerberosClass.return_realm())
			self.kerberosKDCEntry.set_text(myKerberosClass.return_KDC())
			self.kerberosMasterEntry.set_text(myKerberosClass.return_master())
			self.kerberosRealmEntry.set_sensitive(TRUE)
			self.kerberosKDCEntry.set_sensitive(TRUE)
			self.kerberosMasterEntry.set_sensitive(TRUE)
			self.kerberosLabel1.set_sensitive(TRUE)
			self.kerberosLabel2.set_sensitive(TRUE)
			self.kerberosLabel3.set_sensitive(TRUE)

		self.kerberosCheck.connect("toggled", self.enableKerberos)

		#---------Hesiod--------#

		self.hesiodFrame = GtkFrame("Hesiod Configuration")
		self.hesiodFrame.show()
		self.vbox.pack_start(self.hesiodFrame)

		self.hesiodTable = GtkTable(5, 3, FALSE)
		self.hesiodTable.show()
		self.hesiodFrame.add(self.hesiodTable)
	
		self.hesiodCheck = GtkCheckButton("Enable Hesiod Support")
		self.hesiodCheck.show()
		self.hesiodTable.attach(self.hesiodCheck, 0, 1, 0, 1)
	
		self.hesiodLabel1 = GtkLabel("Hesiod LHS:")
		self.hesiodLabel1.show()
		self.hesiodLabel1.set_state(STATE_INSENSITIVE)	
		self.hesiodTable.attach(self.hesiodLabel1, 0, 1, 1, 2)

		self.hesiodLHSEntry = GtkEntry()
		self.hesiodLHSEntry.show()
		self.hesiodLHSEntry.set_state(STATE_INSENSITIVE)	
		self.hesiodTable.attach(self.hesiodLHSEntry, 1, 2, 1, 2)

		self.hesiodLabel2 = GtkLabel("Hesiod RHS:")
		self.hesiodLabel2.show()
		self.hesiodLabel2.set_state(STATE_INSENSITIVE)	
		self.hesiodTable.attach(self.hesiodLabel2, 0, 1, 2, 3)
	
		self.hesiodRHSEntry = GtkEntry()
		self.hesiodRHSEntry.show()
		self.hesiodRHSEntry.set_state(STATE_INSENSITIVE)
		self.hesiodTable.attach(self.hesiodRHSEntry, 1, 2, 2, 3)
		
		if (myHesiodClass.return_status() == "TRUE"):
			self.hesiodCheck.set_active(FALSE)
		else:
			self.hesiodCheck.set_active(TRUE)
			self.hesiodLHSEntry.set_text(myHesiodClass.return_LHS())
			self.hesiodRHSEntry.set_text(myHesiodClass.return_RHS())
			self.hesiodLHSEntry.set_sensitive(TRUE)
			self.hesiodRHSEntry.set_sensitive(TRUE)
			self.hesiodLabel1.set_sensitive(TRUE)
			self.hesiodLabel2.set_sensitive(TRUE)

		self.hesiodCheck.connect("toggled", self.enableHesiod)

		#----------Ok and Cancel Buttons for Authenication window--------#
		self.hbox = GtkHBox()
		self.hbox.show()
		self.vbox.pack_start(self.hbox)

		self.okButton = GtkButton("Ok")
		self.okButton.show()
		self.okButton.connect("clicked", self.okClicked)
		self.hbox.pack_start(self.okButton)
		
		self.cancelButton = GtkButton("Cancel")
		self.cancelButton.show()
		self.cancelButton.connect("clicked", self.cancelClicked)
		self.hbox.pack_start(self.cancelButton)

		self.show()

	def enableNIS(self, args):
		self.nisLabel1.set_sensitive(self.nisCheck.get_active())
		self.nisDomainEntry.set_sensitive(self.nisCheck.get_active())
		self.nisLabel2.set_sensitive(self.nisCheck.get_active())
		self.nisBroadcastCheck.set_sensitive(self.nisCheck.get_active())	
		self.nisServerEntry.set_sensitive(self.nisCheck.get_active())
		myNisClass.set_enabled()

	def disableBroadcast(self, args):
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
		myLDAPClass.set_enabled()

	def enableKerberos(self, args):
		self.kerberosLabel1.set_sensitive(self.kerberosCheck.get_active())
		self.kerberosLabel2.set_sensitive(self.kerberosCheck.get_active())
		self.kerberosLabel3.set_sensitive(self.kerberosCheck.get_active())				
		
		self.kerberosRealmEntry.set_sensitive(self.kerberosCheck.get_active())
		self.kerberosKDCEntry.set_sensitive(self.kerberosCheck.get_active())
		self.kerberosMasterEntry.set_sensitive(self.kerberosCheck.get_active())				
		myKerberosClass.set_enabled()			

	def enableHesiod(self, args):
		self.hesiodLabel1.set_sensitive(self.hesiodCheck.get_active())		
		self.hesiodLabel2.set_sensitive(self.hesiodCheck.get_active())		
		self.hesiodLHSEntry.set_sensitive(self.hesiodCheck.get_active())
		self.hesiodRHSEntry.set_sensitive(self.hesiodCheck.get_active())	
		myHesiodClass.set_enabled()

	def toggleLDAP(self, args):
		if (self.ldapRadio1.get_active()):
			myLDAPClass.set_auth("YES")
		else:
			myLDAPClass.set_auth("No")

	def okClicked(self, args):
		if (self.nisCheck.get_active()):
			myNisClass.set_domain(self.nisDomainEntry.get_text())
			myNisClass.set_server(self.nisServerEntry.get_text())
			
			if (self.nisBroadcastCheck.get_active()):
				myNisClass.set_broadcast("ON")
			else:
				myNisClass.set_broadcast("OFF")

		else:
			myNisClass.set_disabled()
			
		if (self.ldapCheck.get_active()):
			myLDAPClass.set_server(self.ldapServerEntry.get_text())
			myLDAPClass.set_DN(self.ldapDNEntry.get_text())
			

		else:
			myLDAPClass.set_disabled()


		if (self.kerberosCheck.get_active()):
			myKerberosClass.set_realm(self.kerberosRealmEntry.get_text())
			myKerberosClass.set_KDC(self.kerberosKDCEntry.get_text())
			myKerberosClass.set_master(self.kerberosMasterEntry.get_text())
			
		else:
			myKerberosClass.set_disabled()


		if (self.hesiodCheck.get_active()):
			myHesiodClass.set_LHS(self.hesiodLHSEntry.get_text())
			myHesiodClass.set_RHS(self.hesiodRHSEntry.get_text())
		else:
			myHesiodClass.set_disabled()
			
		self.destroy()

	def cancelClicked(self, args):
		myNisClass.set_disabled()
		myKerberosClass.set_disabled()
		self.destroy()
	

def destroy(args):
	window.destroy()
	mainquit()
	
def saveClicked(args):
        #show file dialog box#
	saveDialog.set_filename("ks.cfg")
	saveDialog.ok_button.connect("clicked", saveFile)
	saveDialog.cancel_button.connect("clicked", saveDialog.destroy)
	saveDialog.show()

def saveFile(args):
	filePath = saveDialog.get_filename()
	saveDialog.destroy()
	
	buf = "#Generated by Kickstart Configurator"

	buf = buf + "\n" + languageLookup(languageCombo.entry.get_text())
	buf = buf + "\n" + "keyboard " + keyboardCombo.entry.get_text()
	buf = buf + "\n" + mouseLookup(mouseCombo.entry.get_text())
	buf = buf + "\n" + timezoneLookup(timeCombo.entry.get_text())
	buf = buf + "\n" + "rootpw " + rootEntry.get_text()
	
	if sourceRadio1.get_active():
		buf = buf + "\n" + "cdrom"
	elif sourceRadio2.get_active():
		buf = buf + "\n" + "nfs"
		buf = buf + " --server " + serverEntry.get_text()
		buf = buf + " --dir " + dirEntry.get_text()
	elif sourceRadio3.get_active():
		buf = buf + "\n" + "url"
		buf = buf + " --url ftp://" + ftpEntry.get_text()
		buf = buf + ftpDirEntry.get_text()		
	elif sourceRadio4.get_active():
		buf = buf + "\n" + "harddrive"
		buf = buf + " --dir " + hdDirEntry.get_text()
		buf = buf + " --partition " + hdDevEntry.get_text()
		
	if networkRadio1.get_active():
		buf = buf + "\n" + "network --bootproto dhcp"
	elif networkRadio2.get_active():
		buf = buf + "\n" + "network --bootproto static"
		buf = buf + " --ip " 
		buf = buf + ipEntry1.get_text() + "."
		buf = buf + ipEntry2.get_text() + "."
		buf = buf + ipEntry3.get_text() + "."
		buf = buf + ipEntry4.get_text()
		buf = buf + " --netmask " 
		buf = buf + netmaskEntry1.get_text() + "."
		buf = buf + netmaskEntry2.get_text() + "."
		buf = buf + netmaskEntry3.get_text() + "."
		buf = buf + netmaskEntry4.get_text()
		buf = buf + " --gateway " 
		buf = buf + gatewayEntry1.get_text() + "."
		buf = buf + gatewayEntry2.get_text() + "."
		buf = buf + gatewayEntry3.get_text() + "."
		buf = buf + gatewayEntry4.get_text()
		buf = buf + " --nameserver " 
		buf = buf + dnsEntry1.get_text() + "."
		buf = buf + dnsEntry2.get_text() + "."
		buf = buf + dnsEntry3.get_text() + "."
		buf = buf + dnsEntry4.get_text()
	
	buf = buf + "\n" + "install"

	buf = buf + "\n" + "auth"
	
	if authCheck1.get_active():
		buf = buf + " --useshadow"
	
	if authCheck2.get_active():
		buf = buf + " --enablemd5"
		
	buf = buf + myNisClass.return_data()
	buf = buf + myLDAPClass.return_data()
	buf = buf + myKerberosClass.return_data()
	buf = buf + myHesiodClass.return_data()
		
	if mbrRadio1.get_active():
		buf = buf + "\n" + "zerombr yes"
	elif mbrRadio2.get_active():
		buf = buf + "\n" + "zerombr no"			
			
	if clearRadio1.get_active():
		buf = buf
	elif clearRadio2.get_active():
		buf = buf + "\n" + "clearpart --all"
	elif clearRadio3.get_active():
		buf = buf + "\n" + "clearpart --linux"
		
	rows = myCount.currentVal()
	
	for n in range(rows):
		line = "part"
		for i in range(4):
						
			if i == 0:
				mount = partClist.get_text(n, i)
				if mount == '':
					line = line
				else:
					line = line + " " + mount
			elif i == 1:
				fsType = partClist.get_text(n, i)
				if fsType == 'Linux Swap':
					line = line + " swap"
				elif fsType == 'ext2':
					line = line + " "
				else:
					line = line + " " + fsType
			elif i == 2:
				size = partClist.get_text(n, i)
				line = line + " --size " + size
			elif i == 3:
				grow = partClist.get_text(n, i)
				if grow == 'Yes':
					line = line + " --grow"
				else:
					line = line

		buf = buf + "\n" + line

	if liloRadio1.get_active():
		buf = buf + "\n" + "lilo --location mbr"
	elif liloRadio2.get_active():
		buf = buf + "\n" + "lilo --location none"


	buf = buf + "\n" + "%packages"
	
	if packageRadio1.get_active():
		buf = buf + "\n" + "@Server"
	elif packageRadio2.get_active():
		buf = buf + "\n" + "@Workstation"
	elif packageRadio4.get_active():
		buf = buf + "\n" + "@Everything"

	ksFile = open(filePath, "w")
	ksFile.write(buf)
	ksFile.close()

def installTypeLookup(args):
	if args == 'Graphical':
		return ""
	elif args == 'Text':
		return "skipx"	

def languageLookup(args):
	if args == 'Czech':
		return "lang cs_CZ"
	if args == 'English':
		return "lang en_US"
	if args == 'French':
		return "lang fr_FR"
	if args == 'German':
		return "lang de_DE"
	if args == 'Hungarian':
		return "lang hu_HU"
	if args == 'Icelandic':
		return "lang is_IS"
	if args == 'Italian':
		return "lang it_IT"
	if args == 'Norwegian':
		return "lang no_NO"
	if args == 'Romanian':
		return "lang ro_RO"
	if args == 'Russian':
		return "lang ru_RU.K0I8-R"
	if args == 'Serbian':		
		return "lang sr_YU"
	if args == 'Slovak':		
		return "lang sk_SK"
	if args == 'Slovenian':
		return "lang sl_SI"
	if args == 'Spanish':
		return "lang es_ES"
	if args == 'Swedish':
		return "lang sv_SV"
	if args == 'Turkish':
		return "lang tr_TR"
	if args == 'Ukrainian':
		return "lang uk_UA.KOI8-U"

	
def keyboardLookup(args):
	if args == 'us':
		return "keyboard us"
		
def mouseLookup(args):
	if args:	
		return "mouse generic3ps/2"

def timezoneLookup(args):
	if args == 'US Eastern':
		return "timezone --utc US/Eastern"
	elif args == 'US Central':
		return "timezone --utc US/Central"
	elif args == 'US Mountain':
		return "timezone --utc US/Mountain"
	elif args == 'US Pacific':
		return "timezone --utc US/Pacific"

def enableNFS(args):
	serverEntry.set_sensitive(sourceRadio2.get_active())
	dirEntry.set_sensitive(sourceRadio2.get_active())

def disableNFS(args):
	serverEntry.set_state(STATE_INSENSITIVE)
	dirEntry.set_state(STATE_INSENSITIVE)

def enableFTP(args):
	ftpEntry.set_sensitive(sourceRadio3.get_active())
	ftpDirEntry.set_sensitive(sourceRadio3.get_active())

def disableFTP(args):
	ftpEntry.set_state(STATE_INSENSITIVE)

def enableHD(args):
	hdDevEntry.set_sensitive(sourceRadio4.get_active())
	hdDirEntry.set_sensitive(sourceRadio4.get_active())

def disableHD(args):
	hdDevEntry.set_state(STATE_INSENSITIVE)
	hdDirEntry.set_state(STATE_INSENSITIVE)

def toggleDHCP(args):
	ipEntry1.set_state(STATE_INSENSITIVE)
	ipEntry2.set_state(STATE_INSENSITIVE)	
	ipEntry3.set_state(STATE_INSENSITIVE)	
	ipEntry4.set_state(STATE_INSENSITIVE)		
	netmaskEntry1.set_state(STATE_INSENSITIVE)
	netmaskEntry2.set_state(STATE_INSENSITIVE)	
	netmaskEntry3.set_state(STATE_INSENSITIVE)	
	netmaskEntry4.set_state(STATE_INSENSITIVE)		
	gatewayEntry1.set_state(STATE_INSENSITIVE)
	gatewayEntry2.set_state(STATE_INSENSITIVE)	
	gatewayEntry3.set_state(STATE_INSENSITIVE)	
	gatewayEntry4.set_state(STATE_INSENSITIVE)		
	dnsEntry1.set_state(STATE_INSENSITIVE)
	dnsEntry2.set_state(STATE_INSENSITIVE)	
	dnsEntry3.set_state(STATE_INSENSITIVE)	
	dnsEntry4.set_state(STATE_INSENSITIVE)		

def toggleIP(args):
	ipEntry1.set_sensitive(networkRadio2.get_active())
	ipEntry2.set_sensitive(networkRadio2.get_active())
	ipEntry3.set_sensitive(networkRadio2.get_active())
	ipEntry4.set_sensitive(networkRadio2.get_active())
	netmaskEntry1.set_sensitive(networkRadio2.get_active())
	netmaskEntry2.set_sensitive(networkRadio2.get_active())
	netmaskEntry3.set_sensitive(networkRadio2.get_active())
	netmaskEntry4.set_sensitive(networkRadio2.get_active())
	gatewayEntry1.set_sensitive(networkRadio2.get_active())
	gatewayEntry2.set_sensitive(networkRadio2.get_active())
	gatewayEntry3.set_sensitive(networkRadio2.get_active())
	gatewayEntry4.set_sensitive(networkRadio2.get_active())
	dnsEntry1.set_sensitive(networkRadio2.get_active())
	dnsEntry2.set_sensitive(networkRadio2.get_active())
	dnsEntry3.set_sensitive(networkRadio2.get_active())
	dnsEntry4.set_sensitive(networkRadio2.get_active())
	
def toggleNoNetwork(args):
	ipEntry1.set_state(STATE_INSENSITIVE)
	ipEntry2.set_state(STATE_INSENSITIVE)	
	ipEntry3.set_state(STATE_INSENSITIVE)	
	ipEntry4.set_state(STATE_INSENSITIVE)		
	netmaskEntry1.set_state(STATE_INSENSITIVE)
	netmaskEntry2.set_state(STATE_INSENSITIVE)	
	netmaskEntry3.set_state(STATE_INSENSITIVE)	
	netmaskEntry4.set_state(STATE_INSENSITIVE)		
	gatewayEntry1.set_state(STATE_INSENSITIVE)
	gatewayEntry2.set_state(STATE_INSENSITIVE)	
	gatewayEntry3.set_state(STATE_INSENSITIVE)	
	gatewayEntry4.set_state(STATE_INSENSITIVE)		
	dnsEntry1.set_state(STATE_INSENSITIVE)
	dnsEntry2.set_state(STATE_INSENSITIVE)	
	dnsEntry3.set_state(STATE_INSENSITIVE)	
	dnsEntry4.set_state(STATE_INSENSITIVE)		

#start of main#
window = GtkWindow()
window.connect("destroy", destroy)
window.set_title('Kickstart Configurator')
window.set_border_width(6)
window.set_default_size(480, 200)

saveDialog = GtkFileSelection("Save File")

vbox1 = GtkVBox()
vbox1.show()
window.add(vbox1)

#number of partitions#
myCount = counterClass()
myCount.setCounter(3)

myNisClass = nisData()
myLDAPClass = ldapData()
myKerberosClass = kerberosData()
myHesiodClass = hesiodData()

#---------------Install Type-----------#

frame1 = GtkFrame("Basic configuration")
frame1.set_label("Basic configuration")
frame1.show()
vbox1.pack_start(frame1)

installVbox = GtkVBox()
installVbox.show()
frame1.add(installVbox)


table1 = GtkTable(7, 2, FALSE)
table1.show()
installVbox.pack_start(table1)

#---------------Language----------------#
languageLabel = GtkLabel("Language:")
table1.attach(languageLabel, 0, 1, 2, 3)
languageLabel.show()

languageCombo = GtkCombo()
table1.attach(languageCombo, 1, 2, 2, 3)
languageCombo.show()

list_items = [ "Czech", "English", "French", "German", "Hungarian", "Icelandic", 
			"Italian", "Norwegian", "Romanian", "Russian", "Serbian", "Slovak",
			"Slovenian", "Spanish", "Swedish", "Turkish", "Ukrainian" ]

languageCombo.set_popdown_strings(list_items)
languageCombo.list.select_item(1)
languageCombo.entry.set_editable(FALSE)


#---------------Keyboard------------------#
keyboardLabel = GtkLabel("Keyboard:")
table1.attach(keyboardLabel, 0, 1, 3, 4)
keyboardLabel.show()

keyboardCombo = GtkCombo()
table1.attach(keyboardCombo, 1, 2, 3, 4)
keyboardCombo.show()

list_items = [ "azerty", "be-latin1", "be2-latin1", "fr-latin0", "fr-pc", "fr", 
			"wangbe", "ANSI-dvorak", "dvorak-1", "dvorak-r", "dvorak", "pc-dvorak-latin1",
			"tr_f-latin5", "trf", "bg", "cf", "cz-lat2-prog", "cz-lat2", "defkeymap",
			"defkeymap_V1.0", "dk-latin1", "dk.emacs", "emacs2", "es", "fi-latin1", "fi",
			"gr-pc", "gr", "hebrew", "hu101", "is-latin", "it-ibm", "it", "it2", "jp106",
			"la-latin1", "lt", "lt.l4", "nl", "no-latin1", "no", "pc110", "pl", "pt-latin1",
			"pt-old", "ro", "ru-cp1251", "ru-ms", "ru-yawerty", "ru", "ru1", "ru2", "ru_win",
			"se-latin1", "sk-prog-qwerty", "sk-prog", "sk-qwerty", "tr_q-latin5", "tralt",
			"trf", "trq", "ua", "uk", "us", "croat", "cz-us-qwerty", "de-latin1-nodeadkeys",
			"de-latin1", "de", "fr_CH-latin1", "fr_CH", "hu", "sg-latin1-lk450",
			"sg-latin1", "sg", "sk-prog-qwertz", "sk-qwertz", "slovene" ]

keyboardCombo.set_popdown_strings(list_items)
keyboardCombo.list.select_item(63)
keyboardCombo.entry.set_editable(FALSE)


#-------------------Mouse----------------#
mouseLabel = GtkLabel("Mouse:")
table1.attach(mouseLabel, 0, 1, 4, 5)
mouseLabel.show()

mouseCombo = GtkCombo()
table1.attach(mouseCombo, 1, 2, 4, 5)
mouseCombo.show()

list_items = [ "Generic - 2 Button Mouse (serial)", "Generic - 2 Button Mouse (PS/2)",
			"Logitech - MouseMan/FirstMouse (serial)", "Logitech - MouseMan/FirstMouse (PS/2)" ]			

mouseCombo.set_popdown_strings(list_items)
mouseCombo.list.select_item(1)
mouseCombo.entry.set_editable(FALSE)

#-------------------Time Zone----------------#
timeLabel = GtkLabel("Time Zone:")
table1.attach(timeLabel, 0, 1, 5, 6)
timeLabel.show()

timeCombo = GtkCombo()
table1.attach(timeCombo, 1, 2, 5, 6)
timeCombo.show()

list_items = [ "US Eastern", "US Central", "US Mountain", "US Pacific" ]			

timeCombo.set_popdown_strings(list_items)
timeCombo.list.select_item(0)
timeCombo.entry.set_editable(FALSE)

#-------------------Root Password----------------#
rootLabel = GtkLabel("Root Password:")
table1.attach(rootLabel, 0, 1, 6, 7)
rootLabel.show()

rootEntry = GtkEntry()
table1.attach(rootEntry, 1, 2, 6, 7)
rootEntry.show()


#------------------LILO--------------------------#
liloHbox = GtkHBox()
liloHbox.show()
installVbox.pack_start(liloHbox)


liloLabel = GtkLabel("LILO:")
liloLabel.show()
liloHbox.pack_start(liloLabel)

liloRadio1 = GtkRadioButton(None, "MBR")
liloRadio1.show()
liloHbox.pack_start(liloRadio1)

liloRadio2 = GtkRadioButton(liloRadio1, "None")
liloRadio2.show()
liloHbox.pack_start(liloRadio2)

#------------------Authentication--------------------------#
authHbox = GtkHBox()
authHbox.show()
installVbox.pack_start(authHbox)


authLabel = GtkLabel("Authentication:")
authLabel.show()
authHbox.pack_start(authLabel)

authCheck1 = GtkCheckButton("Use shadow passwords")
authCheck1.show()
authHbox.pack_start(authCheck1)

authCheck2 = GtkCheckButton("Use MD5")
authCheck2.show()
authHbox.pack_start(authCheck2)

authButton = GtkButton("More...")
authButton.show()
authButton.connect("clicked", authWindow)
authHbox.pack_start(authButton)

#-------------------Install Source----------------#
frame2 = GtkFrame("Installation Source")
frame2.set_label("Installation Source")
frame2.show()
vbox1.pack_start(frame2)

installVbox = GtkVBox()
installVbox.show()
frame2.add(installVbox)

installHbox = GtkHBox()
installHbox.show()
installVbox.pack_start(installHbox)


sourceLabel = GtkLabel("Installation Source:")
sourceLabel.show()
installHbox.pack_start(sourceLabel)

sourceRadio1 = GtkRadioButton(None, "CD-ROM")
sourceRadio1.show()
installHbox.pack_start(sourceRadio1)
sourceRadio1.connect("toggled", disableNFS)
sourceRadio1.connect("toggled", disableFTP)
sourceRadio1.connect("toggled", disableHD)

sourceRadio2 = GtkRadioButton(sourceRadio1, "NFS")
sourceRadio2.show()
installHbox.pack_start(sourceRadio2)
sourceRadio2.connect("toggled", enableNFS)
sourceRadio2.connect("toggled", disableFTP)
sourceRadio2.connect("toggled", disableHD)

sourceRadio3 = GtkRadioButton(sourceRadio1, "FTP")
sourceRadio3.show()
installHbox.pack_start(sourceRadio3)
sourceRadio3.connect("toggled", enableFTP)
sourceRadio3.connect("toggled", disableNFS)
sourceRadio3.connect("toggled", disableHD)


sourceRadio4 = GtkRadioButton(sourceRadio1, "Hard drive")
sourceRadio4.show()
installHbox.pack_start(sourceRadio4)
sourceRadio4.connect("toggled", enableHD)
sourceRadio4.connect("toggled", disableNFS)
sourceRadio4.connect("toggled", disableFTP)


#-------------------NFS Options----------------#
installTable = GtkTable(3, 2, FALSE)
installTable.show()
installVbox.pack_start(installTable)

serverLabel = GtkLabel("NFS Server:")
serverLabel.show()
installTable.attach(serverLabel, 0, 1, 0, 1)

serverEntry = GtkEntry()
serverEntry.show()
installTable.attach(serverEntry, 1, 2, 0, 1)

serverEntry.set_state(STATE_INSENSITIVE)

dirLabel = GtkLabel("NFS Directory:")
dirLabel.show()
installTable.attach(dirLabel, 0, 1, 1, 2)

dirEntry = GtkEntry()
dirEntry.show()
installTable.attach(dirEntry, 1, 2, 1, 2)

dirEntry.set_state(STATE_INSENSITIVE)



#-------------------FTP Options----------------#
#ftpHbox = GtkHBox()
#ftpHbox.show()
#installVbox.pack_start(ftpHbox)

ftpLabel = GtkLabel("FTP Server:")
ftpLabel.show()
installTable.attach(ftpLabel, 0, 1, 2, 3)

ftpEntry = GtkEntry()
ftpEntry.show()
installTable.attach(ftpEntry, 1, 2, 2, 3)

ftpLabel2 = GtkLabel("FTP Directory:")
ftpLabel2.show()
installTable.attach(ftpLabel2, 0, 1, 3, 4)

ftpDirEntry = GtkEntry()
ftpDirEntry.show()
installTable.attach(ftpDirEntry, 1, 2, 3, 4)


ftpEntry.set_state(STATE_INSENSITIVE)
ftpDirEntry.set_state(STATE_INSENSITIVE)

#-------------------Hard Drive Options----------------#
hdHbox = GtkHBox()
hdHbox.show()
installVbox.pack_start(hdHbox)

hdLabel1 = GtkLabel("Hard Drive partition:")
hdLabel1.show()
hdHbox.pack_start(hdLabel1)
#ftpHbox.pack_start(ftpLabel)
#installTable.attach(hdLabel, 0, 1, 2, 3)

#installTable.attach(hdHbox, 1, 2, 2, 3)

hdDevEntry = GtkEntry()
hdDevEntry.set_usize(35, 20)
hdDevEntry.set_max_length(8)
hdDevEntry.show()
hdHbox.pack_start(hdDevEntry)
#ftpHbox.pack_start(ftpEntry)

hdLabel2 = GtkLabel("Directory:")
hdLabel2.show()
hdHbox.pack_start(hdLabel2)

hdDirEntry = GtkEntry()
hdDirEntry.show()
hdHbox.pack_start(hdDirEntry)


hdDevEntry.set_state(STATE_INSENSITIVE)
hdDirEntry.set_state(STATE_INSENSITIVE)


#-------------------Network settings----------------#
frame3 = GtkFrame("Network Configuration")
frame3.set_label("Network Configuration")
frame3.show()
vbox1.pack_start(frame3)

networkVbox = GtkVBox()
networkVbox.show()
frame3.add(networkVbox)


networkHbox = GtkHBox()
networkHbox.show()
networkVbox.pack_start(networkHbox)

networkLabel = GtkLabel("Network Configuration:")
networkLabel.show()
networkHbox.pack_start(networkLabel)

networkRadio1 = GtkRadioButton(None, "DHCP")
networkRadio1.show()
networkHbox.pack_start(networkRadio1)
networkRadio1.connect("toggled", toggleDHCP)

networkRadio2 = GtkRadioButton(networkRadio1, "Static IP")
networkRadio2.show()
networkHbox.pack_start(networkRadio2)
networkRadio2.connect("toggled", toggleIP)

networkRadio3 = GtkRadioButton(networkRadio1, "None")
networkRadio3.show()
networkHbox.pack_start(networkRadio3)
networkRadio3.connect("toggled", toggleNoNetwork)


table2 = GtkTable(4, 2, FALSE)
table2.show()
networkVbox.pack_start(table2) 

#---ip---#
ipHBox = GtkHBox()
ipHBox.show()

ipLabel = GtkLabel("IP Address:")
ipLabel.show()
table2.attach(ipLabel, 0, 1, 0, 1)
table2.attach(ipHBox, 1, 2, 0, 1)


ipDot1 = GtkLabel(".")
ipDot1.show()
ipDot2 = GtkLabel(".")
ipDot2.show()
ipDot3 = GtkLabel(".")
ipDot3.show()



ipEntry1 = GtkEntry()
ipEntry1.set_max_length(3)
ipEntry1.set_usize(15, 20)
ipHBox.pack_start(ipEntry1)
ipEntry1.set_state(STATE_INSENSITIVE)
ipEntry1.show()


ipHBox.pack_start(ipDot1)

ipEntry2 = GtkEntry(3)
ipEntry2.set_max_length(3)
ipEntry2.set_usize(15, 20)
ipHBox.pack_start(ipEntry2)
ipEntry2.set_state(STATE_INSENSITIVE)
ipEntry2.show()

ipHBox.pack_start(ipDot2)

ipEntry3 = GtkEntry()
ipEntry3.set_max_length(3)
ipEntry3.set_usize(15, 20)
ipHBox.pack_start(ipEntry3)
ipEntry3.set_state(STATE_INSENSITIVE)
ipEntry3.show()

ipHBox.pack_start(ipDot3)

ipEntry4 = GtkEntry()
ipEntry4.set_max_length(3)
ipEntry4.set_usize(15, 20)
ipHBox.pack_start(ipEntry4)
ipEntry4.set_state(STATE_INSENSITIVE)
ipEntry4.show()



#---netmask---#
netmaskHBox = GtkHBox()
netmaskHBox.show()

netmaskLabel = GtkLabel("Netmask:")
netmaskLabel.show()
table2.attach(netmaskLabel, 0, 1, 1, 2)
table2.attach(netmaskHBox, 1, 2, 1, 2)


netmaskDot1 = GtkLabel(".")
netmaskDot1.show()
netmaskDot2 = GtkLabel(".")
netmaskDot2.show()
netmaskDot3 = GtkLabel(".")
netmaskDot3.show()

netmaskEntry1 = GtkEntry()
netmaskEntry1.set_max_length(3)
netmaskEntry1.set_usize(15, 20)
netmaskHBox.pack_start(netmaskEntry1)
netmaskEntry1.set_state(STATE_INSENSITIVE)
netmaskEntry1.show()


netmaskHBox.pack_start(netmaskDot1)

netmaskEntry2 = GtkEntry(3)
netmaskEntry2.set_max_length(3)
netmaskEntry2.set_usize(15, 20)
netmaskHBox.pack_start(netmaskEntry2)
netmaskEntry2.set_state(STATE_INSENSITIVE)
netmaskEntry2.show()

netmaskHBox.pack_start(netmaskDot2)

netmaskEntry3 = GtkEntry()
netmaskEntry3.set_max_length(3)
netmaskEntry3.set_usize(15, 20)
netmaskHBox.pack_start(netmaskEntry3)
netmaskEntry3.set_state(STATE_INSENSITIVE)
netmaskEntry3.show()

netmaskHBox.pack_start(netmaskDot3)

netmaskEntry4 = GtkEntry()
netmaskEntry4.set_max_length(3)
netmaskEntry4.set_usize(15, 20)
netmaskHBox.pack_start(netmaskEntry4)
netmaskEntry4.set_state(STATE_INSENSITIVE)
netmaskEntry4.show()

#---gateway---#
gatewayHBox = GtkHBox()
gatewayHBox.show()

gatewayLabel = GtkLabel("Gateway:")
gatewayLabel.show()
table2.attach(gatewayLabel, 0, 1, 2, 3)
table2.attach(gatewayHBox, 1, 2, 2, 3)


gatewayDot1 = GtkLabel(".")
gatewayDot1.show()
gatewayDot2 = GtkLabel(".")
gatewayDot2.show()
gatewayDot3 = GtkLabel(".")
gatewayDot3.show()

gatewayEntry1 = GtkEntry()
gatewayEntry1.set_max_length(3)
gatewayEntry1.set_usize(15, 20)
gatewayHBox.pack_start(gatewayEntry1)
gatewayEntry1.set_state(STATE_INSENSITIVE)
gatewayEntry1.show()


gatewayHBox.pack_start(gatewayDot1)

gatewayEntry2 = GtkEntry(3)
gatewayEntry2.set_max_length(3)
gatewayEntry2.set_usize(15, 20)
gatewayHBox.pack_start(gatewayEntry2)
gatewayEntry2.set_state(STATE_INSENSITIVE)
gatewayEntry2.show()

gatewayHBox.pack_start(gatewayDot2)

gatewayEntry3 = GtkEntry()
gatewayEntry3.set_max_length(3)
gatewayEntry3.set_usize(15, 20)
gatewayHBox.pack_start(gatewayEntry3)
gatewayEntry3.set_state(STATE_INSENSITIVE)
gatewayEntry3.show()

gatewayHBox.pack_start(gatewayDot3)

gatewayEntry4 = GtkEntry()
gatewayEntry4.set_max_length(3)
gatewayEntry4.set_usize(15, 20)
gatewayHBox.pack_start(gatewayEntry4)
gatewayEntry4.set_state(STATE_INSENSITIVE)
gatewayEntry4.show()



#---Nameserver---#
dnsHBox = GtkHBox()
dnsHBox.show()

dnsLabel = GtkLabel("Nameserver:")
dnsLabel.show()
table2.attach(dnsLabel, 0, 1, 3, 4)
table2.attach(dnsHBox, 1, 2, 3, 4)


dnsDot1 = GtkLabel(".")
dnsDot1.show()
dnsDot2 = GtkLabel(".")
dnsDot2.show()
dnsDot3 = GtkLabel(".")
dnsDot3.show()



dnsEntry1 = GtkEntry()
dnsEntry1.set_max_length(3)
dnsEntry1.set_usize(15, 20)
dnsHBox.pack_start(dnsEntry1)
dnsEntry1.set_state(STATE_INSENSITIVE)
dnsEntry1.show()


dnsHBox.pack_start(dnsDot1)

dnsEntry2 = GtkEntry(3)
dnsEntry2.set_max_length(3)
dnsEntry2.set_usize(15, 20)
dnsHBox.pack_start(dnsEntry2)
dnsEntry2.set_state(STATE_INSENSITIVE)
dnsEntry2.show()

dnsHBox.pack_start(dnsDot2)

dnsEntry3 = GtkEntry()
dnsEntry3.set_max_length(3)
dnsEntry3.set_usize(15, 20)
dnsHBox.pack_start(dnsEntry3)
dnsEntry3.set_state(STATE_INSENSITIVE)
dnsEntry3.show()

dnsHBox.pack_start(dnsDot3)

dnsEntry4 = GtkEntry()
dnsEntry4.set_max_length(3)
dnsEntry4.set_usize(15, 20)
dnsHBox.pack_start(dnsEntry4)
dnsEntry4.set_state(STATE_INSENSITIVE)
dnsEntry4.show()

#-----------Partition Information---------------#
frame4 = GtkFrame("Partition Information")
frame4.set_label("Partition Information")
frame4.show()
vbox1.pack_start(frame4)

partVbox = GtkVBox()
partVbox.show()
frame4.add(partVbox)


mbrHbox = GtkHBox()
mbrHbox.show()
partVbox.pack_start(mbrHbox)

mbrLabel = GtkLabel("Clear Master Boot Record:")
mbrLabel.show()
mbrHbox.pack_start(mbrLabel)

mbrRadio1 = GtkRadioButton(None, "Yes")
mbrRadio1.show()
mbrHbox.pack_start(mbrRadio1)

mbrRadio2 = GtkRadioButton(mbrRadio1, "No")
mbrRadio2.show()
mbrHbox.pack_start(mbrRadio2)


clearHbox = GtkHBox()
clearHbox.show()
partVbox.pack_start(clearHbox)

clearLabel = GtkLabel("Remove Existing Partitions:")
clearLabel.show()
clearHbox.pack_start(clearLabel)

clearRadio1 = GtkRadioButton(None, "None")
clearRadio1.show()
clearHbox.pack_start(clearRadio1)

clearRadio2 = GtkRadioButton(clearRadio1, "All")
clearRadio2.show()
clearHbox.pack_start(clearRadio2)

clearRadio3 = GtkRadioButton(clearRadio1, "Linux")
clearRadio3.show()
clearHbox.pack_start(clearRadio3)

#---Partition table clist---#
titles = ["Mount Point", "Type", "Size (M)", "Growable"]

partClist = GtkCList(4, titles)
partClist.show()
partVbox.pack_start(partClist)

partClist.set_column_width(0, 150)
partClist.set_column_width(1, 150)
partClist.set_column_width(2, 50)
partClist.set_column_width(3, 20)

s = [0]

def delPartition(_button, partClist=partClist, selected=s, myCount=myCount):
	myCount.decrement()
	partClist.remove(selected[0])
	editButton.set_state(STATE_INSENSITIVE)
	delButton.set_state(STATE_INSENSITIVE)

def select_clist(_clist, r, c, event, selected=s):
	selected[0] = r
	editButton.set_sensitive(TRUE)
	delButton.set_sensitive(TRUE)

def unselect_clist(_clist, r, c, event, selected=s):
	editButton.set_state(STATE_INSENSITIVE)
	delButton.set_state(STATE_INSENSITIVE)

def addPartition(args):
	
	addWindow = GtkWindow()
#	addWindow.connect("destroy", destroyPopup)
	addWindow.connect("delete_event", deleteEvent)
	addWindow.set_title('Add Partition Entry')
	addWindow.set_border_width(6)
	addWindow.set_default_size(100, 50)

	addTable = GtkTable(5, 2, FALSE)
	addTable.show()
	addWindow.add(addTable)

	addLabel1 = GtkLabel("Mount Point:")
	addLabel1.show()
	addTable.attach(addLabel1, 0, 1, 0, 1)
	
	mpCombo = GtkCombo()
	addTable.attach(mpCombo, 1, 2, 0, 1)
	mpCombo.show()	
	list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
	mpCombo.set_popdown_strings(list_items)
#	mpCombo.entry.set_text("")
	mpCombo.entry.set_editable(TRUE)

	addLabel2 = GtkLabel("Filesystem Type:")
	addLabel2.show()
	addTable.attach(addLabel2, 0, 1, 1, 2)

	fsCombo = GtkCombo()
	addTable.attach(fsCombo, 1, 2, 1, 2)
	fsCombo.show()	
	list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
	fsCombo.set_popdown_strings(list_items)
	fsCombo.entry.set_text("")
	fsCombo.entry.set_editable(TRUE)
	
	addLabel3 = GtkLabel("Size (M):")
	addLabel3.show()
	addTable.attach(addLabel3, 0, 1, 2, 3)

	sizeEntry = GtkEntry()
	addTable.attach(sizeEntry, 1, 2, 2, 3)
	sizeEntry.show()	

	addLabel4 = GtkLabel("Growable:")
	addLabel4.show()
	addTable.attach(addLabel4, 0, 1, 3, 4)

	growCombo = GtkCombo()
	addTable.attach(growCombo, 1, 2, 3, 4)
	growCombo.show()	
	list_items = [ "No", "Yes" ]			
	growCombo.set_popdown_strings(list_items)
	growCombo.list.select_item(0)
	growCombo.entry.set_editable(FALSE)


	def addEntry(args, addWindow=addWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, myCount=myCount):
		a = mpCombo.entry.get_text()
		b = fsCombo.entry.get_text()
		c = sizeEntry.get_text()
		d = growCombo.entry.get_text()

		entry = [ a, b, c, d]
		partClist.append(entry)
		addWindow.destroy()
		myCount.increment()

	ok = GtkButton("OK")
	ok.show()
	addTable.attach(ok, 0, 1, 4, 5)
	ok.connect("clicked", addEntry)

	cancelAdd = GtkButton("Cancel")
	cancelAdd.show()
	addTable.attach(cancelAdd, 1, 2, 4, 5)
	cancelAdd.connect("clicked", addWindow.hide)

	addWindow.show()


def editPartition(args, partClist=partClist, selection=s):
	
	editWindow = GtkWindow()
	editWindow.connect("delete_event", deleteEvent)
	editWindow.set_title('Edit Partition Entry')
	editWindow.set_border_width(6)
	editWindow.set_default_size(100, 50)

	editTable = GtkTable(5, 2, FALSE)
	editTable.show()
	editWindow.add(editTable)

	editLabel1 = GtkLabel("Mount Point:")
	editLabel1.show()
	editTable.attach(editLabel1, 0, 1, 0, 1)
	
	mpCombo = GtkCombo()
	editTable.attach(mpCombo, 1, 2, 0, 1)
	mpCombo.show()	
	list_items = [ "/", "/boot", "/home", "/usr", "/opt", "/var" ]			
	mpCombo.set_popdown_strings(list_items)
	mpCombo.entry.set_text("")
	mpCombo.entry.set_editable(TRUE)

	editLabel2 = GtkLabel("Filesystem Type:")
	editLabel2.show()
	editTable.attach(editLabel2, 0, 1, 1, 2)

	fsCombo = GtkCombo()
	editTable.attach(fsCombo, 1, 2, 1, 2)
	fsCombo.show()	
	list_items = [ "ext2", "Linux Swap", "FAT 16" ]			
	fsCombo.set_popdown_strings(list_items)
	fsCombo.entry.set_text("")
	fsCombo.entry.set_editable(FALSE)
	
	editLabel3 = GtkLabel("Size (M):")
	editLabel3.show()
	editTable.attach(editLabel3, 0, 1, 2, 3)

	sizeEntry = GtkEntry()
	editTable.attach(sizeEntry, 1, 2, 2, 3)
	sizeEntry.show()	

	editLabel4 = GtkLabel("Growable:")
	editLabel4.show()
	editTable.attach(editLabel4, 0, 1, 3, 4)

	growCombo = GtkCombo()
	editTable.attach(growCombo, 1, 2, 3, 4)
	growCombo.show()	
	list_items = [ "No", "Yes" ]			
	growCombo.set_popdown_strings(list_items)
#	growCombo.list.select_item(0)
	growCombo.entry.set_editable(FALSE)



	for i in range(4):
		if i == 0:
			mpCombo.entry.set_text(partClist.get_text(s[0], i))
		elif i == 1:
			fsCombo.entry.set_text(partClist.get_text(s[0], i))
		elif i == 2:
			sizeEntry.set_text(partClist.get_text(s[0], i))
		elif i == 3:
			growCombo.entry.set_text(partClist.get_text(s[0], i))
			

	def editEntry(args, editWindow=editWindow, mpCombo=mpCombo, fsCombo=fsCombo, sizeEntry=sizeEntry, growCombo=growCombo, selected=s):
		a = mpCombo.entry.get_text()
		b = fsCombo.entry.get_text()
		c = sizeEntry.get_text()
		d = growCombo.entry.get_text()

		partClist.remove(selected[0])

		entry = [ a, b, c, d]
#		partClist.append(entry)
		partClist.insert(selected[0], entry)
		editWindow.destroy()
		
		editButton.set_state(STATE_INSENSITIVE)
		delButton.set_state(STATE_INSENSITIVE)



	okEdit = GtkButton("OK")
	okEdit.show()
	editTable.attach(okEdit, 0, 1, 4, 5)
	okEdit.connect("clicked", editEntry)

	cancelEdit = GtkButton("Cancel")
	cancelEdit.show()
	editTable.attach(cancelEdit, 1, 2, 4, 5)

	def exitEdit(cancelEdit=cancelEdit, editWindow=editWindow):
		editWindow.hide()

	cancelEdit.connect("clicked", exitEdit)

	editWindow.show()

def deleteEvent(win, event=None):
	win.destroy()
	return TRUE

bootPartition = ["/boot", "ext2", "35", "No"]
partClist.append(bootPartition)

swapPartition = ["", "Linux Swap", "128", "No"]
partClist.append(swapPartition)

rootPartition = ["/", "ext2", "1000", "Yes"]
partClist.append(rootPartition)

partHbox = GtkHBox()
partHbox.show()
partVbox.pack_start(partHbox)

addButton = GtkButton("Add")
addButton.show()
addButton.connect("clicked", addPartition)
partHbox.pack_start(addButton)

editButton = GtkButton("Edit")
editButton.show()
editButton.connect("clicked", editPartition)
partHbox.pack_start(editButton)
editButton.set_state(STATE_INSENSITIVE)

delButton = GtkButton("Delete")
delButton.show()
delButton.connect("clicked", delPartition)
partHbox.pack_start(delButton)
delButton.set_state(STATE_INSENSITIVE)

partClist.connect("select_row", select_clist)
partClist.connect("unselect_row", unselect_clist)

#-----------Package Information---------------#
frame5 = GtkFrame("Package Information")
frame5.set_label("Package Information")
frame5.show()
vbox1.pack_start(frame5)

packageHbox = GtkHBox()
packageHbox.show()
frame5.add(packageHbox)


packageLabel = GtkLabel("Package configuration:")
packageLabel.show()
packageHbox.pack_start(packageLabel)

packageRadio1 = GtkRadioButton(None, "Server")
packageRadio1.show()
packageHbox.pack_start(packageRadio1)

packageRadio2 = GtkRadioButton(packageRadio1, "Workstation")
packageRadio2.show()
packageHbox.pack_start(packageRadio2)

packageRadio3 = GtkRadioButton(packageRadio1, "Custom")
packageRadio3.show()
packageHbox.pack_start(packageRadio3)

packageRadio4 = GtkRadioButton(packageRadio1, "Everything")
packageRadio4.show()
packageHbox.pack_start(packageRadio4)

#---------------------Buttons-------------------#
hbox = GtkHBox()
hbox.show()
hbox.set_border_width(5)
hbox.set_spacing(75)
vbox1.pack_start(hbox)

saveButton = GtkButton("Save File")
saveButton.show()
saveButton.connect("clicked", saveClicked)
hbox.pack_start(saveButton)

exitButton = GtkButton("Exit")
exitButton.show()
exitButton.connect("clicked", destroy)
hbox.pack_start(exitButton)

window.show()
mainloop()
