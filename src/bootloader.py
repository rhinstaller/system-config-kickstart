## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                      Tammy Fox <tfox@redhat.com>

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

import gtk
import gtk.glade
import string
import random
import crypt

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

import kickstartGui

class bootloader:

    def __init__(self, xml, notebook, ksdata):
        self.ksdata = ksdata
        self.notebook = notebook
        self.bootloader_vbox = xml.get_widget("bootloader_vbox")
        self.bootloader_label = xml.get_widget("bootloader_label")
        self.install_bootloader_radio = xml.get_widget("install_bootloader_radio")
        self.upgrade_bootloader_radio = xml.get_widget("upgrade_bootloader_radio")
        self.no_bootloader_radio = xml.get_widget("no_bootloader_radio")
        self.mbr_radiobutton = xml.get_widget("mbr_radiobutton")               
        self.firstsector_radiobutton = xml.get_widget("firstsector_radiobutton")
        self.parameters_label = xml.get_widget("parameters_label")
        self.parameters_entry = xml.get_widget("parameters_entry")
        self.linear_checkbutton = xml.get_widget("linear_checkbutton")
        self.lba32_checkbutton = xml.get_widget("lba32_checkbutton")
        self.grub_password_label = xml.get_widget("grub_password_label")
        self.grub_password_checkbutton = xml.get_widget("grub_password_checkbutton")
        self.grub_password_hbox = xml.get_widget("grub_password_hbox")
        self.grub_password_entry = xml.get_widget("grub_password_entry")
        self.grub_password_confirm = xml.get_widget("grub_password_confirm")
        self.grub_password_encrypt_checkbutton = xml.get_widget("grub_password_encrypt_checkbutton")

        self.install_bootloader_radio.connect("toggled", self.toggled_bootloader)
        self.grub_password_checkbutton.connect("toggled", self.toggled_grub_password)

    def toggled_bootloader (self, args):
        status = self.install_bootloader_radio.get_active()
        self.parameters_label.set_sensitive(status)
        self.parameters_entry.set_sensitive(status)
        self.mbr_radiobutton.set_sensitive(status)
        self.firstsector_radiobutton.set_sensitive(status)

    def toggled_grub_password(self, args):
        self.grub_password_hbox.set_sensitive(self.grub_password_checkbutton.get_active())

    def platformTypeChanged(self, platform):
        if platform != "x86, AMD64, or Intel EM64T":
            self.bootloader_vbox.hide()
            self.bootloader_label.set_text(_("Bootloader options are not applicable to "
                                             "the %s platform" % platform))
            self.bootloader_label.show()
        else:
            self.bootloader_vbox.show()
            self.bootloader_label.hide()

    def enableUpgradeRadio(self, boolean):
        self.upgrade_bootloader_radio.set_sensitive(not boolean)

    def getData (self):
        if self.install_bootloader_radio.get_active():
            buf = ""
            if self.mbr_radiobutton.get_active():
                self.ksdata.bootloader["location"] = "mbr"
            elif self.firstsector_radiobutton.get_active():
                self.ksdata.bootloader["location"] = "partition"

            params = string.strip (self.parameters_entry.get_text())
            if len(params) > 0:
                self.ksdata.bootloader["appendLine"] = params

            if self.grub_password_checkbutton.get_active() == True:
                gp = string.strip (self.grub_password_entry.get_text())
                cp = string.strip (self.grub_password_confirm.get_text())

                if len(gp) > 0:
                    if gp == cp:
                        if self.grub_password_encrypt_checkbutton.get_active():
                            salt = "$1$"
                            saltLen = 8
                            for i in range(saltLen):
                                salt = salt + random.choice (string.letters + string.digits + './')
                            self.passwd = crypt.crypt (gp, salt)
                            self.ksdata.bootloader["md5pass"] = unicode(self.passwd, 'iso-8859-1')
                        else:
                            self.ksdata.bootloader["password"] = gp

                    else:
                        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                                (_("Grub passwords do not match.  Please try again.")))
                        dlg.set_position(gtk.WIN_POS_CENTER)
                        dlg.set_modal(True)
                        dlg.set_icon(kickstartGui.iconPixbuf)
                        dlg.run()
                        dlg.destroy()
                        self.grub_password_entry.set_text("")
                        self.grub_password_confirm.set_text("")
                        self.notebook.set_current_page(2)
                        self.grub_password_entry.grab_focus()
                        return None
                        
        elif self.upgrade_bootloader_radio.get_active():
            self.ksdata.bootloader["upgrade"] = True
        else:
            self.ksdata.bootloader["location"] = "none"

        return 0

    def fillData(self):
        if self.ksdata.bootloader["location"] == "none":
            self.no_bootloader_radio.set_active(True)
        elif self.ksdata.bootloader["location"] == "mbr":
            self.mbr_radiobutton.set_active(True)
        elif self.ksdata.bootloader["location"] == "partition":
            self.firstsector_radiobutton.set_active(True)

        if self.ksdata.bootloader["password"] != "":
            self.grub_password_entry.set_text(self.ksdata.bootloader["password"])
            self.grub_password_confirm.set_text(self.ksdata.bootloader["password"])

        if self.ksdata.bootloader["appendLine"] != "":
            self.parameters_entry.set_text(self.ksdata.bootloader["appendLine"])

        if self.ksdata.bootloader["md5pass"] != "":
            self.grub_password_encrypt_checkbutton.set_active(True)

        if self.ksdata.bootloader["upgrade"] == True:
            self.upgrade_bootloader_radio.set_active(True)
