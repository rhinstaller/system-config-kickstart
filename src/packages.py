## Kickstart Configurator - A graphical kickstart file generator
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

# Kickstart package selection UI
# FIXME:  package-level selection and deselection doesn't currently work.

import gtk
import gtk.glade
import gobject
import getopt
import os
import string
import sys
import yum
import yum.Errors
from yum.constants import *
from pirut import GroupSelector

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class sckYumBase(yum.YumBase):
    def log(self, value, msg):
        pass

    def errorlog(self, value, msg):
        pass

    def filelog(self, value, msg):
        pass

    def isPackageInstalled(self, name=None, epoch=None, version=None,
                           release=None, arch=None, po=None):
        if po is not None:
            (name, epoch, version, release, arch) = po.returnNevraTuple()

        installed = False

        lst = self.tsInfo.matchNaevr(name = name, epoch = epoch,
                                     ver = version, rel = release,
                                     arch = arch)
        for txmbr in lst:
            if txmbr.output_state in TS_INSTALL_STATES:
                return True
        if installed and len(lst) > 0:
            # if we get here, then it was installed, but it's in the tsInfo
            # for an erase or obsoleted --> not going to be installed at end
            return False
        return installed

    def isGroupInstalled(self, grp):
        return grp.selected

    def __init__ (self):
        import tempfile

        yum.YumBase.__init__(self)

        # Set up a temporary root for RPM so it thinks there's nothing
        # installed.
        self.temproot = tempfile.mkdtemp(dir="/tmp")
        self.doConfigSetup(root=self.temproot)
        self.conf.installroot = self.temproot

        self.doTsSetup()

        # If we're on a release, we want to try the base repo first.  Otherwise,
        # try development.  If neither of those works, we have a problem.
        if "base" in map(lambda repo: repo.id, self.repos.listEnabled()):
            repoorder = ["base", "development"]
        else:
            repoorder = ["development", "base"]

        self.repos.disableRepo("*")

        try:
            self.repos.enableRepo(repoorder[0])
        except yum.Errors.RepoError:
            try:
                self.repos.enableRepo(repoorder[1])
            except yum.Errors.RepoError:
                print _("system-config-kickstart requires either the base or development yum repository enabled for package selection.  Please enable one of these in /etc/yum.repos.d and restart the program.")
                sys.exit(1)

        self.doRepoSetup()
        self.doGroupSetup()
        self.doSackSetup()

    def cleanup(self):
        for root, dirs, files in os.walk(self.temproot, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(self.temproot)

class Packages:
    def __init__(self, xml, ksdata):
        gsFileName = lambda fn: "/usr/share/pirut/ui/" + fn
        
        self.ksdata = ksdata
        self.y = sckYumBase()
        self.gs = GroupSelector.GroupSelector(self.y, gsFileName)
        self.gs.doRefresh()

        self.package_frame = xml.get_widget("package_frame")
        self.package_frame.add(self.gs.vbox)

        self.detailsButton = self.gs.xml.get_widget("detailsButton")
        self.detailsButton.hide()
        self.optionalLabel = self.gs.xml.get_widget("optionalLabel")
        self.optionalLabel.hide()

    def cleanup(self):
        self.y.cleanup()

    def formToKsdata(self):
        self.ksdata.groupList = []
#        self.ksdata.packageList = []
#        self.ksdata.excludedList = []

        self.y.tsInfo.makelists()
        for txmbr in self.y.tsInfo.getMembers():
#            if txmbr.ts_state == '-':
#                self.ksdata.excludedList.append(txmbr.name)
#                continue
            if txmbr.groups:
                for g in txmbr.groups:
                    grp = self.y.comps.return_group(g)
                    if g not in self.ksdata.groupList:
                        self.ksdata.groupList.append(g)
#                    if txmbr.name in grp.optional_packages.keys():
#                        self.ksdata.packageList.append(txmbr.name)
#            else:
#                self.ksdata.packageList.append(txmbr.name)

    def applyKsdata(self):
#        # We don't really care about invalid names here.  Perhaps we should
#        # at least throw them out of the ksdata lists so they don't keep
#        # coming back?
#        for pkg in self.ksdata.packageList:
#            try:
#                self.y.install(name=pkg)
#            except:
#                pass

        self.y.tsInfo = self.y._transactionDataFactory()

        for grp in self.y.comps.groups:
            if grp.groupid in self.ksdata.groupList:
                self.y.selectGroup(grp.groupid)
            else:
                self.y.deselectGroup(grp.groupid)

#        # This is a whole lot like __deselectPackage in OptionalPackageSelector
#        # in pirut.  If only we could get to that.
#        for pkg in self.ksdata.excludedList:
#            pkgs = self.y.pkgSack.returnNewestByName(pkg)
#            if pkgs:
#                pkgs = self.y.bestPackagesFromList(pkgs)
#            for po in pkgs:
#                txmbrs = self.y.tsInfo.getMembers(pkgtup=po.pkgtup)
#                self.y.tsInfo.remove(po.pkgtup)

        # Refresh UI to get whatever selections the ks file specified.
        self.gs.doRefresh()
