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

#Kickstart Configurator Basic Configuration

from gtk import *
import GtkExtra
import libglade
import string
import os

class basic:

    def __init__(self, xml):
        self.xml = xml
        self.lang_combo = xml.get_widget("lang_combo")
        self.lang_support_combo = xml.get_widget("lang_support_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.mouse_combo = xml.get_widget("mouse_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")
        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.lilo_mbr_radiobutton = xml.get_widget("lilo_mbr_radiobutton")
        self.lilo_none_radiobutton = xml.get_widget("lilo_none_radiobutton")
        self.emulate_3_buttons = xml.get_widget("emulate_3_buttons")
        lang_combo = xml.get_widget("lang_combo")
        lang_support_combo = xml.get_widget("lang_support_combo")
        mouse_combo = xml.get_widget("mouse_combo")
        keyboard_combo = xml.get_widget("keyboard_combo")		
        timezone_combo = xml.get_widget("timezone_combo")
        self.reboot_checkbutton = xml.get_widget("reboot_checkbutton")

        #define languages, add languages here
        self.langDict = {"Czech" : "cs_CZ",
                         "English" : "en_US",
                         "French" : "fr_FR",
                         "German" : "de_DE",
                         "Hungarian" : "hu_HU",
                         "Icelandic" : "is_IS",
                         "Italian" : "it_IT",
                         "Japanese" : "ja_JP.eucJP",
                         "Norwegian" : "no_NO",
                         "Romanian" : "ro_RO",
                         "Russian" : "ru_RU.K0I8-R",
                         "Serbian" : "sr_YU",
                         "Slovak" : "sk_SK",
                         "Slovenian" : "sl_SI",
                         "Spanish" : "es_ES",
                         "Swedish" : "sv_SE",
                         "Turkish" : "tr_TR",
                         "Ukrainian" : "tr_TR",
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
                           "Genius NetMouse Pro (PS/2)" : "geniusnmps/2",
                           "Genius NetScroll (PS/2)" : "geniusnsps/2",
                           "Kensington Thinking Mouse (serial)" : "thinking",
                           "Kensington Thinking Mouse (PS/2)" : "thinkingps/2",
                           "Logitech Mouse (serial, old C7 type)" : "logitech",
                           "Logitech CC Series (serial)" : "logitechcc",
                           "Logitech Bus Mouse" : "logibm",
                           "Logitech MouseMan/FirstMouse (serial)" : "logimman",
                           "Logitech MouseMan/FirstMouse (PS/2)" : "logimmanps/2",
                           "Logitech MouseMan+/FirstMouse+ (serial)" : "logimman+",
                           "Logitech MouseMan+/FirstMouse+ (PS/2)" : "logimman+ps/2",
                           "Logitech MouseMan Wheel (USB)" : "generic3usb",
                           "Microsoft compatible (serial)" : "microsoft",
                           "Microsoft Rev 2.1A or higher (serial)" : "msnew",
                           "Microsoft IntelliMouse (serial)" : "msintelli",
                           "Microsoft IntelliMouse (PS/2)" : "msintellips/2",
                           "Microsoft IntelliMouse (USB)" : "generic3usb",
                           "Microsoft Bus Mouse" : "msbm",
                           "Mouse Systems (serial)" : "mousesystems",
                           "MM Series (serial)" : "mmseries",
                           "MM HitTablet (serial)" : "mmhittab",
                           }

        #populate language combo
        lang_list = self.langDict.keys()
        lang_list.sort()
        lang_combo.set_popdown_strings(lang_list)
        #set default to English
        lang_combo.list.select_item(1)
        lang_combo.entry.set_editable(FALSE)

        #populate language support combo
        lang_support_combo.set_popdown_strings(lang_list)
        #set default to English
        lang_support_combo.list.select_item(1)
        lang_support_combo.entry.set_editable(FALSE)				
        
        #populate mouse combo
        mouse_list = ["Probe for Mouse"]
        dict_list = self.mouseDict.keys()
        dict_list.sort()
        for item in dict_list:
            mouse_list.append(item)
        mouse_combo.set_popdown_strings(mouse_list)
        mouse_combo.list.select_item(0)
        mouse_combo.entry.set_editable(FALSE)		

        #populate keyboard combo, add keyboards here
        keyboard_list = [ "azerty", "be-latin1", "be2-latin1",
                       "fr-latin0", "fr-pc", "fr", "wangbe", "ANSI-dvorak",
                       "dvorak-1", "dvorak-r", "dvorak", "pc-dvorak-latin1",
                       "tr_f-latin5", "trf", "bg", "cf", "cz-lat2-prog",
                       "cz-lat2", "defkeymap", "defkeymap_V1.0", "dk-latin1",
                       "dk.emacs", "emacs2", "es", "fi-latin1", "fi",
                       "gr-pc", "gr", "hebrew", "hu101", "is-latin",
                       "it-ibm", "it", "it2", "jp106", "la-latin1", "lt",
                       "lt.l4", "nl", "no-latin1", "no", "pc110", "pl",
                       "pt-latin1", "pt-old", "ro", "ru-cp1251", "ru-ms",
                       "ru-yawerty", "ru", "ru1", "ru2", "ru_win",
                       "se-latin1", "sk-prog-qwerty", "sk-prog", "sk-qwerty",
                       "tr_q-latin5", "tralt", "trf", "trq", "ua", "uk",
                       "us", "croat", "cz-us-qwerty", "de-latin1-nodeadkeys",
                       "de-latin1", "de", "fr_CH-latin1", "fr_CH", "hu",
                       "sg-latin1-lk450", "sg-latin1", "sg",
                       "sk-prog-qwertz", "sk-qwertz", "slovene" ]
        keyboard_combo.set_popdown_strings(keyboard_list)
        #set default to English
        keyboard_combo.list.select_item(63)
        keyboard_combo.entry.set_editable(FALSE)		

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
        timezone_combo.entry.set_editable(FALSE)		

    def getData(self):
        buf = ""
        buf = buf + "\n" + "lang " + self.languageLookup(self.lang_combo.entry.get_text())
        buf = buf + "\n" + "langsupport " + self.languageLookup(self.lang_support_combo.entry.get_text())
        buf = buf + "\n" + "keyboard " + self.keyboard_combo.entry.get_text()
        buf = buf + "\n" + self.mouseLookup(self.mouse_combo.entry.get_text())
        buf = buf + "\n" + "timezone --utc " + self.timezone_combo.entry.get_text()
        buf = buf + "\n" + "rootpw " + self.root_passwd_entry.get_text()
        if self.lilo_mbr_radiobutton.get_active():
            buf = buf + "\n" + "lilo --location mbr"
        elif self.lilo_none_radiobutton.get_active():
            buf = buf + "\n" + "lilo --location none"
        if self.reboot_checkbutton.get_active():
            buf = buf + "\n" + "reboot"
        return buf

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


