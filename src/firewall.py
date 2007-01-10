## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003, 2004, 2005, 2006 Red Hat, Inc.
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
import sys
sys.path.append("../../../system-config-securitylevel/head/src")
from securitylevel import xml as selinuxXml
from securitylevel import childWindow as scslWindow
from selinuxPage import selinuxPage
from pykickstart.constants import *

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class selinuxWindow(selinuxPage):
    def __init__(self, xml, doDebug=None, inFirstboot=False):
        selinuxPage.__init__(self, xml, doDebug, inFirstboot)

    def read_selinux_config(self):
        return 0

    def enabled_changed(self, combo):
        pass

    def apply(self, *args):
        self.ks = args[0]

        if self.enabledOptionMenu.get_active() == 0:
            self.ks.selinux.selinux = SELINUX_ENFORCING
        elif self.enabledOptionMenu.get_active() == 1:
            self.ks.selinux.selinux = SELINUX_PERMISSIVE
        elif self.enabledOptionMenu.get_active() == 2:
            self.ks.selinux.selinux = SELINUX_DISABLED

class FirewallWindow(scslWindow):
    def __init__(self):
        scslWindow.__init__(self)

    def apply(self, *args):
        self.ks = args[0]

        self.ks.firewall.trusts = []
        self.ks.firewall.ports = []
        self.ks.firewall.enabled = self.securityOptionMenu.get_active()

        iter = self.incomingList.store.get_iter_first()
        while iter:
            svc = self._getServiceByDesc(self.incomingList.store.get_value(iter, 1))
            if self.incomingList.store.get_value(iter, 0):
                for (port, proto) in svc.ports:
                    self.ks.firewall.ports.append("%s:%s" % (port, proto))

            iter = self.incomingList.store.iter_next(iter)

        model = self.otherPortsView.get_model()
        iter = model.get_iter_first()

        while iter:
            self.ks.firewall.ports.append("%s:%s" % (model.get_value(iter, 0),
                                                     model.get_value(iter, 1)))
            iter = model.iter_next(iter)

class Firewall:
    def __init__(self, xml, ksHandler):
        self.toplevel = xml.get_widget("main_window")
        self.firewall_frame = xml.get_widget("firewall_frame")
        self.ks = ksHandler

        if self.ks.upgrade.upgrade:
            disabledLabel = gtk.Label(_("Firewall configuration is not applicable on upgrades."))
            disabledLabel.set_line_wrap(True)
            self.firewall_frame.add(disabledLabel)
            self.firewall_frame.show_all()
            return

        # Bring in windows from system-config-securitylevel.
        self.scsl_window = FirewallWindow()
        self.selinuxWindow = selinuxWindow(selinuxXml)
        self.scsl_window.setupScreen()
        self.scsl_notebook = self.scsl_window.xml.get_widget("scsNotebook")

        # Set some defaults that can be overridden by applyKsdata later.
        self.scsl_window.securityOptionMenu.set_active(0)
        self.scsl_window.trustedServicesBox.set_sensitive(True)
        self.scsl_window.otherPortsExpander.set_sensitive(True)

        self.scsl_notebook.reparent(self.firewall_frame)
        self.scsl_notebook.show_all()

    def formToKickstart(self):
        if self.ks.upgrade.upgrade:
            return

        self.scsl_window.apply(self.ks)
        self.selinuxWindow.apply(self.ks)

    def applyKickstart(self):
        # If we convert everything into a list of arguments, then
        # system-config-securitylevel already knows how to handle it.
        args = []

        if self.ks.firewall.enabled:
            args.append("--enabled")
        else:
            args.append("--disabled")

        for port in self.ks.firewall.ports:
            args.append("--port=%s" % port)

        if self.ks.selinux.selinux == SELINUX_DISABLED:
            self.selinuxWindow.enabledOptionMenu.set_active(2)
        elif self.ks.selinux.selinux == SELINUX_ENFORCING:
            self.selinuxWindow.enabledOptionMenu.set_active(0)
        elif self.ks.selinux.selinux == SELINUX_PERMISSIVE:
            self.selinuxWindow.enabledOptionMenu.set_active(1)

        self.scsl_window.parseArgList(args)
