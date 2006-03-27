## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
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

import string
import sys
import os
sys.path.append("/usr/share/system-config-language")
import language_backend
import rhpl.keyboard as keyboard

from pykickstart.constants import *

class ProfileSystem:
    def __init__(self, kickstartData):
        self.kickstartData = kickstartData
        self.languageBackend = language_backend.LanguageBackend()
        
        self.getLang()
        self.getKeyboard()
        self.getTimezone()
        self.getRootPassword()
        self.getSELinux()
        self.getPackages()

        self.kickstartData.method["method"] = "cdrom"
        self.kickstartData.upgrade = False
        self.kickstartData.zerombr = True
        self.kickstartData.clearpart["type"] = CLEARPART_TYPE_LINUX

    def getLang(self):
        default, langs = self.languageBackend.getInstalledLangs()
        self.kickstartData.lang = default

    def getKeyboard(self):
        kbd = keyboard.Keyboard()
        kbd.read()
        self.kickstartData.keyboard = kbd.get()

    def getTimezone(self):
        lines = open('/etc/sysconfig/clock', 'r').readlines()

        for line in lines:
            if line[:4] == "ZONE":
                tag, zone = string.split(line, '=')

        zone = string.replace(zone, '"', "")
        zone = string.replace(zone, "'", "")
        zone = string.strip(zone)

        self.kickstartData.timezone["timezone"] = zone
        self.kickstartData.timezone["isUtc"] = False

    def getRootPassword(self):
        if os.access('/etc/shadow', os.R_OK) == 1:
            line = open('/etc/shadow', 'r').readline()
            tokens = string.split(line, ":")
            self.kickstartData.rootpw["isCrypted"] = True
            self.kickstartData.rootpw["password"] = tokens[1]
        else:
            print "no access to /etc/shadow"

    def getSELinux(self):
        lines = os.popen("/usr/sbin/getenforce").readlines()

        if lines[0].lower().startswith("disabled"):
            self.kickstartData.selinux = SELINUX_DISABLED
        elif lines[0].lower().startswith("permissive"):
            self.kickstartData.selinux = SELINUX_PERMISSIVE
        elif lines[0].lower().startswith("enforcing"):
            self.kickstartData.selinux = SELINUX_ENFORCING

    def getPackages(self):
        fd = os.popen("/bin/rpm -qa --queryformat \"%{NAME}\n\"")
        packages = fd.readlines()
        fd.close
        packages.sort()

        for package in packages:
            packages[packages.index(package)] = string.strip(package)

        self.kickstartData.packageList = packages
