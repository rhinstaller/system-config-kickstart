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
import shutil
import string
import sys
import yum
import yum.Errors
from yum.constants import *
from yum.misc import getCacheDir
from pirut import GroupSelector, PirutProgressCallback

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class sckGroupSelector(GroupSelector.GroupSelector):
    def __doGroupPopup(self, button, time):
        pass

    def _groupListButtonPress(self, widget, event):
        pass

    def _groupListPopup(self, widget):
        pass

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

    def __init__ (self, callback=None):
        import tempfile

        self.packagesEnabled = True

        yum.YumBase.__init__(self)

        if callback:
            callback.log = self.log
            self.repos.callback = callback

        # Set up a temporary root for RPM so it thinks there's nothing
        # installed, but don't use it until after we set up the config info.
        # We need to find the fedora-release package in the real root so
        # we can set $releasever and other variables from /etc/yum.repos.d/*
        # (#190999).
        self.temproot = tempfile.mkdtemp(dir="/tmp")
        self.doConfigSetup(init_plugins=False)
        if os.geteuid() != 0:
            cachedir = getCacheDir()
            if cachedir is None:
                self.errorlog("0, Error: Could not make cachedir, exiting")
                sys.exit(1)
            self.repos.setCacheDir(cachedir)

        if callback: callback.next_task()
        self.conf.installroot = self.temproot

        self.doTsSetup()
        if callback: callback.next_task()

        # If we're on a release, we want to try the base repo first.  Otherwise,
        # try development.  If neither of those works, we have a problem.
        if "base" in map(lambda repo: repo.id, self.repos.listEnabled()):
            repoorder = ["core", "base", "development"]
        else:
            repoorder = ["development", "core", "base"]

        self.repos.disableRepo("*")
        if callback: callback.next_task()

        enabledBaseRepo = False
        for repo in repoorder:
            try:
                self.repos.enableRepo(repo)
                enabledBaseRepo = True
            except yum.Errors.RepoError:
                pass

        if not enabledBaseRepo:
            self.packagesEnabled = False
            return

        self.doRepoSetup()
        if callback: callback.next_task()
        self.doGroupSetup()
        if callback: callback.next_task(next=5)
        self.doSackSetup()
        if callback:
            callback.next_task()
            self.repos.callback = None

    def cleanup(self):
        shutil.rmtree(self.temproot)

class Packages:
    def __init__(self, xml, ksdata):
        self.toplevel = xml.get_widget("main_window")
        self.package_frame = xml.get_widget("package_frame")
        self.ksdata = ksdata
        pbar = PirutProgressCallback(_("Retrieving package information"),
                                     self.toplevel, num_tasks=10)
        pbar.show()

        self.y = sckYumBase(pbar)

        # If we failed to initialize yum, we should still be able to run
        # the program.  Just disable the package screen.
        if not self.y.packagesEnabled:
            disabledLabel = gtk.Label(_("Package selection is disabled due to problems downloading package information."))
            disabledLabel.set_line_wrap(True)
            self.package_frame.add(disabledLabel)
            self.package_frame.show_all()
            pbar.destroy()
            return

        self.gs = sckGroupSelector(self.y, lambda fn: "/usr/share/pirut/ui/" + fn)
        self.gs.doRefresh()
        pbar.destroy()

        self.package_frame.add(self.gs.vbox)

        self.detailsButton = self.gs.xml.get_widget("detailsButton")
        self.detailsButton.hide()
        self.optionalLabel = self.gs.xml.get_widget("optionalLabel")
        self.optionalLabel.hide()

    def cleanup(self):
        if self.y.packagesEnabled:
            self.y.cleanup()

    def formToKsdata(self):
        self.ksdata.groupList = []
#        self.ksdata.packageList = []
#        self.ksdata.excludedList = []

        if not self.y.packagesEnabled:
            return

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

        if not self.y.packagesEnabled:
            return

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
