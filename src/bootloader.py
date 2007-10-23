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

class AbstractBootloader:
    def __init__(self, xml, notebook, ksHandler):
        self.xml = xml
        self.notebook = notebook
        self.ks = ksHandler

    def applyKickstart(self):
        pass

    def enableUpgrade(self, boolean):
        pass

    def formToKickstart(self):
        return 0

    def hide(self):
        pass

    def show(self, platform):
        pass

    def toggled_bootloader(self, args):
        pass

class GrubBootloader(AbstractBootloader):
    def __init__(self, xml, notebook, ksHandler):
        AbstractBootloader.__init__(self, xml, notebook, ksHandler)

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
        self.grub_options_label = xml.get_widget("grub_options_label")
        self.grub_password_checkbutton = xml.get_widget("grub_password_checkbutton")
        self.grub_password_hbox = xml.get_widget("grub_password_hbox")
        self.grub_password_entry = xml.get_widget("grub_password_entry")
        self.grub_password_confirm = xml.get_widget("grub_password_confirm")
        self.grub_password_encrypt_checkbutton = xml.get_widget("grub_password_encrypt_checkbutton")

        self.install_bootloader_radio.connect("toggled", self.toggled_bootloader)
        self.grub_password_checkbutton.connect("toggled", self._toggled_grub_password)

    def _toggled_grub_password(self, args):
        self.grub_password_hbox.set_sensitive(self.grub_password_checkbutton.get_active())

    def applyKickstart(self):
        if self.ks.bootloader.location == "none":
            self.no_bootloader_radio.set_active(True)
        elif self.ks.bootloader.location == "mbr":
            self.mbr_radiobutton.set_active(True)
        elif self.ks.bootloader.location == "partition":
            self.firstsector_radiobutton.set_active(True)

        if self.ks.bootloader.password != "":
            self.grub_password_entry.set_text(self.ks.bootloader.password)
            self.grub_password_confirm.set_text(self.ks.bootloader.password)

        self.parameters_entry.set_text(self.ks.bootloader.appendLine)

        if self.ks.bootloader.md5pass != "":
            self.grub_password_encrypt_checkbutton.set_active(True)
        else:
            self.grub_password_encrypt_checkbutton.set_active(False)

        if self.ks.bootloader.upgrade == True:
            self.upgrade_bootloader_radio.set_active(True)
        else:
            self.upgrade_bootloader_radio.set_active(False)

    def enableUpgrade(self, boolean):
        self.upgrade_bootloader_radio.set_sensitive(not boolean)

    def formToKickstart(self):
        if self.install_bootloader_radio.get_active():
            buf = ""
            if self.mbr_radiobutton.get_active():
                self.ks.bootloader.location = "mbr"
            elif self.firstsector_radiobutton.get_active():
                self.ks.bootloader.location = "partition"

            params = string.strip (self.parameters_entry.get_text())
            self.ks.bootloader.appendLine = params

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
                            self.ks.bootloader.md5pass = unicode(self.passwd, 'iso-8859-1')
                        else:
                            self.ks.bootloader.password = gp
                            self.ks.bootloader.md5pass = ""

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
            else:
                self.ks.bootloader.password = ""
                self.ks.bootloader.md5pass = ""
        elif self.upgrade_bootloader_radio.get_active():
            self.ks.bootloader.upgrade = True
        else:
            self.ks.bootloader.location = "none"
            self.ks.bootloader.password = ""
            self.ks.bootloader.md5pass = ""

        return 0

    def hide(self):
        self.bootloader_vbox.hide()

    def show(self, platform):
        self.bootloader_vbox.show()

    def toggled_bootloader (self, args):
        status = self.install_bootloader_radio.get_active()
        self.parameters_label.set_sensitive(status)
        self.parameters_entry.set_sensitive(status)
        self.mbr_radiobutton.set_sensitive(status)
        self.firstsector_radiobutton.set_sensitive(status)
        self.grub_options_label.set_sensitive(status)
        self.grub_password_checkbutton.set_sensitive(status)
        self.grub_password_entry.set_sensitive(status)
        self.grub_password_confirm.set_sensitive(status)
        self.grub_password_encrypt_checkbutton.set_sensitive(status)

class UnknownBootloader(AbstractBootloader):
    def __init__(self, xml, notebook, ksHandler):
        AbstractBootloader.__init__(self, xml, notebook, ksHandler)

        self.bootloader_label = xml.get_widget("bootloader_label")

    def hide(self):
        self.bootloader_label.hide()

    def show(self, platform):
        self.bootloader_label.set_text(_("Bootloader options are not applicable to "
                                         "the %s platform" % platform))
        self.bootloader_label.show()

class bootloader:
    def __init__(self, xml, notebook, ksHandler):
        self.default = UnknownBootloader(xml, notebook, ksHandler)
        self.blDict = {"x86, AMD64, or Intel EM64T": GrubBootloader(xml, notebook, ksHandler)}
        self._setBl(ksHandler.platform)

    def _setBl(self, platform):
        try:
            self.bl = self.blDict[platform]
        except:
            self.bl = self.default

    def applyKickstart(self):
        self.bl.applyKickstart()

    def enableUpgrade(self, boolean):
        self.bl.enableUpgrade(not boolean)

    def formToKickstart(self):
        return self.bl.formToKickstart()

    def platformTypeChanged(self, platform):
        self.bl.hide()
        self._setBl(platform)
        self.bl.show(platform)

    def updateKS(self, ksHandler):
        self.ks = ksHandler
        self.default.ks = ksHandler

        for bl in self.blDict.values():
            bl.ks = ksHandler
