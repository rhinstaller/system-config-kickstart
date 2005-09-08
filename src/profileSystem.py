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

class ProfileSystem:
    def __init__(self, kickstartData):
        self.kickstartData = kickstartData
        self.languageBackend = language_backend.LanguageBackend()
        
        self.getLang()
        self.getKeyboard()
        self.getTimezone()
        self.getRootPassword()
        self.getPackages()

        self.kickstartData.setCdrom("cdrom")
        self.kickstartData.setInstall("install")
        self.kickstartData.setZeroMbr("yes")
        self.kickstartData.setClearPart(["--linux"])

    def getLang(self):
        default, langs = self.languageBackend.getInstalledLangs()
        self.kickstartData.setLang([default])
        self.kickstartData.setDefaultLang(default)
        self.kickstartData.setLangSupport(langs)

    def getKeyboard(self):
        kbd = keyboard.Keyboard()
        kbd.read()
        self.kickstartData.setKeyboard([kbd.get()])

    def getTimezone(self):
        lines = open('/etc/sysconfig/clock', 'r').readlines()

        for line in lines:
            if line[:4] == "ZONE":
                tag, zone = string.split(line, '=')

        zone = string.replace(zone, '"', "")
        zone = string.replace(zone, "'", "")
        zone = string.strip(zone)
        
        self.kickstartData.setTimezone([zone])

    def getRootPassword(self):
        if os.access('/etc/shadow', os.R_OK) == 1:
            line = open('/etc/shadow', 'r').readline()
            tokens = string.split(line, ":")
            passwd = "--iscrypted " + tokens[1]
            self.kickstartData.setRootPw([passwd])
        else:
            print "no access to /etc/shadow"

    def getPackages(self):
        fd = os.popen("/bin/rpm -qa --queryformat \"%{NAME}\n\"")
        packages = fd.readlines()
        fd.close
        packages.sort()

        for package in packages:
            packages[packages.index(package)] = string.strip(package)

        self.kickstartData.setIndividualPackageList(packages)
