## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003 Brent Fox <bfox@redhat.com>

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
import getopt

class KickstartParser:
    def __init__(self, kickstartData, file):
        self.kickstartData = kickstartData

	self.handlers = { 
 		     "auth"		: self.kickstartData.setAuth  	        ,
 		     "authconfig"	: self.kickstartData.setAuth	        ,
                     "bootloader"       : self.kickstartData.setBootloader      ,
 		     "cdrom"		: self.kickstartData.setCdrom           ,
 		     "clearpart"	: self.kickstartData.setClearPart	,
## 		     "device"		: None			,
## 		     "deviceprobe"	: None			,
## 		     "driverdisk"	: None			,
 		     "firewall"		: self.kickstartData.setFirewall	,
                     "firstboot"        : self.kickstartData.setFirstboot       ,
 		     "harddrive"	: self.kickstartData.setHardDrive	,
 		     "install"		: self.kickstartData.setInstall        	,
 		     "keyboard"		: self.kickstartData.setKeyboard	,
# 		     "lang"		: self.kickstartData.setLang		,
       		     "lang"		: self.kickstartData.setLang		,
                     "langsupport"	: self.kickstartData.setLangSupport	,
## 		     "lilo"		: self.kickstartData.setLilo		,

## 		     "lilocheck"	: self.kickstartData.setLiloCheck	,
 		     "mouse"		: self.kickstartData.setMouse		,
 		     "network"		: self.kickstartData.setNetwork	        ,
 		     "nfs"		: self.kickstartData.setNfs		,
 		     "part"		: self.kickstartData.definePartition	,
 		     "partition"	: self.kickstartData.definePartition	,
 		     "raid"		: self.kickstartData.defineRaid	        ,
##                      "volgroup"         : self.defineVolumeGroup,
##                      "logvol"           : self.defineLogicalVolume,
 		     "reboot"		: self.kickstartData.setReboot		,
 		     "rootpw"		: self.kickstartData.setRootPw		,
 		     "skipx"		: self.kickstartData.setSkipX		,
 		     "text"		: self.kickstartData.setText		,
 		     "timezone"		: self.kickstartData.setTimezone	,
 		     "url"		: self.kickstartData.setUrl		,
 		     "upgrade"		: self.kickstartData.setUpgrade	        ,
 		     "xconfig"		: self.kickstartData.setXconfig	        ,
## 		     "xdisplay"		: None			,
 		     "zerombr"		: self.kickstartData.setZeroMbr	,
                     "interactive"      : self.kickstartData.setInteractive     ,
##                      "autostep"         : self.kickstartData.setAutoStep       ,
##                      "firstboot"        : self.kickstartData.setFirstboot      ,
		   }


        self.readKickstartFile(file)

    def readKickstartFile(self, file):
        self.lines = open(file, "r").readlines()
        fd = open(file, "r")
        line = fd.readline()

        mainList = []
        packageList = []
        preList = []
        postList = []

        list = mainList

        #Separate the file into main, package, pre and post lists
        for line in self.lines:
            line = string.strip(line)

            if line == "":
                continue
            elif line[:9] == "%packages":
                list = packageList
            elif line[:4] == "%pre":
                list = preList
            elif line[:5] == "%post":
                list = postList

            list.append(line)

        for line in mainList:
            line = string.strip(line)

            if line == "":
                continue
            elif line[:10] == "#platform=":
                key, value = string.split(line, "=")
                self.kickstartData.setPlatform(value)
            elif line[0] == "#":
                continue
            elif line != "":
                tokens = string.split(line)
                if tokens[0] in self.handlers.keys():
                    if self.handlers[tokens[0]]:
			self.handlers[tokens[0]](tokens[1:])
                    

        if packageList != []:
            tokens = string.split(packageList[0])

            groupList = []
            individualList = []

            for pkg in packageList[1:]:
                if pkg[0] == "@":
                    pkg = string.replace(pkg, "@", "")
                    pkg = string.strip(pkg)

                    if pkg[:10] == "everything":
                        self.kickstartData.setEverything(True)
                        break
                    else:
                        groupList.append(pkg)
                else:
                    individualList.append(pkg)
            
            self.kickstartData.setPackageGroupList(groupList)
            self.kickstartData.setIndividualPackageList(individualList)            

        if preList != []:
            tokens = string.split(preList[0])
            self.kickstartData.setPreLine(tokens[1:])
            self.kickstartData.setPreList(preList[1:])
        
        if postList != []:
            tokens = string.split(postList[0])
            self.kickstartData.setPostLine(tokens[1:])
            self.kickstartData.setPostList(postList[1:])
