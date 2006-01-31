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

## Authors: Brent Fox <bfox@redhat.com>
##          Tammy Fox <tfox@redhat.com>

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
from pykickstart.parser import *
from pykickstart.data import KickstartData

try:
    from gtk import _disable_gdk_threading
    _disable_gdk_threading()
except ImportError:
    pass

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

##
## Icon for windows
##
iconPixbuf = None      
try:
    iconPixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/system-config-kickstart/pixmaps/system-config-kickstart.png")
     
except:
    pass

##
## Pull in the Glade file
##
if os.access("system-config-kickstart.glade", os.F_OK):
    xml = gtk.glade.XML ("system-config-kickstart.glade", domain=domain)
else:
    xml = gtk.glade.XML ("/usr/share/system-config-kickstart/system-config-kickstart.glade", domain=domain)

class kickstartGui:
    def destroy(self, args):
        gtk.main_quit()
        self.packages_class.cleanup()

    def __init__ (self, file):
        self.kickstartData = KickstartData()

        if file:
            self.kickstartHandlers = KickstartHandlers(self.kickstartData)
            self.parser = KickstartParser (self.kickstartData,
                                           self.kickstartHandlers)
            self.parser.readKickstart(file)

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

	#bring in basic functions
	self.basic_class = basic.basic(self, xml, self.options_notebook, self.kickstartData)
        
	#bring in bootloader functions
	self.bootloader_class = bootloader.bootloader(xml, self.options_notebook, self.kickstartData)
                                                      
	#bring in install functions
	self.install_class = install.install(self, xml, self.category_store,
					     self.category_view, self.options_notebook,
					     self.kickstartData)
	#bring in partitions functions
	self.partition_class = partition.partition(xml, self.kickstartData)
	#bring in network functions
	self.network_class = network.network(xml, self.kickstartData)
	#bring in auth functions
	self.auth_class = auth.auth(xml, self.kickstartData)
	#bring in firewall functions
	self.firewall_class = firewall.firewall(xml, self.kickstartData)
	#bring in X functions
	self.X_class = xconfig.xconfig(xml, self.kickstartData)
	#bring in package function
	self.packages_class = packages.Packages(xml, self.kickstartData)
	#bring in scripts function
	self.scripts_class = scripts.scripts(xml, self.kickstartData)
	
	col = gtk.TreeViewColumn(_("Subsection"), gtk.CellRendererText(), text=0)
	col.set_sort_column_id(0)
	self.category_view.append_column(col)
	
	self.category_list = [ (_("Basic Configuration")), (_("Installation Method")),
			       (_("Boot Loader Options")), (_("Partition Information")),
			       (_("Network Configuration")), (_("Authentication")),
			       (_("Firewall Configuration")), (_("Display Configuration")),
			       (_("Package Selection")), (_("Pre-Installation Script")),
			       (_("Post-Installation Script")) ]
		
	for item in self.category_list:
		iter = self.category_store.append()
		self.category_store.set_value(iter, 0, item)

        self.open_menu.connect("activate", self.on_activate_open)
	self.preview_menu.connect("activate", self.on_activate_preview_options)
	self.save_menu.connect("activate", self.on_activate_save_options)
	self.quit_menu.connect("activate", gtk.main_quit)
	self.help_menu.connect("activate", self.on_help_button_clicked)
	self.about_menu.connect("activate", self.on_about_activate)
	self.category_view.connect("cursor_changed", self.on_list_view_row_activated)
	self.options_notebook.connect("switch-page", self.on_notebook_changed)
            
	#show gui
        self.applyKsdata()
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
        dlg = gtk.MessageDialog (None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
				 _("Kickstart Configurator @VERSION@\n Copyright (c) 2000-2002 Red Hat, Inc.\n Copyright (c) 2000-2002 Brent Fox <bfox@redhat.com>\n Copyright (c) 2000-2002 Tammy Fox <tfox@redhat.com>\n A graphical interface for creating a kickstart file"))
	dlg.set_title(_("About Kickstart Configurator"))
	dlg.set_default_size(100, 100)
	dlg.set_position (gtk.WIN_POS_CENTER)
	dlg.set_border_width(2)
	dlg.set_modal(True)
	dlg.set_transient_for(self.toplevel)
	dlg.set_icon(iconPixbuf)
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
	    dlg.set_position(gtk.WIN_POS_CENTER)
	    dlg.set_icon(iconPixbuf)
	    dlg.run()
	    dlg.destroy()
	    return

	pid = os.fork()
	if not pid:
	    os.execv(path, [path, page])

    # Copy possible UI changes back to the kickstartData object.
    def getAllData(self, *args):
        if self.install_class.formToKsdata() is None:
            return None
        
        if self.bootloader_class.formToKsdata() is None:
            return None

        doInstall = self.install_radiobutton.get_active()

        if self.basic_class.formToKsdata(doInstall) is None:
            return None

        if self.auth_class.formToKsdata() is None:
            return None

	self.network_class.formToKsdata()
	self.firewall_class.formToKsdata()
	self.X_class.formToKsdata()

        #only do these things in installs, not upgrades
	if doInstall:
            self.partition_class.formToKsdata()
            self.packages_class.formToKsdata()

	self.scripts_class.formToKsdata()
        return 0

    def on_activate_open(self, *args):
        fs = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_OPEN,
                 buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
			  gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        result = fs.run()
        file = fs.get_filename()

        if result == gtk.RESPONSE_OK:
            if os.access(file, os.R_OK) == 1:
                self.kickstartData = KickstartData()
                self.kickstartHandlers = KickstartHandlers(self.kickstartData)
                self.parser = KickstartParser (self.kickstartData,
                                               self.kickstartHandlers)
                self.parser.readKickstart(file)

                # Refresh ksdata pointers in every subclass for the new
                # data we loaded in from the file.
                for cl in [self.basic_class, self.bootloader_class,
                           self.install_class, self.partition_class,
                           self.network_class, self.auth_class, self.X_class,
                           self.firewall_class, self.packages_class,
                           self.scripts_class]:
                    cl.ksdata = self.kickstartData

                self.applyKsdata()
	        self.toplevel.show()
            else:
                dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,
                                        (_("The file \"%s\" cannot be accessed.")) % file)
                dlg.set_position(gtk.WIN_POS_CENTER)
                dlg.set_icon(iconPixbuf)
                dlg.run()
                dlg.destroy()

        fs.destroy()

    #show chosen options for preview
    def on_activate_preview_options (self, *args):
        if self.getAllData() != None:
            from pykickstart.writer import KickstartWriter
            writer = KickstartWriter(self.kickstartData)
            previewDialog = savefile.saveFile (writer.write(), self.xml)

    def on_activate_save_options (self, *args):
        if self.getAllData() != None:
            from pykickstart.writer import KickstartWriter
            writer = KickstartWriter(self.kickstartData)
            fileDialog = savedialog.saveDialog(writer.write(), self.xml)

    def applyKsdata(self):
        self.basic_class.applyKsdata()
        self.install_class.applyKsdata()
        self.bootloader_class.applyKsdata()
        self.partition_class.applyKsdata()
        self.auth_class.applyKsdata()
        self.network_class.applyKsdata()
        self.firewall_class.applyKsdata()
        self.X_class.applyKsdata()
        self.packages_class.applyKsdata()
        self.scripts_class.applyKsdata()

    def platformTypeChanged(self, platform):
        self.bootloader_class.platformTypeChanged(platform)

    def installTypeChanged(self, boolean):
        self.partition_class.setSensitive(boolean)
        self.packages_class.setSensitive(boolean)
        self.auth_class.setSensitive(boolean)
        self.firewall_class.setSensitive(boolean)
        self.X_class.setSensitive(boolean)
        self.bootloader_class.enableUpgradeRadio(boolean)
