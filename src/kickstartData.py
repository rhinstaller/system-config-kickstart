#!/usr/bin/python

class KickstartData:
    def __init__(self):
        self.lang = None
        self.langsupport = None
        self.keyboard = None
        self.mouse = None
        self.timezone = None
        self.rootpw = None
        self.reboot = None
        self.install = None
        self.cdrom = None
        self.bootloader = None
        self.zerombr = None
        self.clearpart = None
        self.network = None
        self.auth = None
        self.firewall = None
        self.skipx = None
        self.packages = None
        self.pre = None
        self.post = None

    def setLang(self, args):
        self.lang = args[0]

    def getLang(self):
        return self.lang

    def setLangsupport(self, args):
        self.langsupport = args

    def getLangsupport(self):
        return self.langsupport
        
    def setKeyboard(self, args):
        self.keyboard = args[0]

    def getKeyboard(self):
        return self.keyboard

    def setMouse(self, args):
        self.mouse = args[0]

    def getMouse(self):
        return self.mouse

    def setTimezone(self, args):
        self.timezone = args

    def getTimezone(self):
        return self.timezone

    def setRootPw(self, args):
        self.rootpw = args

    def getRootPw(self):
        return self.rootpw

    def setReboot(self, args):
        self.reboot = "reboot"

    def getReboot(self):
        return self.reboot 
    
    def setInstall(self, args):
        self.install = "install"

    def getInstall(self):
        return self.install

    def setCdrom(self, args):
        self.cdrom = "cdrom"

    def getCdrom(self):
        return self.cdrom

    def setBootloader(self, args):
        self.bootloader = args

    def getBootloader(self):
        return self.bootloader

    def setZeroMbr(self, args):
        self.zerombr = args

    def getZeroMbr(self):
        return self.zerombr

    def setClearPart(self, args):
        self.clearpart = args

    def getClearPart(self):
        return self.clearpart

    def setNetwork(self, args):
        self.network = args

    def getNetwork(self):
        return self.network

    def setAuth(self, args):
        self.auth = args

    def getAuth(self):
        return self.auth

    def setFirewall(self, args):
        self.firewall = args

    def getFirewall(self):
        return self.firewall

    def setSkipX(self, args):
        self.skipx = args

    def getSkipX(self):
        return self.skipx
