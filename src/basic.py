#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002 Red Hat, Inc.
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

#Kickstart Configurator Basic Configuration

import gtk
import gtk.glade
import gobject
import string
import os
import whrandom
import crypt

from rhpl import keyboard_models
import rhpl.keyboard as keyboard

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class basic:

    def __init__(self, xml):
        self.xml = xml
        self.lang_combo = xml.get_widget("lang_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.mouse_combo = xml.get_widget("mouse_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")
        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.emulate_3_buttons = xml.get_widget("emulate_3_buttons")
        lang_combo = xml.get_widget("lang_combo")
        self.lang_support_view = xml.get_widget("lang_support_view")
        mouse_combo = xml.get_widget("mouse_combo")
        keyboard_combo = xml.get_widget("keyboard_combo")		
        timezone_combo = xml.get_widget("timezone_combo")
        self.reboot_checkbutton = xml.get_widget("reboot_checkbutton")
        self.text_install_checkbutton = xml.get_widget("text_install_checkbutton")
        self.interactive_checkbutton = xml.get_widget("interactive_checkbutton")                
        self.encrypt_root_pw_checkbutton = xml.get_widget("encrypt_root_pw_checkbutton")
        self.lang_support_list = xml.get_widget("lang_support_list")
#        self.lang_support_list.set_selection_mode(SELECTION_MULTIPLE)
#        self.messagebox = xml.get_widget("messagebox")

        self.lang_support_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.lang_support_view.set_model(self.lang_support_store)
        self.checkbox = gtk.CellRendererToggle()
        col = gtk.TreeViewColumn('', self.checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.checkbox.connect("toggled", self.langToggled)
        self.lang_support_view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.lang_support_view.append_column(col)

        #define languages, add languages here
        self.langDict = {"Chinese(Mainland)" :  "zh_CN.GB2312",
			 "Chinese(Taiwan)" : "zh_TW.Big5",
			 "Czech" : "cs_CZ",
                         "Danish" : "da_DK",
                         "English" : "en_US",
                         "French" : "fr_FR",
                         "German" : "de_DE",
                         "Icelandic" : "is_IS",
                         "Italian" : "it_IT",
                         "Japanese" : "ja_JP.eucJP",
                         "Korean" : "ko_KR.eucKR",
                         "Norwegian" : "no_NO",
                         "Portuguese" : "pt_PT",
                         "Russian" : "ru_RU.k0I8r",
                         "Slovenian" : "sl_SI",
                         "Spanish" : "es_ES",
                         "Swedish" : "sv_SE",
                         "Ukrainian" : "uk_UA",
                    }

        #define mice, add mice here
        self.mouseDict = { "No Mouse" : "none",
                           "ALPS GlidePoint (PS/2)" : "alpsps/2",
                           "ASCII MieMouse (serial)" : "ascii",
                           "ASCII MieMouse (PS/2)" : "asciips/2",
                           "ATI Bus Mouse" : "atibm",
                           "Generic Mouse (serial)" : "generic",
                           "Generic 3 Button Mouse (serial)" : "generic3",
                           "Generic Mouse (PS/2)" : "genericps/2",
                           "Generic 3 Button Mouse (PS/2)" : "generic3ps/2",
                           "Generic Mouse (USB)" : "genericusb",
                           "Generic 3 Button Mouse (USB)" : "generic3usb",
                           "Genius NetMouse (serial)" : "geniusnm",
                           "Genius NetMouse (PS/2)" : "geniusnmps/2",
                           "Genius NetMouse Pro (PS/2)" : "geniusprops/2",
                           "Genius NetScroll (PS/2)" : "geniusscrollps/2",
                           "Kensington Thinking Mouse (serial)" : "thinking",
                           "Kensington Thinking Mouse (PS/2)" : "thinkingps/2",
                           "Logitech Mouse (serial, old C7 type)" : "logitech",
                           "Logitech CC Series (serial)" : "logitechcc",
                           "Logitech Bus Mouse" : "logibm",
                           "Logitech MouseMan/FirstMouse (serial)" : "logimman",
                           "Logitech MouseMan/FirstMouse (PS/2)" : "logimmanps/2",
                           "Logitech MouseMan+/FirstMouse+ (serial)" : "logimman+",
                           "Logitech MouseMan+/FirstMouse+ (PS/2)" : "logimman+ps/2",
                           "Logitech MouseMan Wheel (USB)" : "logimmusb",
                           "Microsoft compatible (serial)" : "microsoft",
                           "Microsoft Rev 2.1A or higher (serial)" : "msnew",
                           "Microsoft IntelliMouse (serial)" : "msintelli",
                           "Microsoft IntelliMouse (PS/2)" : "msintellips/2",
                           "Microsoft IntelliMouse (USB)" : "msintelliusb",
                           "Microsoft Bus Mouse" : "msbm",
                           "Mouse Systems (serial)" : "mousesystems",
                           "MM Series (serial)" : "mmseries",
                           "MM HitTablet (serial)" : "mmhittab",
                           "Sun Mouse" : "sun",
                           }

        #populate language combo
        lang_list = self.langDict.keys()
        lang_list.sort()
        lang_combo.set_popdown_strings(lang_list)
        #set default to English
        lang_combo.list.select_item(4)
        lang_combo.entry.set_editable(gtk.FALSE)

        self.populateLangSupport()
#        for lang in lang_list:
#            self.lang_support_list.append([lang])

        #populate mouse combo
        mouse_list = ["Probe for Mouse"]
        dict_list = self.mouseDict.keys()
        dict_list.sort()
        for item in dict_list:
            mouse_list.append(item)
        mouse_combo.set_popdown_strings(mouse_list)
        mouse_combo.list.select_item(0)
        mouse_combo.entry.set_editable(gtk.FALSE)		

        #populate keyboard combo, add keyboards here
        self.keyboard_dict = keyboard_models.KeyboardModels().get_models()
        keys = self.keyboard_dict.keys()
        keys.sort()
        keyboard_list = []
        for item in keys:
            keyboard_list.append(self.keyboard_dict[item][0])
        keyboard_combo.set_popdown_strings(keyboard_list)
        #set default to English
        kbd = keyboard.Keyboard()
        kbd.read()
        currentKeymap = kbd.get()
	#set keyboard to current keymap
        keyboard_combo.entry.set_text(self.keyboard_dict[currentKeymap][0])

        #set default mouse to generic ps/2
        mouse_combo.list.select_item(8)

        #populate time zone combo
        if os.access("/usr/share/zoneinfo/zone.tab", os.R_OK):
            tz = open ("/usr/share/zoneinfo/zone.tab", "r")
            lines = tz.readlines()
            tz.close()

        list_items = []

        try:
            for line in lines:
                if line[:1] == "#":
                    pass
                else:
                    tokens = string.split(line)
                    list_items.append(tokens[2])

            list_items.sort()
        except:
            list_items = []

        try:
            select = list_items.index("America/New_York")
        except:
            select = 0

        timezone_combo.set_popdown_strings(list_items)
        timezone_combo.list.select_item(select)
        timezone_combo.entry.set_editable(gtk.FALSE)		

    def langToggled(self, data, row):
        iter = self.lang_support_store.get_iter((int(row),))
        val = self.lang_support_store.get_value(iter, 0)
        self.lang_support_store.set_value(iter, 0 , not val)

    def getData(self):
        data = []
        data.append("")
        data.append("#System language")
        lang = self.languageLookup(self.lang_combo.entry.get_text())
        data.append("lang " + lang)
        data.append("")
        data.append("#Language modules to install")

        lang_list = []
        iter = self.lang_support_store.get_iter_root()
        next = 1

        while next:
            if self.lang_support_store.get_value(iter, 0) == gtk.TRUE:
                lang = self.lang_support_store.get_value(iter, 1) 
                lang_list.append(self.langDict[lang])

            next = self.lang_support_store.iter_next(iter)

        defaultLang = self.languageLookup(self.lang_combo.entry.get_text())

        if len(lang_list) == 0:
            data.append("langsupport " + defaultLang)

        elif len(lang_list) > 0:
            list = string.join(lang_list, " ")
            if len(lang_list) == 1:
                if defaultLang in lang_list:
                    data.append("langsupport " + defaultLang)
                else:
                    data.append("langsupport " + list + " --default " + defaultLang)
                
            else:
                if defaultLang in lang_list:                
                    data.append("langsupport " + list + " --default " + defaultLang)
                else:
                    list = list + " " + defaultLang
                    data.append("langsupport " + list + " --default " + defaultLang)
                
        data.append("")
        data.append("#System keyboard")
        data.append("keyboard " + self.keyboard_dict[self.keyboard_combo.entry.get_text()])
        data.append("")
        data.append("#System mouse")
        data.append(self.mouseLookup(self.mouse_combo.entry.get_text()))
        data.append("")
        data.append("#System timezone")
        data.append("timezone --utc " + self.timezone_combo.entry.get_text())

        data.append("")
        data.append("#Root password")

        if self.root_passwd_entry.get_text() == "":
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, _("Please select a root password."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            rc = dlg.run()
            if rc == gtk.RESPONSE_OK:
                dlg.hide()
            self.root_passwd_entry.grab_focus()
            return
            
        if self.encrypt_root_pw_checkbutton.get_active() == gtk.TRUE:
            pure = self.root_passwd_entry.get_text()

            salt = "$1$"
            saltLen = 8

            for i in range(saltLen):
                salt = salt + whrandom.choice (string.letters + string.digits + './')

            self.passwd = crypt.crypt (pure, salt)

            temp = unicode (self.passwd, 'iso-8859-1')
            data.append("rootpw --iscrypted " + temp)

        else:
            self.passwd = self.root_passwd_entry.get_text()
            data.append("rootpw " + self.passwd)

        if self.reboot_checkbutton.get_active():
            data.append("")
            data.append("#Reboot after installation")
            data.append("reboot")
        if self.text_install_checkbutton.get_active():
            data.append("")
            data.append("#Use text mode install")
            data.append("text")
        if self.interactive_checkbutton.get_active():
            data.append("")
            data.append("#Use interactive kickstart installation method")
            data.append("interactive")

        return data

    def languageLookup(self, args):
        return self.langDict [args]

    def mouseLookup(self, args):
        if args == "Probe for Mouse":
            buf = "#Probe for Mouse"
        else:
            buf = "mouse "
            if self.emulate_3_buttons.get_active():
                buf = buf + "--emulthree "
            buf = buf + self.mouseDict [args]
        return buf

    def populateLangSupport(self):
        lang_list = self.langDict.keys()
        lang_list.sort()        
        
        for lang in lang_list:
            iter = self.lang_support_store.append()
            self.lang_support_store.set_value(iter, 0, gtk.FALSE)
            self.lang_support_store.set_value(iter, 1, lang)
