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
import whrandom
import crypt
from gnome.ui import *
import gnome.ui

##
## I18N
##
import gettext
gettext.bindtextdomain ("ksconfig", "/usr/share/locale")
gettext.textdomain ("ksconfig")
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
#        lang_support_combo = xml.get_widget("lang_support_combo")
        mouse_combo = xml.get_widget("mouse_combo")
        keyboard_combo = xml.get_widget("keyboard_combo")		
        timezone_combo = xml.get_widget("timezone_combo")
        self.reboot_checkbutton = xml.get_widget("reboot_checkbutton")
        self.text_install_checkbutton = xml.get_widget("text_install_checkbutton")
        self.interactive_checkbutton = xml.get_widget("interactive_checkbutton")                
        self.encrypt_root_pw_checkbutton = xml.get_widget("encrypt_root_pw_checkbutton")
        self.lang_support_list = xml.get_widget("lang_support_list")
        self.lang_support_list.set_selection_mode(SELECTION_MULTIPLE)
#        self.messagebox = xml.get_widget("messagebox")

        #define languages, add languages here
        self.langDict = {"Chinese(Mainland)" :  "zh_CN.GB2312",
			 "Chinese(Taiwan)" : "zh_TW.Big5",
			 "Czech" : "cs_CZ",
                         "Danish" : "da_DK",
                         "English" : "en_US",
                         "French" : "fr_FR",
                         "German" : "de_DE",
                         "Hungarian" : "hu_HU",
                         "Icelandic" : "is_IS",
                         "Italian" : "it_IT",
                         "Japanese" : "ja_JP.eucJP",
                         "Korean" : "ko_KR.eucKR",
                         "Norwegian" : "no_NO",
                         "Portuguese" : "pt_PT",
                         "Romanian" : "ro_RO",
                         "Russian" : "ru_RU.k0I8r",
                         "Serbian" : "sr_YU",
                         "Slovak" : "sk_SK",
                         "Slovenian" : "sl_SI",
                         "Spanish" : "es_ES",
                         "Swedish" : "sv_SE",
                         "Turkish" : "tr_TR",
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

        self.langSupportList = []

        #populate language combo
        lang_list = self.langDict.keys()
        lang_list.sort()
        lang_combo.set_popdown_strings(lang_list)
        #set default to English
        lang_combo.list.select_item(4)
        lang_combo.entry.set_editable(FALSE)

        for lang in lang_list:
            self.lang_support_list.append([lang])

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
        self.keyboard_dict = { 'U.S. English': 'us',
                          'Swiss German': 'de_CH',
                          'Swiss French': 'fr_CH',
                          'PC-98xx Series': 'nec/jp',
                          'Polish': 'pl',
                          'Canadian': 'ca',
                          'Spanish': 'es',
                          'Slovak': 'sk',
                          'Macedonian': 'mk',
                          'United Kingdom':'gb',
                          'Belarusian': 'by',
                          'Japanese': 'jp',
                          'German': 'de',
                          'Czech': 'cz',
                          'Portuguese':
                          'pt',
                          'Turkish': 'tr',
                          'Croatian': 'hr',
                          'U.S. English w/ deadkeys': 'us_intl',
                          'Serbian': 'sr',
                          'Latvian': 'lv',
                          'Ukrainian': 'ua',
                          'Greek': 'el',
                          'Norwegian': 'no',
                          'Lithuanian qwerty programmers': 'lt_p',
                          'Finnish': 'fi',
                          'Czech (qwerty)': 'cz_qwerty',
                          'Dvorak': 'dvorak',
                          'Thai': 'th',
                          'Russian': 'ru',
                          'Armenian': 'am',
                          'Azerbaidjani': 'az',
                          'Lithuanian qwerty "numeric"': 'lt',
                          'Slovak (qwerty)': 'sk_qwerty',
                          'French': 'fr',
                          'Lithuanian azerty standard': 'lt_std',
                          'Hungarian': 'hu',
                          'Bulgarian': 'bg',
                          'Danish': 'dk',
                          'Belgian': 'be',
                          'U.S. English w/ISO9995-3': 'en_US',
                          'Brazilian': 'br',
                          'Slovenian': 'si',
                          'Italian': 'it',
                          'Romanian': 'ro',
                          'Vietnamese': 'vn',
                          'Estonian': 'ee',
                          'Icelandic': 'is',
                          'Israeli': 'il',
                          'Swedish': 'se'}
       
        keyboard_list = self.keyboard_dict.keys()
        keyboard_list.sort()
        keyboard_combo.set_popdown_strings(keyboard_list)
        #set default to English
        keyboard_combo.list.select_item(43)
        keyboard_combo.entry.set_editable(FALSE)		

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
        timezone_combo.entry.set_editable(FALSE)		

        #bring in signals from glade file
        xml.signal_autoconnect (
                { "on_lang_support_list_select_row" : self.on_lang_support_list_select_row,
                  "on_lang_support_list_unselect_row" : self.on_lang_support_list_unselect_row,
#                  "on_messagebox_button_clicked" : self.on_messagebox_button_clicked,
                  } )

    def on_lang_support_list_select_row(self, *args):
        self.langSupportList.append(self.langDict[self.lang_support_list.get_text(args[1], args[2])])

    def on_lang_support_list_unselect_row(self, *args):
        self.langSupportList.remove(self.langDict[self.lang_support_list.get_text(args[1], args[2])])

#    def on_messagebox_button_clicked(self, *args):
#        print "button clicked"
#        self.messagebox.hide()

    def getData(self):
        data = []
        data.append("")
        data.append("#System language")
        lang = self.languageLookup(self.lang_combo.entry.get_text())
        data.append("lang " + lang)
        data.append("")
        data.append("#Language modules to install")

        if lang not in self.langSupportList:
            self.langSupportList.append(lang)

        if self.langSupportList != []:
            buf = ""
            for lang in self.langSupportList:
                buf = lang + " " + buf
            data.append("langsupport --default " + self.languageLookup(self.lang_combo.entry.get_text()) + " " + buf)
        else:
            data.append("langsupport --default " + self.languageLookup(self.lang_combo.entry.get_text()))

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
            dlg = GnomeMessageBox(_("Please set a root password."),
                                  MESSAGE_BOX_ERROR, STOCK_BUTTON_OK)
            dlg.set_position(WIN_POS_CENTER)
            dlg.show()
            dlg.run_and_close()
            self.root_passwd_entry.grab_focus()
            self.root_passwd_entry.show()
            return
            
        if self.encrypt_root_pw_checkbutton.get_active():
            pure = self.root_passwd_entry.get_text()

            salt = "$1$"
            saltLen = 8

            for i in range(saltLen):
                salt = salt + whrandom.choice (string.letters + string.digits + './')

            self.passwd = crypt.crypt (pure, salt)
            data.append("rootpw --iscrypted " + self.passwd)
            
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


