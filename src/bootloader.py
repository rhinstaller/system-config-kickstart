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
import whrandom
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

    def __init__(self, xml, notebook, kickstartData):
        self.kickstartData = kickstartData
        self.notebook = notebook
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

    def setSensitive(self, boolean):
        self.upgrade_bootloader_radio.set_sensitive(not boolean)

    def getData (self):
        if self.install_bootloader_radio.get_active():
            buf = ""
            #lilo stuff
            if self.lilo_radiobutton.get_active():
                buf = "--useLilo "
                if self.linear_checkbutton.get_active():
                    buf = buf + "--linear "
                else:
                    buf = buf + "--nolinear "
                if self.lba32_checkbutton.get_active():
                    buf = buf + "--lba32 "
            #end of lilo stuff
            if self.mbr_radiobutton.get_active():
                buf = buf + "--location=mbr "
            elif self.firstsector_radiobutton.get_active():
                buf = buf + "--location=partition "                
            params = string.strip (self.parameters_entry.get_text())
            length = len (params)
            if length > 0:
                buf = buf + "--append " + params + " "

            if self.grub_password_checkbutton.get_active() == gtk.TRUE:
                gp = string.strip (self.grub_password_entry.get_text())
                cp = string.strip (self.grub_password_confirm.get_text())
                length = len(gp)
                if length > 0:
                    if gp == cp:
                        if self.grub_password_encrypt_checkbutton.get_active():
                            salt = "$1$"
                            saltLen = 8
                            for i in range(saltLen):
                                salt = salt + whrandom.choice (string.letters + string.digits + './')
                            self.passwd = crypt.crypt (gp, salt)
                            temp = unicode (self.passwd, 'iso-8859-1')
                            buf = buf + "--md5pass=" + temp
                        else:
                            buf = buf + "--password=" + gp + " "

                    else:
                        dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                                (_("Grub passwords do not match.  Please try again.")))
                        dlg.set_position(gtk.WIN_POS_CENTER)
                        dlg.set_modal(gtk.TRUE)
                        dlg.set_icon(kickstartGui.iconPixbuf)
                        dlg.run()
                        dlg.destroy()
                        self.grub_password_entry.set_text("")
                        self.grub_password_confirm.set_text("")
                        self.notebook.set_current_page(2)
                        self.grub_password_entry.grab_focus()
                        return None
                        
        elif self.upgrade_bootloader_radio.get_active():
            buf = "--upgrade"
        else:
            buf = "--location=none"

        self.kickstartData.setBootloader([buf])
        return 0

    def fillData(self):
        list = self.kickstartData.getBootloader()

        if list == None:
            return

        for item in list:
            if item[:11] == "--location=":
                if item[11:] == "none":
                    self.no_bootloader_radio.set_active(gtk.TRUE)
                elif item[11:] == "mbr":
                    self.mbr_radiobutton.set_active(gtk.TRUE)
                elif item[11:] == "partition":
                    self.firstsector_radiobutton.set_active(gtk.TRUE)

            if item[:10] == "--password":
                self.grub_password_entry.set_text(item[10:])
                self.grub_password_confirm.set_text(item[10:])                

        if "--append" in list:
            self.parameters_entry.set_text(list[list.index(item)])

        if "--md5pass" in list:
            self.grub_password_encrypt_checkbutton.set_active(gtk.TRUE)

        if "--upgrade" in list:
            self.upgrade_bootloader_radio.set_active(gtk.TRUE)
            
        if "--useLilo" in list:
            self.lilo_radiobutton.set_active(gtk.TRUE)

            if "--linear" in list:
                self.linear_checkbutton.set_active(gtk.TRUE)

            if "--nolinear" in list:
                self.linear_checkbutton.set_active(gtk.FALSE)

            if "--lba32" in list:
                self.lba32_checkbutton.set_active(gtk.TRUE)

