#!/usr/bin/python

import string
import getopt
import kickstartData

class KickstartFile:
    def __init__(self):
        print "starting"

        self.kickstartData = kickstartData.KickstartData()

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
## 		     "harddrive"	: None			,
 		     "install"		: self.kickstartData.setInstall        	,
 		     "keyboard"		: self.kickstartData.setKeyboard	,
# 		     "lang"		: self.kickstartData.setLang		,
       		     "lang"		: self.kickstartData.setLang		,
                     "langsupport"	: self.kickstartData.setLangsupport	,
## 		     "lilo"		: self.kickstartData.setLilo		,

## 		     "lilocheck"	: self.kickstartData.setLiloCheck	,
 		     "mouse"		: self.kickstartData.setMouse		,
 		     "network"		: self.kickstartData.setNetwork	        ,
## 		     "nfs"		: None			,
## 		     "part"		: self.definePartition	,
## 		     "partition"	: self.definePartition	,
## 		     "raid"		: self.defineRaid	,
##                      "volgroup"         : self.defineVolumeGroup,
##                      "logvol"           : self.defineLogicalVolume,
 		     "reboot"		: self.kickstartData.setReboot		,
 		     "rootpw"		: self.kickstartData.setRootPw		,
 		     "skipx"		: self.kickstartData.setSkipX		,
## 		     "text"		: None			,
 		     "timezone"		: self.kickstartData.setTimezone	,
## 		     "url"		: None			,
## 		     "upgrade"		: self.kickstartData.setUpgrade	,
## 		     "xconfig"		: self.kickstartData.setXconfig	,
## 		     "xdisplay"		: None			,
 		     "zerombr"		: self.kickstartData.setZeroMbr	,
##                      "interactive"      : self.kickstartData.setInteractive    ,
##                      "autostep"         : self.kickstartData.setAutoStep       ,
##                      "firstboot"        : self.kickstartData.setFirstboot      ,
		   }


        self.readKickstartFile()
        print "Lang is", self.kickstartData.getLang()
        print "Langsupport is", self.kickstartData.getLangsupport()
        print "Keyboard is", self.kickstartData.getKeyboard()
        print self.kickstartData.getMouse()
        print self.kickstartData.getTimezone()        

    def readKickstartFile(self):
        self.lines = open("ks.cfg", "r").readlines()
#        print self.lines

        for line in self.lines:
            line = string.strip(line)

            if line == "":
                continue
            elif line[0] == "#":
                continue
            elif line != "":
                tokens = string.split(line)
                print tokens
                if tokens[0] in self.handlers.keys():
                    if self.handlers[tokens[0]]:
			self.handlers[tokens[0]](tokens[1:])                        
                    

KickstartFile()
