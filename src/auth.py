#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2007 Red Hat, Inc.
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
import gtk.glade
import getopt
import string

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class nisData:
    def __init__(self, quit_cb=None):
        global nisdomain
        global nisserver
        self.nisdomain = ''
        self.nisserver = ''
        self.broadcast = "OFF"
        self.enabled = 0

    def set_domain(self, name):
        self.nisdomain = name
    def set_server(self, name):
        self.nisserver = name
    def set_enabled(self, val):
        self.enabled = val
    def set_broadcast(self, name):
        self.broadcast = name
    def return_domain(self):
        return self.nisdomain
    def return_server(self):
        return self.nisserver
    def return_status(self):
        return self.enabled
    def return_broadcast(self):
        return self.broadcast
    def return_data(self):
        if self.enabled == 0:
            return ""
        else:
            if self.return_broadcast() == 'ON':
                if self.nisdomain == "":
                    return ""
                else:
                    return " --enablenis --nisdomain=" + self.nisdomain
            else:
                if self.nisdomain == "" or self.nisserver == "":
                    return ""
                else:
                    return " --enablenis --nisdomain=" + self.nisdomain + " --nisserver=" + self.nisserver
			
class ldapData:
    def __init__(self, quit_cb=None):
        global ldapAuth
        global ldapServer
        global ldapDN
        self.ldapAuth = "YES"
        self.ldapServer = ''
        self.ldapDN = ''
        self.ldapCert = ''
        self.enabled = 0
    def set_auth(self, name):
        self.ldapAuth = name
    def set_server(self, name):
        self.ldapServer = name
    def set_DN(self, name):
        self.ldapDN = name
    def set_cert(self, name):
        self.ldapCert = name
    def set_enabled(self, val):
        self.enabled = val
    def return_auth(self):
        return self.ldapAuth
    def return_server(self):
        return self.ldapServer
    def return_DN(self):
        return self.ldapDN
    def return_status(self):
        return self.enabled
    def return_data(self):
        if self.enabled == 0:
            return ""
        elif self.ldapServer == "" or self.ldapDN == "":
            return ""
        else:
            retval = " --enableldap --enableldapauth --ldapserver=" + self.ldapServer + " --ldapbasedn=" + self.ldapDN

            if self.ldapCert == "":
                return retval
            else:
                return retval + " --ldaploadcacert=" + self.ldapCert

class kerberosData:
    def __init__(self, quit_cb=None):
        global kerberosRealm
        global kerberosKDC
        global kerberosMaster
        self.kerberosRealm = " "
        self.kerberosKDC = " "
        self.kerberosMaster = " "
        self.enabled = 0
    def set_realm(self, name):
        self.kerberosRealm = name
    def set_KDC(self, name):
        self.kerberosKDC = name
    def set_master(self, name):
        self.kerberosMaster = name
    def set_enabled(self, val):
        self.enabled = val
    def return_realm(self):
        return self.kerberosRealm
    def return_KDC(self):
        return self.kerberosKDC
    def return_master(self):
        return self.kerberosMaster
    def return_status(self):
        return self.enabled
    def return_data(self):
        if self.enabled == 0:
            return ""
        elif self.kerberosRealm == "" or self.kerberosKDC == "" or self.kerberosMaster == "":
            return ""
        else:
            return " --enablekrb5 --krb5realm=" + self.kerberosRealm + " --krb5kdc=" + self.kerberosKDC + " --krb5adminserver=" + self.kerberosMaster
            
class hesiodData:
    def __init__(self, quit_cb=None):
        global hesiodLHS
        global hesiodRHS
        self.hesiodLHS = " "
        self.hesiodRHS = " "
        self.enabled = 0
    def set_LHS(self, name):
        self.hesiodLHS = name
    def set_RHS(self, name):
        self.hesiodRHS = name
    def set_enabled(self, val):
        self.enabled = val
    def return_LHS(self):
        return self.hesiodLHS
    def return_RHS(self):
        return self.hesiodRHS
    def return_status(self):
        return self.enabled
    def return_data(self):
        if self.enabled == 0:
            return ""
        elif self.hesiodLHS == "" or self.hesiodRHS == "":
            return ""
        else:
            return " --enablehesiod --hesiodlhs=" + self.hesiodLHS + " --hesiodrhs=" + self.hesiodRHS

class sambaData:
	def __init__(self, quit_cb=None):
		global sambaServer
		global sambaWorkgroup
		self.sambaServer = " "
		self.sambaWorkgroup = " "
		self.enabled = 0
	def set_server(self, name):
		self.sambaServer = name
        def set_workgroup(self, name):
		self.sambaWorkgroup = name
        def set_enabled(self, val):
		self.enabled = val
	def return_server(self):
		return self.sambaServer
	def return_workgroup(self):
		return self.sambaWorkgroup
	def return_status(self):
		return self.disabled
	def return_data(self):
		if self.enabled == 0:
			return ""
                elif self.sambaServer == "" or self.sambaWorkgroup == "":
                        return ""
                else:
			return " --enablesmbauth --smbservers=" + self.sambaServer + " --smbworkgroup=" + self.sambaWorkgroup

      
class auth:
    def formToKickstart(self):
        if self.nisCheck.get_active():
            self.myNisClass.set_domain(self.nisDomainEntry.get_text())
            self.myNisClass.set_server(self.nisServerEntry.get_text())

            if self.nisBroadcastCheck.get_active():
                self.myNisClass.set_broadcast("ON")
            else:
                self.myNisClass.set_broadcast("OFF")

            if self.myNisClass.return_data() == "":
                self.showDialog()
                return None
        else:
            self.myNisClass.set_enabled(self.nisCheck.get_active())

        if self.ldapCheck.get_active():
            self.myLDAPClass.set_server(self.ldapServerEntry.get_text())
            self.myLDAPClass.set_DN(self.ldapDNEntry.get_text())

            if self.ldapCertCheck.get_active():
                self.myLDAPClass.set_cert(self.ldapCertEntry.get_text())
            else:
                self.myLDAPClass.set_cert("")

            if self.myLDAPClass.return_data() == "":
                self.showDialog()
                return None
        else:
            self.myLDAPClass.set_enabled(self.ldapCheck.get_active())

        if self.kerberosCheck.get_active():
            self.myKerberosClass.set_realm(self.kerberosRealmEntry.get_text())
            self.myKerberosClass.set_KDC(self.kerberosKDCEntry.get_text())
            self.myKerberosClass.set_master(self.kerberosMasterEntry.get_text())

            if self.myKerberosClass.return_data() == "":
                self.showDialog()
                return None
        else:
            self.myKerberosClass.set_enabled(self.kerberosCheck.get_active())

        if self.hesiodCheck.get_active():
            self.myHesiodClass.set_LHS(self.hesiodLHSEntry.get_text())
            self.myHesiodClass.set_RHS(self.hesiodRHSEntry.get_text())

            if self.myHesiodClass.return_data() == "":
                self.showDialog()
                return None
        else:
            self.myHesiodClass.set_enabled(self.hesiodCheck.get_active())

        if self.sambaCheck.get_active():
            self.mySambaClass.set_server(self.sambaServerEntry.get_text())
            self.mySambaClass.set_workgroup(self.sambaWorkgroupEntry.get_text())

            if self.mySambaClass.return_data() == "":
                self.showDialog()
                return None
        else:
            self.mySambaClass.set_enabled(self.sambaCheck.get_active())

        buf = ""
        if self.shadow_passwd_checkbutton.get_active():
            buf = " --useshadow "
        if self.authCombobox.get_active() == 0:
            buf += " --passalgo=md5"
        elif self.authCombobox.get_active() == 1:
            buf += " --passalgo=sha256"
        elif self.authCombobox.get_active() == 2:
            buf += " --passalgo=sha512"

        buf = buf + self.myNisClass.return_data()
        buf = buf + self.myLDAPClass.return_data()
        buf = buf + self.myKerberosClass.return_data()
        buf = buf + self.myHesiodClass.return_data()
        buf = buf + self.mySambaClass.return_data()
	
        if (self.nscd_checkbutton.get_active()):
            buf = buf + " --enablecache"

        self.ks.authconfig(authconfig=buf)
        return 0
    
    def __init__(self, xml, ksHandler):
        self.ks = ksHandler

        self.myNisClass = nisData()
        self.myLDAPClass = ldapData()
        self.myKerberosClass = kerberosData()
        self.myHesiodClass = hesiodData()
        self.mySambaClass = sambaData()

        self.auth_vbox = xml.get_widget("auth_vbox")
        self.auth_label_box = xml.get_widget("auth_label_box")
        self.authCombobox = xml.get_widget("authCombobox")
        self.nisCheck = xml.get_widget("nisCheck")
        self.nisDomainLabel = xml.get_widget("nisDomainLabel")
        self.nisDomainEntry = xml.get_widget("nisDomainEntry")
        self.nisServerLabel = xml.get_widget("nisServerLabel")
        self.nisBroadcastCheck = xml.get_widget("nisBroadcastCheck")
        self.nisServerEntry = xml.get_widget("nisServerEntry")
        self.ldapCheck = xml.get_widget("ldapCheck")
        self.ldapLabel1 = xml.get_widget("ldapLabel1")
        self.ldapLabel2 = xml.get_widget("ldapLabel2")
        self.ldapLabel3 = xml.get_widget("ldapLabel3")
        self.ldapServerEntry = xml.get_widget("ldapServerEntry")
        self.ldapDNEntry = xml.get_widget("ldapDNEntry")
        self.ldapCertCheck = xml.get_widget("ldapCertCheck")
        self.ldapCertEntry = xml.get_widget("ldapCertEntry")
        self.kerberosCheck = xml.get_widget("kerberosCheck")
        self.kerberosLabel1 = xml.get_widget("kerberosLabel1")
        self.kerberosLabel2 = xml.get_widget("kerberosLabel2")
        self.kerberosLabel3 = xml.get_widget("kerberosLabel3")
        self.kerberosRealmEntry = xml.get_widget("kerberosRealmEntry")
        self.kerberosKDCEntry = xml.get_widget("kerberosKDCEntry")
        self.kerberosMasterEntry = xml.get_widget("kerberosMasterEntry")
        self.hesiodCheck = xml.get_widget("hesiodCheck")
        self.hesiodLabel1 = xml.get_widget("hesiodLabel1")
        self.hesiodLabel2 = xml.get_widget("hesiodLabel2")
        self.hesiodLabel3 = xml.get_widget("hesiodLabel3")
        self.hesiodLHSEntry = xml.get_widget("hesiodLHSEntry")
        self.hesiodRHSEntry = xml.get_widget("hesiodRHSEntry")
        self.sambaCheck = xml.get_widget("sambaCheck")
        self.sambaLabel1 = xml.get_widget("sambaLabel1")
        self.sambaLabel2 = xml.get_widget("sambaLabel2")
        self.sambaServerEntry = xml.get_widget("sambaServerEntry")
        self.sambaWorkgroupEntry = xml.get_widget("sambaWorkgroupEntry")
        self.nscd_checkbutton = xml.get_widget("nscd_checkbutton")
        self.shadow_passwd_checkbutton = xml.get_widget("shadow_passwd_checkbutton")

        self.nisCheck.connect("toggled", self.enableNIS)
        self.nisBroadcastCheck.connect("toggled", self.enableBroadcast)
        self.ldapCheck.connect("toggled", self.enableLDAP)
        self.ldapCertCheck.connect("toggled", self.enableCert)
        self.kerberosCheck.connect("toggled", self.enableKerberos)
        self.hesiodCheck.connect("toggled", self.enableHesiod)
        self.sambaCheck.connect("toggled", self.enableSamba)

        self.authCombobox.set_active(0)

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def showDialog(self):
        text = _("Please fill in the authentication information")
        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
        dlg.set_position(gtk.WIN_POS_CENTER)
        dlg.set_modal(True)
        rc = dlg.run()
        dlg.destroy()
        return None

    def enableNIS(self, args):
        self.nisDomainLabel.set_sensitive(self.nisCheck.get_active())
        self.nisDomainEntry.set_sensitive(self.nisCheck.get_active())
        self.nisServerLabel.set_sensitive(self.nisCheck.get_active())
        self.nisBroadcastCheck.set_sensitive(self.nisCheck.get_active())	
        self.nisServerEntry.set_sensitive(self.nisCheck.get_active())
        self.myNisClass.set_enabled(self.nisCheck.get_active())
        
    def enableBroadcast(self, checkbutton):
        val = not checkbutton.get_active()
        self.nisServerEntry.set_sensitive(val)
        self.nisServerLabel.set_sensitive(val)
            
    def enableLDAP(self, args):
        self.ldapLabel1.set_sensitive(self.ldapCheck.get_active())		
        self.ldapLabel2.set_sensitive(self.ldapCheck.get_active())		
        self.ldapServerEntry.set_sensitive(self.ldapCheck.get_active())
        self.ldapDNEntry.set_sensitive(self.ldapCheck.get_active())				
        self.ldapCertCheck.set_sensitive(self.ldapCheck.get_active())
        self.ldapLabel3.set_sensitive(self.ldapCheck.get_active() and self.ldapCertCheck.get_active())
        self.ldapCertEntry.set_sensitive(self.ldapCheck.get_active() and self.ldapCertCheck.get_active())
        self.myLDAPClass.set_enabled(self.ldapCheck.get_active())

    def enableCert(self, checkbutton):
        val = checkbutton.get_active()
        self.ldapLabel3.set_sensitive(val)
        self.ldapCertEntry.set_sensitive(val)

    def enableKerberos(self, args):
        self.kerberosLabel1.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosLabel2.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosLabel3.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosRealmEntry.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosKDCEntry.set_sensitive(self.kerberosCheck.get_active())
        self.kerberosMasterEntry.set_sensitive(self.kerberosCheck.get_active())
        self.myKerberosClass.set_enabled(self.kerberosCheck.get_active())			

    def enableHesiod(self, args):
        self.hesiodLabel1.set_sensitive(self.hesiodCheck.get_active())		
        self.hesiodLabel2.set_sensitive(self.hesiodCheck.get_active())		
        self.hesiodLHSEntry.set_sensitive(self.hesiodCheck.get_active())
        self.hesiodRHSEntry.set_sensitive(self.hesiodCheck.get_active())	
        self.myHesiodClass.set_enabled(self.hesiodCheck.get_active())

    def enableSamba(self, args):
        self.sambaLabel1.set_sensitive(self.sambaCheck.get_active())		
        self.sambaLabel2.set_sensitive(self.sambaCheck.get_active())		
        self.sambaServerEntry.set_sensitive(self.sambaCheck.get_active())
        self.sambaWorkgroupEntry.set_sensitive(self.sambaCheck.get_active())	
        self.mySambaClass.set_enabled(self.sambaCheck.get_active())
        
    def toggleLDAP(self, args):
        if (self.ldapRadio1.get_active()):
            self.myLDAPClass.set_auth("YES")
        else:
            self.myLDAPClass.set_auth("No")	

    def setSensitive(self, boolean):
        if boolean == False:
            self.auth_vbox.hide()
            self.auth_label_box.show()
        else:
            self.auth_vbox.show()
            self.auth_label_box.hide()

    def applyKickstart(self):
        if self.ks.authconfig.authconfig != "":
            authstr = string.split(self.ks.authconfig.authconfig)
            opts, args = getopt.getopt(authstr, "d:h",["enablemd5", "enablenis", "passalgo=",
                                       "nisdomain=", "nisserver=", "useshadow", "enableshadow",
                                       "enableldap", "enableldapauth", "ldapserver=", "ldapbasedn=",
                                       "ldaploadcacert=", "enableldaptls",
                                       "enablekrb5", "krb5realm=", "krb5kdc=", "krb5adminserver=",
                                       "enablehesiod", "hesiodlhs=", "hesiodrhs=", "enablesmbauth",
                                       "smbservers=", "smbworkgroup=", "enablecache"])

            for opt, value in opts:
                if opt == "--enablemd5":
                    self.authCombobox.set_active(0)

                if opt == "--passalgo":
                    if value == "md5":
                        self.authCombobox.set_active(0)
                    elif value == "sha256":
                        self.authCombobox.set_active(1)
                    elif value == "sha512":
                        self.authCombobox.set_active(2)

                if opt == "--enableshadow" or opt == "--useshadow":
                    self.shadow_passwd_checkbutton.set_active(True)

                if opt == "--enablenis":
                    self.nisCheck.set_active(True)
                    self.nisBroadcastCheck.set_active(True)

                if opt == "--nisdomain":
                    self.nisCheck.set_active(True)
                    self.nisDomainEntry.set_text(value)
                    self.nisBroadcastCheck.set_active(True)

                if opt == "--nisserver":
                    self.nisCheck.set_active(True)
                    self.nisServerEntry.set_text(value)
                    self.nisBroadcastCheck.set_active(False)

                if opt == "--enableldap":
                    self.ldapCheck.set_active(True)

                if opt == "--ldapserver":
                    self.ldapServerEntry.set_text(value)
                    self.ldapCheck.set_active(True)

                if opt == "--ldapbasedn":
                    self.ldapDNEntry.set_text(value)
                    self.ldapCheck.set_active(True)

                if opt == "--ldaploadcacert":
                    self.ldapCertEntry.set_text(value)
                    self.ldapCheck.set_active(True)
                    self.ldapCertCheck.set_active(True)

                if opt == "--enablekrb5":
                    self.kerberosCheck.set_active(True)

                if opt == "--krb5realm":
                    self.kerberosRealmEntry.set_text(value)
                    self.kerberosCheck.set_active(True)

                if opt == "--krb5kdc":
                    self.kerberosKDCEntry.set_text(value)
                    self.kerberosCheck.set_active(True)

                if opt == "--krb5adminserver":
                    self.kerberosMasterEntry.set_text(value)
                    self.kerberosCheck.set_active(True)

                if opt == "--enablehesiod":
                    self.hesiodCheck.set_active(True)

                if opt == "--hesiodlhs":
                    self.hesiodLHSEntry.set_text(value)
                    self.hesiodCheck.set_active(True)

                if opt == "--hesiodrhs":
                    self.hesiodRHSEntry.set_text(value)
                    self.hesiodCheck.set_active(True)

                if opt == "--enablesmbauth":
                    self.sambaCheck.set_active(True)

                if opt == "--smbservers":
                    self.sambaServerEntry.set_text(value)
                    self.sambaCheck.set_active(True)

                if opt == "--smbworkgroup":
                    self.sambaWorkgroupEntry.set_text(value)
                    self.sambaCheck.set_active(True)                

                if opt == "--enablecache":
                    self.nscd_checkbutton.set_active(True)
