#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2008 Red Hat, Inc.
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
import getopt
from pykickstart.constants import *

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

class xconfig:
    def __init__(self, xml, ksHandler):
        self.ks = ksHandler
        self.xconfig_label_box = xml.get_widget("xconfig_label_box")
        self.config_x_button = xml.get_widget("config_x_button")
        self.firstbootLabel = xml.get_widget("firstbootLabel")
        self.firstboot_optionmenu = xml.get_widget("firstboot_optionmenu")

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def setSensitive(self, boolean):
        if boolean == False:
            self.xconfig_label_box.show()
            self.config_x_button.hide()
            self.firstbootLabel.hide()
            self.firstboot_optionmenu.hide()
        else:
            self.xconfig_label_box.hide()
            self.config_x_button.show()
            self.firstbootLabel.show()
            self.firstboot_optionmenu.show()

    def formToKickstart(self):
        if self.ks.upgrade.upgrade == True:
            self.ks.firstboot.firstboot = FIRSTBOOT_SKIP
            return

        if self.config_x_button.get_active():
            if self.firstboot_optionmenu.get_active() == 0:
                self.ks.firstboot.firstboot = FIRSTBOOT_SKIP
            elif self.firstboot_optionmenu.get_active() == 1:
                self.ks.firstboot.firstboot = FIRSTBOOT_DEFAULT
            elif self.firstboot_optionmenu.get_active() == 2:
                self.ks.firstboot.firstboot = FIRSTBOOT_RECONFIG

            self.ks.skipx.skipx = False
        else:
            self.ks.skipx(skipx=True)

        return 0

    def applyKickstart(self):
        if self.ks.skipx.skipx == True:
            self.config_x_button.set_active(False)
        else:
            self.config_x_button.set_active(True)

        if self.ks.firstboot.firstboot == FIRSTBOOT_DEFAULT:
            self.firstboot_optionmenu.set_active(1)
        elif self.ks.firstboot.firstboot == FIRSTBOOT_RECONFIG:
            self.firstboot_optionmenu.set_active(2)
        else:
            self.firstboot_optionmenu.set_active(0)
