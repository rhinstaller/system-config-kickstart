## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
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

import string

class KickstartData:
    def __init__(self):
        self.lang = None
        self.langsupport = None
        self.defaultLang = None
        self.keyboard = None
        self.mouse = None
        self.timezone = None
        self.rootpw = None
        self.reboot = None
        self.install = None
        self.interactive = None
        self.text = None
        self.cdrom = None
        self.harddrive = None
        self.nfs = None
        self.url = None
        self.bootloader = None
        self.zerombr = None
        self.clearpart = None
        self.networkList = []
        self.auth = None
        self.firewall = None
        self.skipx = None
        self.package = None
        self.everything = False
        self.pre = None
        self.post = None
        self.upgrade = None
        self.xconfig = None
        self.firstboot = None
        self.partList = []
        self.raidList = []
        self.packageGroupList = []
        self.individualPackageList = []
        self.preLine = None
        self.preList = []
        self.postLine = None
        self.postList = []
        self.platform = "x86, AMD64, or Intel EM64T"

    def setLang(self, args):
        self.lang = args[0]

    def getLang(self):
        return self.lang

    def setLangSupport(self, args):
        list = []

        if args == None:
            self.langsupport = []
            return
        
        for item in args:
            if item[:10] == "--default=":
                self.setDefaultLang(item[10:])
            else:
                list.append(item)

        self.langsupport = list

    def getLangSupport(self):
        return self.langsupport
        
    def setDefaultLang(self, default):
        self.defaultLang = default

    def getDefaultLang(self):
        return self.defaultLang

    def setKeyboard(self, args):
        self.keyboard = args[0]

    def getKeyboard(self):
        return self.keyboard

    def setMouse(self, args):
        self.mouse = args

    def getMouse(self):
        return self.mouse

    def setText(self, args):
        if args == None:
            self.text = None
        else:
            self.text = "text"

    def getText(self):
        return self.text

    def setTimezone(self, args):
        self.timezone = args[-1]

    def getTimezone(self):
        return self.timezone

    def setRootPw(self, args):
        self.rootpw = string.join(args, " ")

    def getRootPw(self):
        return self.rootpw

    def setReboot(self, args):
        if args == None:
            self.reboot = None
        else:
            self.reboot = "reboot"

    def getReboot(self):
        return self.reboot 
    
    def setInstall(self, args):
        if args == None:
            self.install = None
        else:
            self.install = "install"
            self.setUpgrade(None)

    def getInstall(self):
        return self.install

    def setInteractive(self, args):
        if args == None:
            self.interactive = None
        else:
            self.interactive = "interactive"

    def getInteractive(self):
        return self.interactive

    def setCdrom(self, args):
        if args == None:
            self.cdrom = None
        else:
            self.cdrom = "cdrom"
            self.setNfs(None)
            self.setUrl(None)
            self.setHardDrive(None)

    def getCdrom(self):
        return self.cdrom

    def setHardDrive(self, args):
        if args == None:
            self.harddrive = None
        else:
            self.harddrive = args
            self.setNfs(None)
            self.setUrl(None)
            self.setCdrom(None)

    def getHardDrive(self):
        return self.harddrive

    def setNfs(self, args):
        if args == None:
            self.nfs = None
        else:
            self.nfs = args
            self.setHardDrive(None)
            self.setUrl(None)
            self.setCdrom(None)

    def getNfs(self):
        return self.nfs

    def setUrl(self, args):
        if args == None:
            self.url = None
        else:
            self.url = args[1]
            self.setNfs(None)
            self.setHardDrive(None)
            self.setCdrom(None)

    def getUrl(self):
        return self.url

    def setBootloader(self, args):
        self.bootloader = args

    def getBootloader(self):
        return self.bootloader

    def setZeroMbr(self, args):
        if args == None:
            self.zerombr = None
        else:
            self.zerombr = "yes"

    def getZeroMbr(self):
        return self.zerombr

    def setClearPart(self, args):
        if args == None:
            self.clearpart = None
        else:
            self.clearpart = args

    def getClearPart(self):
        return self.clearpart

    def setNetwork(self, args):
        self.networkList.append(args)

    def getNetwork(self):
        return self.networkList

    def clearNetwork(self):
        self.networkList = []

    def setAuth(self, args):
        self.auth = args

    def getAuth(self):
        return self.auth

    def setFirewall(self, args):
        self.firewall = args

    def getFirewall(self):
        return self.firewall

    def setSkipX(self, args):
        if args == None:
            self.skipx = None
        else:
            self.skipx = "skipx"

    def getSkipX(self):
        return self.skipx

    def setUpgrade(self, args):
        if args == None:
            self.upgrade = None
        else:
            self.upgrade = "upgrade"
            self.setInstall(None)

    def getUpgrade(self):
        return self.upgrade

    def definePartition(self, args):
        self.partList.append(args)

    def getPartitions(self):
        return self.partList

    def clearPartList(self):
        self.partList = []

    def defineRaid(self, args):
        self.raidList.append(args)

    def getRaid(self):
        return self.raidList

    def clearRaidList(self):
        self.raidList = []

    def setXconfig(self, args):
        if args == None:
            self.xconfig = None
        else:
            self.xconfig = args

    def getXconfig(self):
        return self.xconfig

    def setFirstboot(self, args):
        if args == None:
            self.firstboot = None
        else:
            self.firstboot = args[0]

    def getFirstboot(self):
        return self.firstboot

    def setEverything(self, args):
        self.everything = args

    def getEverything(self):
        return self.everything

    def setPackageGroupList(self, args):
        self.packageGroupList = args

    def getPackageGroupList(self):
        return self.packageGroupList

    def setIndividualPackageList(self, args):
        self.individualPackageList = args

    def getIndividualPackageList(self):
        return self.individualPackageList

    def setPreLine(self, args):
        if args == None:
            self.preLine = None
        else:
            self.preLine = args

    def getPreLine(self):
        return self.preLine

    def setPreList(self, args):
        self.preList = args

    def getPreList(self):
        return self.preList

    def setPostLine(self, args):
        if args == None:
            self.postLine = None
        else:
            self.postLine = args

    def getPostLine(self):
        return self.postLine

    def setPostList(self, args):
        self.postList = args

    def getPostList(self):
        return self.postList

    def setPlatform(self, platform):
        self.platform = platform

    def getPlatform(self):
        return self.platform

    def getAll(self):
        file = []

        file.append("#Generated by Kickstart Configurator")
        file.append("#platform=%s\n" % self.platform)
        file.append("#System  language")
        file.append("lang %s" % self.getLang())

        file.append("#Language modules to install")
        if len(self.langsupport) == 0:
            file.append("langsupport " + self.getDefaultLang())

        elif len(self.langsupport) == 1:
            if self.getDefaultLang() in self.getLangSupport():
                file.append("langsupport " + self.langsupport[0])
            else:
                file.append("langsupport " + self.langsupport[0] + " --default=" + self.getDefaultLang())

        elif len(self.langsupport) > 1:
            if self.getDefaultLang() in self.getLangSupport():
                self.langsupport.remove(self.getDefaultLang())
                            
            list = string.join(self.langsupport, " ")
            file.append("langsupport " + list + " --default=" + self.getDefaultLang())

        file.append("#System keyboard")
        file.append("keyboard " + self.getKeyboard())
        file.append("#System mouse")

        mouse = self.getMouse()
        try:
            file.append("mouse " + string.join(mouse), " ")
        except:
            file.append("mouse")
        file.append("#Sytem timezone")
        file.append("timezone " + self.getTimezone())
        file.append("#Root password")
        file.append("rootpw " + self.getRootPw())

        
        if self.getReboot():
            file.append("#Reboot after installation")
            file.append(self.getReboot())

        if self.getText():
            file.append("#Use text mode install")
            file.append(self.getText())

        if self.getInteractive():
            file.append("#Use interactive kickstart installation method")
            file.append(self.getInteractive())

        if self.getInstall():
            file.append("#Install OS instead of upgrade")
            file.append(self.getInstall())

        elif self.getUpgrade():
            file.append("#Upgrade existing installation")
            file.append(self.getUpgrade())

        if self.getCdrom():
            file.append("#Use CDROM installation media")
            file.append(self.getCdrom())

        elif self.getNfs():
            file.append("#Use NFS installation Media")
            file.append("nfs " +  string.join(self.getNfs()," "))

        elif self.getHardDrive():
            file.append("#Use hard drive installation media")
            file.append("harddrive " + self.getHardDrive())

        elif self.getUrl():
            file.append("#Use Web installation")
            file.append("url --url " + self.getUrl())
            pass

        if self.getBootloader():
            file.append("#System bootloader configuration")
            file.append("bootloader " + string.join(self.getBootloader(), " "))

        if self.getZeroMbr():
            file.append("#Clear the Master Boot Record")
            file.append("zerombr " + self.getZeroMbr())

        if self.getClearPart():
            file.append("#Partition clearing information")
            file.append("clearpart " + string.join(self.getClearPart(), " "))

        if self.getPartitions() != []:
            file.append("#Disk partitioning information")
            for line in self.getPartitions():
                tokens = string.split(string.strip(line[0]))
                if tokens[0] == "raid":
                    file.append(string.join(line, " "))
                else:
                    file.append("part " + string.join(line, " "))

        if self.getAuth():
            file.append("#System authorization infomation")
            file.append("auth " + string.join(self.getAuth(), " "))

        if self.getNetwork():
            file.append("#Network information")
            for line in self.networkList:
                file.append("network " + string.join(line, " "))

        if self.getFirewall():
            file.append("#Firewall configuration")
            file.append("firewall " + string.join(self.getFirewall(), " "))

        if self.getXconfig():
            file.append("#XWindows configuration information")
            file.append("xconfig " + string.join(self.getXconfig(), " "))

        if self.getFirstboot():
            file.append("#Run the Setup Agent on first boot")
            file.append("firstboot " + self.getFirstboot())

        if self.getSkipX():
            file.append("#Do not configure XWindows")
            file.append("skipx")

        if self.getEverything() == True:
            file.append("#Package install information")
            file.append("%packages\n@everything")
        elif self.getPackageGroupList() != [] or self.getIndividualPackageList() != []:
            file.append("#Package install information")
            file.append("%packages")

            if self.getPackageGroupList() != []:
                for package in self.getPackageGroupList():
                    file.append("@ %s" % package)

            if self.getIndividualPackageList() != []:
                for package in self.getIndividualPackageList():
                    file.append(package)

        if self.getPreLine():
            file.append("%pre " + self.getPreLine())

            if self.getPreList != []:
                for line in self.getPreList():
                    file.append(line)
        else:
            if self.getPreList() != []:
                file.append("%pre")
                for line in self.getPreList():
                    file.append(line)

        if self.getPostLine():
            file.append("%post " + self.getPostLine())

            if self.getPostList != []:
                for line in self.getPostList():
                    file.append(line)

        else:
            if self.getPostList() != []:
                file.append("%post")
                for line in self.getPostList():
                    file.append(line)

        return file

    def printData(self):
        file = self.getAll()
        for line in file:
            print line
