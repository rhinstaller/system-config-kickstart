#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2008 Red Hat, Inc.
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
sys.path.append('/usr/lib/anaconda')
sys.path.append('/usr/lib/anaconda/iw')
import GroupSelector

from pykickstart.parser import Group

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

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

    def simpleDBInstalled(self, name):
        # FIXME: doing this directly instead of using self.rpmdb.installed()
        # speeds things up by 400%
        mi = self.ts.ts.dbMatch('name', name)
        if mi.count() > 0:
            return True
        return False

    def _pkgExists(self, pkg):
        """Whether or not a given package exists in our universe."""
        try:
            pkgs = self.pkgSack.returnNewestByName(pkg)
            return True
        except yum.Errors.PackageSackError:
            pass
        try:
            pkgs = self.rpmdb.returnNewestByName(pkg)
            return True
        except (IndexError, yum.Errors.PackageSackError):
            pass
        return False

    def _groupHasPackages(self, grp):
        # this checks to see if the given group has any packages available
        # (ie, already installed or in the sack of available packages)
        # so that we don't show empty groups.  also, if there are mandatory
        # packages and we have none of them, don't show
        for pkg in grp.mandatory_packages.keys():
            if self._pkgExists(pkg):
                return True
        if len(grp.mandatory_packages) > 0:
            return False
        for pkg in grp.default_packages.keys() + grp.optional_packages.keys():
            if self._pkgExists(pkg):
                return True
        return False

    def __init__ (self, callback=None):
        import tempfile

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

        try:
            self.doTsSetup()
        except yum.Errors.RepoError, msg:
            text = _("Package selection is disabled due to an error in setup.  Please fix your repository configuration and try again.\n\n%s") % msg
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
            dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
            dlg.set_modal(True)
            rc = dlg.run()
            dlg.destroy()

            self.packagesEnabled = False
            return

        if callback: callback.next_task()

        # If we're on a release, we want to try the base repo first.  Otherwise,
        # try development.  If neither of those works, we have a problem.
        if "fedora" in map(lambda repo: repo.id, self.repos.listEnabled()):
            repoorder = ["fedora", "rawhide", "development"]
        else:
            repoorder = ["rawhide", "development", "fedora"]

        self.repos.disableRepo("*")
        if callback: callback.next_task()

        self.packagesEnabled = False
        for repo in repoorder:
            try:
                self.repos.enableRepo(repo)
                self.packagesEnabled = True
                break
            except yum.Errors.RepoError:
                pass

        if not self.packagesEnabled:
            return

        try:
            self.doRepoSetup()
            if callback: callback.next_task()
            self.doGroupSetup()
            if callback: callback.next_task(next=5)
            self.doSackSetup()
            if callback:
                callback.next_task()
                self.repos.callback = None
        except:
            self.packagesEnabled = False

    def cleanup(self):
        shutil.rmtree(self.temproot)


class Packages:
    def __init__(self, xml, ksHandler, progress_window):
        self.toplevel = xml.get_widget("main_window")
        self.package_frame = xml.get_widget("package_frame")
        self.ks = ksHandler

        if self.ks.upgrade.upgrade:
            disabledLabel = gtk.Label(_("Package configuration is not applicable on upgrades."))
            disabledLabel.set_line_wrap(True)
            self.package_frame.add(disabledLabel)
            self.package_frame.show_all()
            return

        progress_window.set_label(_("Retrieving package information"))
        progress_window.show()
        self.y = sckYumBase(progress_window)

        # If we failed to initialize yum, we should still be able to run
        # the program.  Just disable the package screen.
        if not self.y.packagesEnabled:
            disabledLabel = gtk.Label(_("Package selection is disabled due to problems downloading package information."))
            disabledLabel.set_line_wrap(True)
            self.package_frame.add(disabledLabel)
            self.package_frame.show_all()
            progress_window.hide()
            
            return

        self.gs = GroupSelector.GroupSelector(self.y, lambda fn: "/usr/share/anaconda/ui/" + fn)
        self.gs.doRefresh()

        self.package_frame.add(self.gs.vbox)
        progress_window.hide()

    def updateKS(self, ksHandler):
        self.ks = ksHandler

    def cleanup(self):
        if self.y.packagesEnabled:
            self.y.cleanup()

    def formToKickstart(self):
        if not self.y.packagesEnabled:
            return

        # Don't clear the lists out until now.  This means that if we failed
        # to start yum up, we can still write out the initial %packages
        # section.
        self.ks.packages.groupList = []
        self.ks.packages.packageList = []
        self.ks.packages.excludedList = []

        # Faster to grab all the package names up front rather than call
        # searchNevra in the loop below.
        allPkgNames = map(lambda pkg: pkg.name, self.y.pkgSack.returnPackages())
        allPkgNames.sort()

        self.y.tsInfo.makelists()

        txmbrNames = map (lambda x: x.name, self.y.tsInfo.getMembers())

        for grp in filter(lambda x: x.selected, self.y.comps.groups):
            self.ks.packages.groupList.append(Group(name=grp.groupid))

            defaults = grp.default_packages.keys()
            optionals = grp.optional_packages.keys()

            for pkg in filter(lambda x: x in defaults and (not x in txmbrNames and x in allPkgNames), grp.packages):
                self.ks.packages.excludedList.append(pkg)

            for pkg in filter(lambda x: x in txmbrNames, optionals):
                self.ks.packages.packageList.append(pkg)

    def applyKickstart(self):
        if not self.y.packagesEnabled:
            return

        selectedGroups = map (lambda grp: grp.name, self.ks.packages.groupList)

        for grp in self.y.comps.groups:
            if grp.groupid in selectedGroups:
                self.y.selectGroup(grp.groupid)
            else:
                self.y.deselectGroup(grp.groupid)

        # We don't really care about invalid names here.  Perhaps we should
        # at least throw them out of the packages lists so they don't keep
        # coming back?
        for pkg in self.ks.packages.packageList:
            try:
                self.y.install(name=pkg)
            except:
                pass

        # This is a whole lot like __deselectPackage in OptionalPackageSelector
        # in pirut.  If only we could get to that.
        for pkg in self.ks.packages.excludedList:
            try:
                pkgs = self.y.pkgSack.returnNewestByName(pkg)
            except yum.Errors.PackageSackError:
                continue

            if pkgs:
                pkgs = self.y.bestPackagesFromList(pkgs)
            for po in pkgs:
                txmbrs = self.y.tsInfo.getMembers(pkgtup=po.pkgtup)
                self.y.tsInfo.remove(po.pkgtup)

        # Refresh UI to get whatever selections the ks file specified.
        self.gs.doRefresh()
