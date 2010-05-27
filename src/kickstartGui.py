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

#Patch contributed by Bill Huang - applied on 4/23/2001 for Japanese support

import gtk
import gtk.glade
import gobject
import signal
import basic
import bootloader
import install
import partition
import network
import auth
import firewall
import savefile
import savedialog
import xconfig
import packages
import scripts
import os
import progressWindow
from pykickstart.parser import *
from pykickstart.version import makeVersion

try:
    from gtk import _disable_gdk_threading
    _disable_gdk_threading()
except ImportError:
    pass

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

##
## Icon for windows
##
iconPixbuf = None
try:
    iconPixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/icons/hicolor/48x48/apps/system-config-kickstart.png")

except:
    pass

##
## Texts in about dialog
##

AUTHORS = [
    "Chris Lumens <clumens@redhat.com>",
    "Brent Fox <bfox@redhat.com>",
    "Tammy Fox <tfox@redhat.com>",
    "Roman Rakus <rrakus@redhat.com>",
    ]

LICENSE = _(
    "This program is free software; you can redistribute it and/or modify "
    "it under the terms of the GNU General Public License as published by "
    "the Free Software Foundation; either version 2 of the License, or "
    "(at your option) any later version.\n"
    "\n"
    "This program is distributed in the hope that it will be useful, "
    "but WITHOUT ANY WARRANTY; without even the implied warranty of "
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
    "GNU General Public License for more details.\n"
    "\n"
    "You should have received a copy of the GNU General Public License "
    "along with this program; if not, write to the Free Software "
    "Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.")

COPYRIGHT = '(C) 2000-2009 Red Hat, Inc.'
VERSION = "@VERSION@"
##
## Pull in the Glade file
##
if os.access("system-config-kickstart.glade", os.F_OK):
    xml = gtk.glade.XML ("system-config-kickstart.glade", domain="system-config-kickstart")
else:
    xml = gtk.glade.XML ("/usr/share/system-config-kickstart/system-config-kickstart.glade", domain="system-config-kickstart")

class kickstartGui:
    def destroy(self, args):
        gtk.main_quit()
        self.packages_class.cleanup()

    def __init__ (self, file):
        self.file = file

    def run(self):
        self.ksHandler = makeVersion()

        if self.file:
            self.parser = KickstartParser(self.ksHandler)

            msg = None

            try:
                self.parser.readKickstart(self.file)
            except KickstartError, e:
                if e.value.find("\x00") != -1:
                    msg = _("The kickstart file %s could not be opened.") % self.file
                else:
                    msg = _("The following error was found while parsing your "
                            "kickstart configuration:\n\n%s" % e.value)
            except IOError, e:
                msg = _("The kickstart file %s could not be opened.") % self.file

            if msg:
                dlg = gtk.MessageDialog (None, 0, gtk.MESSAGE_ERROR,
                                         gtk.BUTTONS_OK, msg)
                dlg.set_title(_("Error Parsing Kickstart Config"))
                dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
                dlg.set_modal(True)
                dlg.run()
                dlg.destroy()
                sys.exit(0)

        self.xml = xml
        name_tag = (_("Kickstart"))
        comment_tag = (_("Create a kickstart file"))

	self.toplevel = xml.get_widget("main_window")
	self.toplevel.connect ("destroy", self.destroy)
	self.toplevel.set_icon(iconPixbuf)

	#bring in widgets from glade file
	self.options_notebook = xml.get_widget("options_notebook")
	self.install_radiobutton = xml.get_widget("install_radiobutton")
	self.category_clist = xml.get_widget("category_clist")
        self.open_menu = xml.get_widget("open_menu")
	self.preview_menu = xml.get_widget("preview_menu")
	self.save_menu = xml.get_widget("save_menu")
	self.quit_menu = xml.get_widget("quit_menu")
	self.help_menu = xml.get_widget("help_menu")
	self.about_menu = xml.get_widget("about_menu")

	#populate category list
	self.category_view = xml.get_widget("list_view")
	self.category_store = gtk.ListStore(gobject.TYPE_STRING)
	self.category_view.set_model(self.category_store)
	
	col = gtk.TreeViewColumn(_("Subsection"), gtk.CellRendererText(), text=0)
	col.set_sort_column_id(0)
	self.category_view.append_column(col)
	
	self.category_list = [ (_("Basic Configuration")),
                               (_("Installation Method")),
			       (_("Boot Loader Options")),
                               (_("Partition Information")),
			       (_("Network Configuration")),
                               (_("Authentication")),
			       (_("Firewall Configuration")),
                               (_("Display Configuration")),
			       (_("Package Selection")),
                               (_("Pre-Installation Script")),
			       (_("Post-Installation Script")) ]
		
	for item in self.category_list:
		iter = self.category_store.append()
		self.category_store.set_value(iter, 0, item)

	#bring in basic functions
	self.basic_class = basic.basic(self, xml, self.options_notebook, self.ksHandler)

        # Now that we've loaded the UI elements for the first active thing in the notebook,
        # draw it so we can display a progress bar when yum starts doing stuff.
        self.toplevel.show()
        while gtk.events_pending():
            gtk.main_iteration()

	self.bootloader_class = bootloader.bootloader(xml, self.options_notebook, self.ksHandler)
	self.install_class = install.install(self, xml, self.category_store,
					     self.category_view,
                                             self.options_notebook,
					     self.ksHandler)
	self.partition_class = partition.partition(xml, self.ksHandler)
	self.network_class = network.network(xml, self.ksHandler)
	self.auth_class = auth.auth(xml, self.ksHandler)
	self.firewall_class = firewall.Firewall(xml, self.ksHandler)
	self.X_class = xconfig.xconfig(xml, self.ksHandler)
        self.progress_window = progressWindow.ProgressWindow(self.toplevel)
	self.packages_class = packages.Packages(xml, self.ksHandler, self.progress_window)
	self.scripts_class = scripts.scripts(xml, self.ksHandler)

        self.open_menu.connect("activate", self.on_activate_open)
	self.preview_menu.connect("activate", self.on_activate_preview_options)
	self.save_menu.connect("activate", self.on_activate_save_options)
	self.quit_menu.connect("activate", gtk.main_quit)
	self.help_menu.connect("activate", self.on_help_button_clicked)
	self.about_menu.connect("activate", self.on_about_activate)
	self.category_view.connect("cursor_changed", self.on_list_view_row_activated)
	self.options_notebook.connect("switch-page", self.on_notebook_changed)

	#show gui
        self.applyKickstart()
	self.toplevel.show()

	gtk.main()

    def on_notebook_changed(self, page, data, num):
        count = 0
        iter = self.category_store.get_iter_first()
        if num == 0:
            self.category_view.get_selection().select_iter(iter)
        else:
            while iter:
                if count == num:
                    self.category_view.get_selection().select_iter(iter)
                    self.category_view.show_all()
                iter = self.category_store.iter_next(iter)
                count = count + 1

    def on_list_view_row_activated(self, tree_view):
        data, iter = tree_view.get_selection().get_selected()
	category = self.category_store.get_value(iter, 0)
	row = self.category_list.index(category)
	self.options_notebook.set_current_page(row)

    #about box
    def on_about_activate(self, args):
        dlg = gtk.AboutDialog()
	dlg.set_title(_("About Kickstart Configurator"))
	dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
	dlg.set_transient_for(self.toplevel)
	dlg.set_icon(iconPixbuf)
        dlg.set_version(VERSION)
        dlg.set_authors(AUTHORS)
        dlg.set_license(LICENSE)
        dlg.set_wrap_license(True)
        dlg.set_copyright(COPYRIGHT)
	rc = dlg.run()
        dlg.destroy()

    #display help manual
    def on_help_button_clicked (self, args):
        help_pages = map (lambda str: "file:///usr/share/doc/system-config-kickstart-" + "@VERSION@" + "/system-config-kickstart-" + str + ".html",
                          ["basic", "bootloader", "install", "partitions",
                          "network", "auth", "firewall", "xconfig",
                          "pkgs", "prescript", "postinstall"])
	page = (help_pages [self.options_notebook.get_current_page ()])

	path = "/usr/bin/htmlview"

	if path == None:
	    dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
				    (_("Help is not available.")))
	    dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
	    dlg.set_icon(iconPixbuf)
	    dlg.run()
	    dlg.destroy()
	    return

	pid = os.fork()
	if not pid:
	    os.execv(path, [path, page])

    # Copy possible UI changes back to the kickstartData object.
    def getAllData(self, *args):
        if self.install_class.formToKickstart() is None:
            return None

        if self.bootloader_class.formToKickstart() is None:
            return None

        doInstall = self.install_radiobutton.get_active()

        if self.basic_class.formToKickstart(doInstall) is None:
            return None

        if self.auth_class.formToKickstart() is None:
            return None

	self.network_class.formToKickstart()
	self.firewall_class.formToKickstart()
        self.X_class.formToKickstart()

        #only do these things in installs, not upgrades
	if doInstall:
            self.partition_class.formToKickstart()
            self.packages_class.formToKickstart()

	self.scripts_class.formToKickstart()
        return 0

    def on_activate_open(self, *args):
        fs = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
			  gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        fs.set_default_size(-1, -1)
        fs.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        fs.set_transient_for(self.toplevel)
        result = fs.run()
        file = fs.get_filename()

        if result == gtk.RESPONSE_OK:
            if os.access(file, os.R_OK) == 1:
                self.ksHandler = makeVersion()
                self.parser = KickstartParser(self.ksHandler)

                msg = None

                try:
                    self.parser.readKickstart(file)
                except KickstartError, e:
                    if e.value.find("\x00") != -1:
                        msg = _("The kickstart file %s could not be opened.") % file
                    else:
                        msg = _("The following error was found while parsing your "
                                "kickstart configuration:\n\n%s" % e.value)
                except IOError, e:
                    msg = _("The kickstart file %s could not be opened.") % file

                if msg:
                    dlg = gtk.MessageDialog (None, 0, gtk.MESSAGE_ERROR,
                                             gtk.BUTTONS_OK, msg)
                    dlg.set_title(_("Error Parsing Kickstart Config"))
                    dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
                    dlg.set_modal(True)
                    dlg.run()
                    dlg.destroy()
                    fs.destroy()
                    return

                # Refresh ksdata pointers in every subclass for the new
                # data we loaded in from the file.
                for cl in [self.basic_class, self.bootloader_class,
                           self.install_class, self.partition_class,
                           self.network_class, self.auth_class, self.X_class,
                           self.firewall_class, self.packages_class,
                           self.scripts_class]:
                    cl.updateKS(self.ksHandler)

                self.applyKickstart()
	        self.toplevel.show()
            else:
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                        (_("The file \"%s\" cannot be accessed.")) % file)
                dlg.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
                dlg.set_icon(iconPixbuf)
                dlg.run()
                dlg.destroy()

        fs.destroy()

    #show chosen options for preview
    def on_activate_preview_options (self, *args):
        self.progress_window.set_label(_("Retrieving package information"))
        self.progress_window.show()
        self.progress_window.next_task()
        self.progress_window.hide()

        if self.getAllData() != None:
            previewDialog = savefile.saveFile(self.ksHandler.__str__(),
                                              self.xml)
            previewDialog.run()

    def on_activate_save_options (self, *args):
        self.progress_window.set_label(_("Retrieving package information"))
        self.progress_window.show()
        self.progress_window.next_task()
        self.progress_window.hide()

        if self.getAllData() != None:
            fileDialog = savedialog.saveDialog(self.ksHandler.__str__(),
                                               self.xml)

    def applyKickstart(self):
        self.basic_class.applyKickstart()
        self.install_class.applyKickstart()
        self.bootloader_class.applyKickstart()
        self.partition_class.applyKickstart()
        self.auth_class.applyKickstart()
        self.network_class.applyKickstart()
        self.firewall_class.applyKickstart()
        self.X_class.applyKickstart()
        self.packages_class.applyKickstart()
        self.scripts_class.applyKickstart()

    def platformTypeChanged(self, platform):
        self.bootloader_class.platformTypeChanged(platform)

    def installTypeChanged(self, boolean):
        self.partition_class.setSensitive(boolean)
        self.auth_class.setSensitive(boolean)
        self.X_class.setSensitive(boolean)
        self.firewall_class.setSensitive(boolean)
        self.bootloader_class.enableUpgrade(boolean)
