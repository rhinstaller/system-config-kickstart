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

class basic:

    def __init__(self, xml):
        self.lang_combo = xml.get_widget("lang_combo")
        self.lang_support_combo = xml.get_widget("lang_support_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.mouse_combo = xml.get_widget("mouse_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")
        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.lilo_mbr_radiobutton = xml.get_widget("lilo_mbr_radiobutton")
        self.lilo_none_radiobutton = xml.get_widget("lilo_none_radiobutton")
        self.shadow_passwd_checkbutton = xml.get_widget("shadow_passwd_checkbutton")
        self.md5_checkbutton = xml.get_widget("md5_checkbutton")
        self.emulate_3_buttons = xml.get_widget("emulate_3_buttons")

    def getData(self):
        buf = ""
        print self.lang_combo.entry.get_text()
        buf = buf + "\n" + self.languageLookup(self.lang_combo.entry.get_text())
        buf = buf + "\n" + self.languagesupportLookup(self.lang_support_combo.entry.get_text())
        buf = buf + "\n" + "keyboard " + self.keyboard_combo.entry.get_text()
        buf = buf + "\n" + "mouse " + self.mouseLookup(self.mouse_combo.entry.get_text())
        buf = buf + "\n" + "timezone --utc " + self.timezone_combo.entry.get_text()
        buf = buf + "\n" + "rootpw " + self.root_passwd_entry.get_text()
        if self.lilo_mbr_radiobutton.get_active():
            buf = buf + "\n" + "lilo --location mbr"
        elif self.lilo_none_radiobutton.get_active():
            buf = buf + "\n" + "lilo --location none"
        if self.shadow_passwd_checkbutton.get_active():
            buf = buf + " --useshadow"
        if self.md5_checkbutton.get_active():
            buf = buf + " --enablemd5"
        return buf

    def languageLookup(self, args):
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
            if args == 'Japanese':
                    return "lang ja_JP.eucJP"

    def languagesupportLookup(self, args):
            if args == 'Czech':
                    return "langsupport cs_CZ"
            if args == 'English':
                    return "langsupport en_US"
            if args == 'French':
                    return "langsupport fr_FR"
            if args == 'German':
                    return "langsupport de_DE"
            if args == 'Hungarian':
                    return "langsupport hu_HU"
            if args == 'Icelandic':
                    return "langsupport is_IS"
            if args == 'Italian':
                    return "langsupport it_IT"
            if args == 'Norwegian':
                    return "langsupport no_NO"
            if args == 'Romanian':
                    return "langsupport ro_RO"
            if args == 'Russian':
                    return "langsupport ru_RU.K0I8-R"
            if args == 'Serbian':
                    return "langsupport sr_YU"
            if args == 'Slovak':
                    return "langsupport sk_SK"
            if args == 'Slovenian':
                    return "langsupport sl_SI"
            if args == 'Spanish':
                    return "langsupport es_ES"
            if args == 'Swedish':
                    return "langsupport sv_SV"
            if args == 'Turkish':
                    return "langsupport tr_TR"
            if args == 'Ukrainian':
                    return "langsupport uk_UA.KOI8-U"
            if args == 'Japanese':
                    return "langsupport ja_JP.eucJP"

    def keyboardLookup(self, args):
            if args == 'us':
                    return "keyboard us"

    def mouseLookup(self, args):
             buf = ""
#            if args:	
#                    return "mouse generic3ps/2"
             #translate mouse to driver from mouseconfig
                          
             #check emulate 3 buttons checkbutton
             if self.emulate_3_buttons.get_active():
                 buf = buf + "--emulthree"
             return buf

    def timezoneLookup(self, args):
            if args == 'US Eastern':
                    return "timezone --utc US/Eastern"
            elif args == 'US Central':
                    return "timezone --utc US/Central"
            elif args == 'US Mountain':
                    return "timezone --utc US/Mountain"
            elif args == 'US Pacific':
			return "timezone --utc US/Pacific"        

