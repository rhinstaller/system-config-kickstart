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
import gobject
import string
import os
import random
import crypt
import getopt

from rhpl import keyboard_models
import rhpl.keyboard as keyboard
from hardwareLists import langDict

import kickstartGui

import sys
from pykickstart.constants import *

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class basic:
    def __init__(self, parent_class, xml, notebook, ksdata):
        self.parent_class = parent_class
        self.notebook = notebook
        self.ksdata = ksdata
        self.xml = xml
        self.lang_combo = xml.get_widget("lang_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")
        self.utc_check_button = xml.get_widget("utc_check_button")

        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.root_passwd_confirm_entry = xml.get_widget("root_passwd_confirm_entry")        
        self.reboot_checkbutton = xml.get_widget("reboot_checkbutton")
        self.text_install_checkbutton = xml.get_widget("text_install_checkbutton")
        self.ksdata.bootloader["md5pass"] = ""
        self.ksdata.bootloader["password"] = ""
        self.interactive_checkbutton = xml.get_widget("interactive_checkbutton")                
        self.encrypt_root_pw_checkbutton = xml.get_widget("encrypt_root_pw_checkbutton")
        self.lang_support_list = xml.get_widget("lang_support_list")
        self.platform_combo = xml.get_widget("platform_combo")

        self.platform_list =  [_("x86, AMD64, or Intel EM64T"), _("Intel Itanium"), _("IBM iSeries"),
                               _("IBM pSeries"), _("IBM zSeries/s390")]
        self.platform_combo.set_popdown_strings(self.platform_list)
        self.platform_combo.entry.connect("changed", self.platformChanged)

        self.langDict = langDict

        #populate language combo
        self.lang_list = self.langDict.keys()
        self.lang_list.sort()
        self.lang_combo.set_popdown_strings(self.lang_list)

        #set default to English
        self.lang_combo.list.select_item(self.lang_list.index('English (USA)'))

        #populate keyboard combo, add keyboards here
        self.keyboard_dict = keyboard_models.KeyboardModels().get_models()
        keys = self.keyboard_dict.keys()
        keys.sort()
        keyboard_list = []

        for item in keys:
            keyboard_list.append(self.keyboard_dict[item][0])
        self.keyboard_combo.set_popdown_strings(keyboard_list)

        #set default to English
        kbd = keyboard.Keyboard()
        kbd.read()
        currentKeymap = kbd.get()

	#set keyboard to current keymap
        try:
            self.keyboard_combo.entry.set_text(self.keyboard_dict[currentKeymap][0])
        except:
            self.keyboard_combo.entry.set_text(self.keyboard_dict["us"][0])

        #populate time zone combo
        if os.access("/usr/share/zoneinfo/zone.tab", os.R_OK):
            tz = open ("/usr/share/zoneinfo/zone.tab", "r")
            lines = tz.readlines()
            tz.close()

        self.timezone_list = []

        try:
            for line in lines:
                if line[:1] == "#":
                    pass
                else:
                    tokens = string.split(line)
                    self.timezone_list.append(tokens[2])

            self.timezone_list.sort()
        except:
            self.timezone_list = []

        try:
            select = self.timezone_list.index("America/New_York")
        except:
            select = 0

        self.timezone_combo.set_popdown_strings(self.timezone_list)
        self.timezone_combo.list.select_item(select)

    def formToKsdata(self, doInstall):
        self.ksdata.lang = self.languageLookup(self.lang_combo.entry.get_text())

        keys = self.keyboard_dict.keys()
        keys.sort()
        for item in keys:
            if self.keyboard_dict[item][0] == self.keyboard_combo.entry.get_text():
                self.ksdata.keyboard = item
                break

        self.ksdata.timezone["timezone"] = self.timezone_combo.entry.get_text()
        if self.utc_check_button.get_active() == True:
            self.ksdata.timezone["isUtc"] = True

        if self.root_passwd_entry.get_text() != self.root_passwd_confirm_entry.get_text():
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, _("Root passwords do not match."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_icon(kickstartGui.iconPixbuf)
            dlg.set_border_width(2)
            dlg.set_modal(True)
            toplevel = self.xml.get_widget("main_window")
            dlg.set_transient_for(toplevel)
            dlg.run()
            dlg.hide()
            self.notebook.set_current_page(0)
            self.root_passwd_entry.set_text("")
            self.root_passwd_confirm_entry.set_text("")            
            self.root_passwd_entry.grab_focus()
            return None

        if self.root_passwd_entry.get_text() == "" and doInstall:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, _("Please select a root password."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_icon(kickstartGui.iconPixbuf)
            dlg.set_border_width(2)
            dlg.set_modal(True)
            toplevel = self.xml.get_widget("main_window")
            dlg.set_transient_for(toplevel)
            dlg.run()
            dlg.hide()
            self.notebook.set_current_page(0)
            self.root_passwd_entry.grab_focus()
            return None

        pure = self.root_passwd_entry.get_text()

        if self.encrypt_root_pw_checkbutton.get_active() == True:
            salt = "$1$"
            saltLen = 8

            if not pure.startswith(salt):
                for i in range(saltLen):
                    salt = salt + random.choice (string.letters + string.digits + './')

                self.passwd = crypt.crypt (pure, salt)

                temp = unicode (self.passwd, 'iso-8859-1')
                self.ksdata.rootpw["isCrypted"] = True
                self.ksdata.rootpw["password"] = temp
            else:
                self.ksdata.rootpw["isCrypted"] = True
                self.ksdata.rootpw["password"] = pure
        else:
            self.passwd = self.root_passwd_entry.get_text()
            self.ksdata.rootpw["password"] = pure

        self.ksdata.platform = self.platform_combo.entry.get_text()

        if self.reboot_checkbutton.get_active():
            self.ksdata.reboot["action"] = KS_REBOOT
        else:
            self.ksdata.reboot["action"] = KS_WAIT

        if self.text_install_checkbutton.get_active():
            self.ksdata.displayMode = DISPLAY_MODE_TEXT
        else:
            self.ksdata.displayMode = DISPLAY_MODE_GRAPHICAL

        if self.interactive_checkbutton.get_active():
            self.ksdata.interactive = True
        else:
            self.ksdata.interactive = False

        return 0

    def languageLookup(self, args):
        return self.langDict [args]

    def platformChanged(self, entry):
        platform = entry.get_text()
        if platform:
            self.parent_class.platformTypeChanged(entry.get_text())

    def applyKsdata(self):
        if self.ksdata.platform in self.platform_list:
            self.platform_combo.entry.set_text(self.ksdata.platform)

        for lang in self.langDict.keys():
            if self.langDict[lang] == self.ksdata.lang:
                self.lang_combo.list.select_item(self.lang_list.index(lang))

        if self.ksdata.keyboard != "":
            self.keyboard_combo.entry.set_text(self.keyboard_dict[self.ksdata.keyboard][0])

        if self.ksdata.timezone["timezone"] != "":
            self.timezone_combo.list.select_item(self.timezone_list.index(self.ksdata.timezone["timezone"]))

        if self.ksdata.reboot["action"] == KS_REBOOT:
            self.reboot_checkbutton.set_active(True)

        if self.ksdata.displayMode == DISPLAY_MODE_TEXT:
            self.text_install_checkbutton.set_active(True)

        if self.ksdata.interactive == True:
            self.interactive_checkbutton.set_active(True)

        if self.ksdata.rootpw["password"] != "":
            self.root_passwd_entry.set_text(self.ksdata.rootpw["password"])
            self.root_passwd_confirm_entry.set_text(self.ksdata.rootpw["password"])
            self.encrypt_root_pw_checkbutton.set_active(self.ksdata.rootpw["isCrypted"])
