#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 200, 20021 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002 Brent Fox <bfox@redhat.com>
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

#Kickstart Configurator Bootloader Configuration

import gtk
import gtk.glade
#from gtk import *
#import GtkExtra
#import libglade
import string
import whrandom
import crypt

class bootloader:

    def __init__(self, xml):
        self.install_bootloader_checkbutton = xml.get_widget("install_bootloader_checkbutton")
        self.bootloader_table = xml.get_widget("bootloader_table")
        self.grub_radiobutton = xml.get_widget("grub_radiobutton")
        self.lilo_radiobutton = xml.get_widget("lilo_radiobutton")
        self.mbr_radiobutton = xml.get_widget("mbr_radiobutton")               
        self.firstsector_radiobutton = xml.get_widget("firstsector_radiobutton")
        self.parameters_label = xml.get_widget("parameters_label")
        self.parameters_entry = xml.get_widget("parameters_entry")
        self.lilo_options_label = xml.get_widget("lilo_options_label")
        self.linear_checkbutton = xml.get_widget("linear_checkbutton")
        self.lba32_checkbutton = xml.get_widget("lba32_checkbutton")
        self.grub_options_label = xml.get_widget("grub_options_label")
        self.grub_password_label = xml.get_widget("grub_password_label")
        self.grub_password_entry = xml.get_widget("grub_password_entry")
        self.grub_password_encrypt_checkbutton = xml.get_widget("grub_password_encrypt_checkbutton")
        self.bootloader_upgrade_label = xml.get_widget("bootloader_upgrade_label")
        self.bootloader_upgrade_checkbutton = xml.get_widget("bootloader_upgrade_checkbutton")        
        self.option_notebook = xml.get_widget("option_notebook")

        self.install_bootloader_checkbutton.connect("toggled", self.toggled_bootloader)
        self.grub_radiobutton.connect("toggled", self.toggled_grub)
        self.lilo_radiobutton.connect("toggled", self.toggled_lilo)

    def toggled_bootloader (self, args):
        status = self.install_bootloader_checkbutton.get_active()
        self.bootloader_table.set_sensitive(status)
        self.parameters_label.set_sensitive(status)
        self.parameters_entry.set_sensitive(status)
        self.lilo_options_label.set_sensitive(status)
        self.linear_checkbutton.set_sensitive(status)
        self.lba32_checkbutton.set_sensitive(status)
        self.grub_options_label.set_sensitive(status)        
        self.grub_password_label.set_sensitive(status)
        self.grub_password_entry.set_sensitive(status)
        self.grub_password_encrypt_checkbutton.set_sensitive(status)
        self.bootloader_upgrade_label.set_sensitive(not status)
        self.bootloader_upgrade_checkbutton.set_sensitive(not status)
        self.option_notebook.set_sensitive(status)

    def toggled_lilo (self, args):
        status = self.lilo_radiobutton.get_active()        
        if status:
            self.option_notebook.set_current_page(1)

    def toggled_grub (self, args):
        status = self.grub_radiobutton.get_active()
        if status:
            self.option_notebook.set_current_page(0)
        self.grub_password_encrypt_checkbutton.set_sensitive(status)

    def getData (self):
        data = []
        data.append("")
        data.append("#System bootloader configuration")
        if self.install_bootloader_checkbutton.get_active():
            buf = "bootloader "
            #lilo stuff
            if self.lilo_radiobutton.get_active():
                buf = buf + "--useLilo "
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
            gp = string.strip (self.grub_password_entry.get_text())
            length = len(gp)
            if length > 0:
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
        elif self.bootloader_upgrade_checkbutton.get_active():
            buf = "bootloader --upgrade"
        else:
            buf = "bootloader --location=none"
        data.append(buf)
        return data
        
