#!/usr/bin/python

import string
import getopt

class KickstartFile:
    def __init__(self):
        print "starting"
	self.handlers = { 
## 		     "auth"		: self.doAuthconfig	,
## 		     "authconfig"	: self.doAuthconfig	,
## 		     "cdrom"		: None			,
## 		     "clearpart"	: self.doClearPart	,
## 		     "device"		: None			,
## 		     "deviceprobe"	: None			,
## 		     "driverdisk"	: None			,
## 		     "firewall"		: self.doFirewall	,
## 		     "harddrive"	: None			,
## 		     "install"		: None          	,
## 		     "keyboard"		: self.doKeyboard	,
 		     "lang"		: self.doLang		,
##                      "langsupport"	: self.doLangSupport	,
## 		     "lilo"		: self.doLilo		,
##                      "bootloader"       : self.doBootloader     ,
## 		     "lilocheck"	: self.doLiloCheck	,
## 		     "mouse"		: self.doMouse		,
## 		     "network"		: self.doNetwork	,
## 		     "nfs"		: None			,
## 		     "part"		: self.definePartition	,
## 		     "partition"	: self.definePartition	,
## 		     "raid"		: self.defineRaid	,
##                      "volgroup"         : self.defineVolumeGroup,
##                      "logvol"           : self.defineLogicalVolume,
## 		     "reboot"		: self.doReboot		,
## 		     "rootpw"		: self.doRootPw		,
## 		     "skipx"		: self.doSkipX		,
## 		     "text"		: None			,
## 		     "timezone"		: self.doTimezone	,
## 		     "url"		: None			,
## 		     "upgrade"		: self.doUpgrade	,
## 		     "xconfig"		: self.doXconfig	,
## 		     "xdisplay"		: None			,
## 		     "zerombr"		: self.doZeroMbr	,
##                      "interactive"      : self.doInteractive    ,
##                      "autostep"         : self.doAutoStep       ,
##                      "firstboot"        : self.doFirstboot      ,
		   }


        self.readKickstartFile()

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
                    
    def doLang(self, args):
        print "foo", args
                    



KickstartFile()
