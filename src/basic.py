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

from hardwareLists import langDict
from hardwareLists import mouseDict

import kickstartGui

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class basic:

    def __init__(self, xml, store, view, notebook, kickstartData):
        self.store = store
        self.view = view
        self.notebook = notebook
        self.kickstartData = kickstartData
        self.xml = xml
        self.lang_combo = xml.get_widget("lang_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.mouse_combo = xml.get_widget("mouse_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")

        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.emulate_3_buttons = xml.get_widget("emulate_3_buttons")
        self.lang_support_view = xml.get_widget("lang_support_view")
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

        self.langDict = langDict
        self.mouseDict = mouseDict

        #populate language combo
        self.lang_list = self.langDict.keys()
        self.lang_list.sort()
        self.lang_combo.set_popdown_strings(self.lang_list)

        #set default to English
        self.lang_combo.list.select_item(4)
        self.lang_combo.entry.set_editable(gtk.FALSE)

        self.populateLangSupport()
#        for lang in lang_list:
#            self.lang_support_list.append([lang])

        #populate mouse combo
        self.mouse_list = ["Probe for Mouse"]
        dict_list = self.mouseDict.keys()
        dict_list.sort()

        for item in dict_list:
            self.mouse_list.append(item)

        self.mouse_combo.set_popdown_strings(self.mouse_list)
        self.mouse_combo.list.select_item(0)
        self.mouse_combo.entry.set_editable(gtk.FALSE)		

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
        self.keyboard_combo.entry.set_text(self.keyboard_dict[currentKeymap][0])

        #set default mouse to generic ps/2
        self.mouse_combo.list.select_item(8)

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
        self.timezone_combo.entry.set_editable(gtk.FALSE)		

    def langToggled(self, data, row):
        iter = self.lang_support_store.get_iter((int(row),))
        val = self.lang_support_store.get_value(iter, 0)
        self.lang_support_store.set_value(iter, 0 , not val)

    def getData(self, doInstall):
        lang = self.languageLookup(self.lang_combo.entry.get_text())
        self.kickstartData.setLang([self.languageLookup(self.lang_combo.entry.get_text())])

        lang_list = []
        iter = self.lang_support_store.get_iter_first()

        while iter:
            if self.lang_support_store.get_value(iter, 0) == gtk.TRUE:
                lang = self.lang_support_store.get_value(iter, 1) 
                lang_list.append(self.langDict[lang])

            iter = self.lang_support_store.iter_next(iter)

        defaultLang = self.languageLookup(self.lang_combo.entry.get_text())

        self.kickstartData.setLangSupport(lang_list)
        self.kickstartData.setDefaultLang(defaultLang)

        keys = self.keyboard_dict.keys()
        keys.sort()
        for item in keys:
            if self.keyboard_dict[item][0] == self.keyboard_combo.entry.get_text():
                self.kickstartData.setKeyboard([item])
                break

        self.kickstartData.setMouse([self.mouseLookup(self.mouse_combo.entry.get_text())])
        self.kickstartData.setTimezone([self.timezone_combo.entry.get_text()])

        if self.root_passwd_entry.get_text() == "" and doInstall:
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, _("Please select a root password."))
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_icon(kickstartGui.iconPixbuf)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            toplevel = self.xml.get_widget("main_window")
            dlg.set_transient_for(toplevel)
            dlg.run()
            dlg.hide()
            iter = self.store.get_iter_first()
            self.view.get_selection().select_iter(iter)
            self.notebook.set_current_page(0)
            self.root_passwd_entry.grab_focus()
            return None

        if self.encrypt_root_pw_checkbutton.get_active() == gtk.TRUE:
            pure = self.root_passwd_entry.get_text()

            salt = "$1$"
            saltLen = 8

            for i in range(saltLen):
                salt = salt + whrandom.choice (string.letters + string.digits + './')

            self.passwd = crypt.crypt (pure, salt)

            temp = unicode (self.passwd, 'iso-8859-1')
            self.kickstartData.setRootPw(["--iscrypted " + temp])

        else:
            self.passwd = self.root_passwd_entry.get_text()
            self.kickstartData.setRootPw([self.passwd])            

        if self.reboot_checkbutton.get_active():
            self.kickstartData.setReboot("reboot")
        else:
            self.kickstartData.setReboot(None)

        if self.text_install_checkbutton.get_active():
            self.kickstartData.setText("text")
        else:
            self.kickstartData.setText(None)

        if self.interactive_checkbutton.get_active():
            self.kickstartData.setInteractive("interactive")
        else:
            self.kickstartData.setInteractive(None)

        return 0

    def languageLookup(self, args):
        return self.langDict [args]

    def mouseLookup(self, args):
        if args == "Probe for Mouse":
            buf = "#Probe for Mouse"
        else:
            buf = ""
            if self.emulate_3_buttons.get_active() and self.mouseDict[args] != 'none':
                buf = buf + "--emulthree "
            buf = buf + self.mouseDict [args]
        return buf

    def populateLangSupport(self):
        for lang in self.lang_list:
            iter = self.lang_support_store.append()
            self.lang_support_store.set_value(iter, 0, gtk.FALSE)
            self.lang_support_store.set_value(iter, 1, lang)

    def fillData(self):
        #set language
        for lang in self.langDict.keys():
            if self.langDict[lang] == self.kickstartData.getLang():
                self.lang_combo.list.select_item(self.lang_list.index(lang))

        #set keyboard
        self.keyboard_combo.entry.set_text(self.keyboard_dict[self.kickstartData.getKeyboard()][0])

        #set mouse
        for mouse in self.mouseDict.keys():
            mouseLine = self.kickstartData.getMouse()

            if "--emulthree" in mouseLine:
                self.emulate_3_buttons.set_active(gtk.TRUE)
                mouseLine.remove("--emulthree")

            mouseTag = mouseLine[0]
            
            if self.mouseDict[mouse] == mouseTag:
                self.mouse_combo.list.select_item(self.mouse_list.index(mouse))

        #set timezone
        self.timezone_combo.list.select_item(self.timezone_list.index(self.kickstartData.getTimezone()))

        #set the supported lang list
        langSupportList = self.kickstartData.getLangSupport()

        if langSupportList == []:
            while iter:
                self.lang_support_store.set_value(iter, 0, gtk.TRUE)
                iter = self.lang_support_store.iter_next(iter)
        else:
            langSupportList.append(self.kickstartData.getDefaultLang())
            
            iter = self.lang_support_store.get_iter_root()

            while iter:
                if self.langDict[self.lang_support_store.get_value(iter, 1)] in langSupportList:
                    self.lang_support_store.set_value(iter, 0, gtk.TRUE)
                iter = self.lang_support_store.iter_next(iter)


        if self.kickstartData.getReboot():
            self.reboot_checkbutton.set_active(gtk.TRUE)

        if self.kickstartData.getText():
            self.text_install_checkbutton.set_active(gtk.TRUE)

        if self.kickstartData.getInteractive():
            self.interactive_checkbutton.set_active(gtk.TRUE)
