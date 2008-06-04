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

sys.path.append("/usr/share/system-config-date")


class basic:
    def __init__(self, parent_class, xml, notebook, ksHandler):
        self.parent_class = parent_class
        self.notebook = notebook
        self.ks = ksHandler
        self.xml = xml
        self.lang_combo = xml.get_widget("lang_combo")
        self.keyboard_combo = xml.get_widget("keyboard_combo")
        self.timezone_combo = xml.get_widget("timezone_combo")
        self.utc_check_button = xml.get_widget("utc_check_button")

        self.root_passwd_entry = xml.get_widget("root_passwd_entry")
        self.root_passwd_confirm_entry = xml.get_widget("root_passwd_confirm_entry")
        self.reboot_checkbutton = xml.get_widget("reboot_checkbutton")
        self.text_install_checkbutton = xml.get_widget("text_install_checkbutton")
        self.ks.bootloader(md5pass="", password="")
        self.interactive_checkbutton = xml.get_widget("interactive_checkbutton")
        self.encrypt_root_pw_checkbutton = xml.get_widget("encrypt_root_pw_checkbutton")
        self.lang_support_list = xml.get_widget("lang_support_list")
        self.platform_combo = xml.get_widget("platform_combo")

        self.platform_list =  [_("x86, AMD64, or Intel EM64T"), _("Intel Itanium"), _("IBM iSeries"),
                               _("IBM pSeries"), _("IBM zSeries/s390")]
        self.platform_combo.set_popdown_strings(self.platform_list)
        self.platform_combo.entry.connect("changed", self.platformChanged)

        self.key_checkbutton = xml.get_widget("key_checkbutton")
        self.key_entry = xml.get_widget("key_entry")
        self.key_checkbutton.connect("toggled", self.keyChanged)

        self.langDict = langDict

        # set a default platform
        if not self.ks.platform:
            self.ks.platform = "x86, AMD64, or Intel EM64T"

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
        import zonetab

        zt = zonetab.ZoneTab()
        self.timezone_list = [ x.tz for x in zt.getEntries() ]
        self.timezone_list.sort()

        try:
            select = self.timezone_list.index("America/New_York")
        except:
            select = 0

        self.timezone_combo.set_popdown_strings(self.timezone_list)
        self.timezone_combo.list.select_item(select)

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def formToKickstart(self, doInstall):
        self.ks.lang(lang=self.languageLookup(self.lang_combo.entry.get_text()))

        keys = self.keyboard_dict.keys()
        keys.sort()
        for item in keys:
            if self.keyboard_dict[item][0] == self.keyboard_combo.entry.get_text():
                self.ks.keyboard(keyboard=item)
                break

        self.ks.timezone(timezone=self.timezone_combo.entry.get_text(), isUtc=self.utc_check_button.get_active())

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

        pure = self.root_passwd_entry.get_text()

        if pure != "":
            if self.encrypt_root_pw_checkbutton.get_active() == True:
                salt = "$1$"
                saltLen = 8

                if not pure.startswith(salt):
                    for i in range(saltLen):
                        salt = salt + random.choice (string.letters + string.digits + './')

                    self.passwd = crypt.crypt (pure, salt)

                    temp = unicode (self.passwd, 'iso-8859-1')
                    self.ks.rootpw(isCrypted=True, password=temp)
                else:
                    self.ks.rootpw(isCrypted=True, password=pure)
            else:
                self.passwd = self.root_passwd_entry.get_text()
                self.ks.rootpw(isCrypted=False, password=self.passwd)

        self.ks.platform = self.platform_combo.entry.get_text()

        if self.reboot_checkbutton.get_active():
            self.ks.reboot(action=KS_REBOOT)
        else:
            self.ks.reboot(action=KS_WAIT)

        if self.text_install_checkbutton.get_active():
            self.ks.displaymode(displayMode=DISPLAY_MODE_TEXT)
        else:
            self.ks.displaymode(displayMode=DISPLAY_MODE_GRAPHICAL)

        self.ks.interactive(interactive=self.interactive_checkbutton.get_active())

        if self.key_checkbutton.get_active():
            if self.key_entry.get_text() == "":
                self.ks.key(key=KS_INSTKEY_SKIP)
            else:
                self.ks.key(key=self.key_entry.get_text())
        else:
            self.ks.key(key="")

        return 0

    def languageLookup(self, args):
        return self.langDict [args]

    def platformChanged(self, entry):
        platform = entry.get_text()
        if platform:
            self.parent_class.platformTypeChanged(entry.get_text())

    def keyChanged(self, args):
        self.key_entry.set_sensitive(self.key_checkbutton.get_active())

    def applyKickstart(self):
        if self.ks.platform in self.platform_list:
            self.platform_combo.entry.set_text(self.ks.platform)

        if self.ks.lang.lang.find (".") != -1:
            ksLang = self.ks.lang.lang.split(".")[0]
        else:
            ksLang = self.ks.lang.lang

        for lang in self.langDict.keys():
            if self.langDict[lang] == ksLang:
                self.lang_combo.list.select_item(self.lang_list.index(lang))

        if self.ks.keyboard.keyboard != "":
            self.keyboard_combo.entry.set_text(self.keyboard_dict[self.ks.keyboard.keyboard][0])

        if self.ks.timezone.timezone != "":
            self.timezone_combo.list.select_item(self.timezone_list.index(self.ks.timezone.timezone))

        self.reboot_checkbutton.set_active(self.ks.reboot.action == KS_REBOOT)

        if self.ks.displaymode.displayMode == DISPLAY_MODE_TEXT:
            self.text_install_checkbutton.set_active(True)

        if self.ks.interactive.interactive == True:
            self.interactive_checkbutton.set_active(True)

        if self.ks.rootpw.password != "":
            self.root_passwd_entry.set_text(self.ks.rootpw.password)
            self.root_passwd_confirm_entry.set_text(self.ks.rootpw.password)
            self.encrypt_root_pw_checkbutton.set_active(self.ks.rootpw.isCrypted)

        if self.ks.key.key == "":
            self.key_checkbutton.set_active(False)
            self.key_entry.set_text("")
        elif self.ks.key.key == KS_INSTKEY_SKIP:
            self.key_checkbutton.set_active(True)
            self.key_entry.set_text("")
        else:
            self.key_checkbutton.set_active(True)
            self.key_entry.set_text(self.ks.key.key)
