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

import string
import sys
import os
sys.path.insert(0, "/usr/share/system-config-language")
import language_backend
from system_config_keyboard import keyboard

from pykickstart.constants import *

class ProfileSystem:
    def __init__(self, ksHandler):
        self.ks = ksHandler
        self.languageBackend = language_backend.LanguageBackend()

        self.getLang()
        self.getKeyboard()
        self.getTimezone()
        self.getRootPassword()
        self.getSELinux()
        self.getPackages()

        self.ks.method(method="cdrom")
        self.ks.zerombr(zerombr=True)
        self.ks.clearpart(type=CLEARPART_TYPE_LINUX)

    def getLang(self):
        default, langs = self.languageBackend.get_installed_langs()
        self.ks.lang(lang=default)

    def getKeyboard(self):
        kbd = keyboard.Keyboard()
        kbd.read()
        self.ks.keyboard(keyboard=kbd.get())

    def getTimezone(self):
        zone = os.path.realpath("/etc/localtime")
        zone = zone.replace("/usr/share/zoneinfo/", "")

        self.ks.timezone(timezone=zone.strip(), isUtc=False)

    def getRootPassword(self):
        if os.access('/etc/shadow', os.R_OK) == 1:
            line = open('/etc/shadow', 'r').readline()
            tokens = string.split(line, ":")
            self.ks.rootpw(isCrypted=True, password=tokens[1])
        else:
            print "no access to /etc/shadow"

    def getSELinux(self):
        lines = os.popen("/usr/sbin/getenforce").readlines()

        if lines[0].lower().startswith("disabled"):
            self.ks.selinux(selinux=SELINUX_DISABLED)
        elif lines[0].lower().startswith("permissive"):
            self.ks.selinux(selinux=SELINUX_PERMISSIVE)
        elif lines[0].lower().startswith("enforcing"):
            self.ks.selinux(selinux=SELINUX_ENFORCING)

    def getPackages(self):
        fd = os.popen("/bin/rpm -qa --queryformat \"%{NAME}\n\"")
        packages = fd.readlines()
        fd.close
        packages.sort()

        for package in packages:
            packages[packages.index(package)] = string.strip(package)

        self.ks.packages.add(packages)
