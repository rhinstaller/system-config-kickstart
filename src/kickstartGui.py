#!/usr/bin/python2.2

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002 Brent Fox <bfox@redhat.com>
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
import helpBrowser
import os
import kickstartData
import kickstartParser

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

##
## Icon for windows
##

iconPixbuf = None      
try:
    iconPixbuf = gtk.gdk.pixbuf_new_from_file("/usr/share/redhat-config-kickstart/pixmaps/redhat-config-kickstart.png")
     
except:
    pass

class kickstartGui:
	
    def destroy(self, args):
        gtk.mainquit()

    def __init__ (self, xml, file):
        self.xml = xml

        self.kickstartData = kickstartData.KickstartData()

	self.toplevel = xml.get_widget("main_window")
	self.toplevel.connect ("destroy", self.destroy)
	self.toplevel.set_icon(iconPixbuf)

	#bring in widgets from glade file
	self.options_notebook = xml.get_widget("options_notebook")
	self.install_radiobutton = xml.get_widget("install_radiobutton")
	self.category_clist = xml.get_widget("category_clist")
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
	self.basic_class = basic.basic(xml, self.category_store,
				       self.category_view, self.options_notebook, self.kickstartData)
	#bring in bootloader functions
	self.bootloader_class = bootloader.bootloader(xml, self.kickstartData)
	#bring in install functions
	self.install_class = install.install(xml, self.category_store,
					     self.category_view, self.options_notebook,
					     self.bootloader_class, self.kickstartData)
	#bring in partitions functions
	self.partition_class = partition.partition(xml, self.kickstartData)
	#bring in network functions
	self.network_class = network.network(xml)
	#bring in auth functions
	self.auth_class = auth.auth(xml)
	#bring in firewall functions
	self.firewall_class = firewall.firewall(xml)
	#bring in X functions
	self.X_class = xconfig.xconfig(xml)
	#bring in package function
        #self.packages_class = packages.headerList(xml)
	#FIXME
	self.packages_class = packages.Packages(xml)	
	#bring in scripts function
	self.scripts_class = scripts.scripts(xml)	
	
	col = gtk.TreeViewColumn(_("Subsection"), gtk.CellRendererText(), text=0)
	col.set_sort_column_id(0)
	self.category_view.append_column(col)
	
	self.category_list = [ (_("Basic Configuration")), (_("Installation Method")),
			       (_("Boot Loader Options")), (_("Partition Information")),
			       (_("Network Configuration")), (_("Authentication")),
			       (_("Firewall Configuration")), (_("X Configuration")),
			       (_("Package Selection")), (_("Pre-Installation Script")),
			       (_("Post-Installation Script")) ]
		
	for item in self.category_list:
		iter = self.category_store.append()
		self.category_store.set_value(iter, 0, item)

	self.preview_menu.connect("activate", self.on_activate_preview_options)
	self.save_menu.connect("activate", self.on_activate_save_options)
	self.quit_menu.connect("activate", gtk.mainquit)
	self.help_menu.connect("activate", self.on_help_button_clicked)
	self.about_menu.connect("activate", self.on_about_activate)
	self.category_view.connect("cursor_changed", self.on_list_view_row_activated)

        if file:
            self.kickstartParser = kickstartParser.KickstartParser(self.kickstartData, file)
            self.fillData()
            


	#show gui
	self.toplevel.show_all()

	#		self.options_notebook.set_current_page(3)

	gtk.mainloop ()

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
	dlg.set_modal(gtk.TRUE)
	dlg.set_transient_for(self.toplevel)
	dlg.set_icon(iconPixbuf)
	rc = dlg.run()
	if rc == gtk.RESPONSE_OK:
	    dlg.hide()

    #display help manual
    def on_help_button_clicked (self, args):
        help_pages = ["file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-basic.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-bootloader.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-install.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-partitions.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-network.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-auth.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-firewall.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-xconfig.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-pkgs.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-prescript.html",
		      "file:///usr/share/doc/redhat-config-kickstart-" + "@VERSION@" + "/redhat-config-kickstart-postinstall.html",
		      ]
	page = (help_pages [self.options_notebook.get_current_page ()])
	path = helpBrowser.find_browser()

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

    #get all buffers to save to file
    def getAllData(self, *args):
        list = []

        if self.basic_class.getData() is None:
            return

        if self.install_class.getData() is None:
            return
        
	self.bootloader_class.getData()

	#only write partition info if performing an install
	if self.install_radiobutton.get_active():
		list = list + self.partition_class.getData()
	list = list + self.network_class.getData()
	list = list + self.auth_class.getData()
	list = list + self.firewall_class.getData()
	list = list + self.X_class.getData()

	if self.install_radiobutton.get_active():
		list = list + self.packages_class.getData()

	list = list + self.scripts_class.getData()

        self.kickstartData.getAll()

	return list

    #show chosen options for preview
    def on_activate_preview_options (self, *args):
        list = self.getAllData()
	if list:
	    #show preview dialog window
	    previewDialog = savefile.saveFile (list, self.xml)
	else:
	    return

    def on_activate_save_options (self, *args):
        list = self.getAllData()
	if list:
	    #show file selection dialog
	    fileDialog = savedialog.saveDialog(list, self.xml)
	else:
	    return		

    def fillData(self):
        self.basic_class.fillData()
        self.install_class.fillData()
        self.bootloader_class.fillData()
        self.partition_class.fillData()
