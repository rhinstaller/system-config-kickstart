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
#import ksconfig
import basic
import bootloader
import install
import partition
import network
import auth
import firewall
import savefile
import xconfig
import packages
import scripts


##
## I18N
##
import gettext
gettext.bindtextdomain ("ksconfig", "/usr/share/locale")
gettext.textdomain ("ksconfig")
_=gettext.gettext

#gtk.glade.bindtextdomain(domain)
#xml = gtk.glade.XML ("/usr/share/ksconfig/ksconfig-gtk2.glade", domain="ksconfig")
#xml = gtk.glade.XML ("./ksconfig-gtk2.glade", domain="ksconfig")
#xml = libglade.GladeXML ("/usr/share/ksconfig/ksconfig.glade", domain="ksconfig")
#xml = libglade.GladeXML ("./ksconfig.glade", domain="ksconfig")

class ksconfig_gui:
	
	def destroy(self, args):
		gtk.mainquit()

	def __init__ (self, xml):
		self.xml = xml
		self.toplevel = xml.get_widget("main_window")
		self.toplevel.connect ("destroy", self.destroy)

		#bring in widgets from glade file
		self.ksconfig_about = xml.get_widget("ksconfig_about")
		self.confirm_options_dialog = xml.get_widget("confirm_option_dialog")
		self.confirm_options_button = xml.get_widget("confirm_options_button")
		self.options_notebook = xml.get_widget("options_notebook")
		self.install_radiobutton = xml.get_widget("install_radiobutton")
		self.category_clist = xml.get_widget("category_clist")
		self.save_menu = xml.get_widget("save_menu")
		self.quit_menu = xml.get_widget("quit_menu")
		self.help_menu = xml.get_widget("help_menu")
		self.about_menu = xml.get_widget("about_menu")
		self.cancel_button = xml.get_widget("cancel_button")

		#bring in basic functions
		self.basic_class = basic.basic(xml)
		#bring in bootloader functions
		self.bootloader_class = bootloader.bootloader(xml)		
		#bring in install functions
		self.install_class = install.install(xml)
		#bring in partitions functions
		self.partition_class = partition.partition(xml)
		#bring in network functions
		self.network_class = network.network(xml)
		#bring in auth functions
		self.auth_class = auth.auth(xml)
		#bring in firewall functions
		self.firewall_class = firewall.firewall(xml)
		#bring in X functions
		self.X_class = xconfig.xconfig(xml)
		#bring in package function
#		self.packages_class = packages.headerList(xml)
                #FIXME
#		self.packages_class = packages.Packages(xml)	
		#bring in scripts function
		self.scripts_class = scripts.scripts(xml)	

		#show gui
		self.toplevel.show_all()

		#populate category list
		self.category_view = xml.get_widget("list_view")
		self.category_store = gtk.ListStore(gobject.TYPE_STRING)
		self.category_view.set_model(self.category_store)

		col = gtk.TreeViewColumn(_("Subsection"), gtk.CellRendererText(), text=0)
		col.set_sort_column_id(0)
		self.category_view.append_column(col)

		self.category_list = [ (_("Basic Configuration")), (_("Boot Loader Options")),
				   (_("Installation Method")), (_("Partition Information")),
				   (_("Network Configuration")), (_("Authentication")),
				   (_("Firewall Configuration")), (_("X Configuration")),
				   (_("Package Selection")), (_("Pre-Installation Script")),
				   (_("Post-Installation Script")) ]

		for item in self.category_list:
			iter = self.category_store.append()
			self.category_store.set_value(iter, 0, item)

		self.save_menu.connect("activate", self.on_activate_confirm_options)
		self.quit_menu.connect("activate", gtk.mainquit)
		self.help_menu.connect("activate", self.on_help_button_clicked)
		self.about_menu.connect("activate", self.on_about_activate)

		self.confirm_options_button.connect("clicked", self.on_activate_confirm_options)
		self.cancel_button.connect("clicked", gtk.mainquit)
		self.category_view.connect("cursor_changed", self.on_list_view_row_activated)

		#bring in signals from glade file
#		xml.signal_connect("on_cancel_button_clicked", gtk.mainquit)
#		xml.signal_connect("on_exit_activate", gtk.mainquit)
##		xml.signal_connect("on_list_view_row_activated", self.on_list_view_row_activated)
#		xml.signal_connect("on_about_activate", self.on_about_activate)
#		xml.signal_connect("on_activate_confirm_options", self.on_activate_confirm_options)
#		xml.signal_connect("on_help_button_clicked", self.on_help_button_clicked)


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
		rc = dlg.run()
		if rc == gtk.RESPONSE_OK:
			dlg.hide()

	#display help manual
	def on_help_button_clicked (self, args):
		print "you clicked help"
## 		help_pages = ["file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-basic.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-bootloader.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-install.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-partitions.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-network.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-auth.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-firewall.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-xconfig.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-pkgs.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-prescript.html",
## 			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-postinstall.html",
## 			      ]
## 		gnome.help.goto (help_pages [self.options_notebook.get_current_page ()])

	#show choosen options for confirmation
	def on_activate_confirm_options (self, *args):
		list = []

		list.append("#Generated by Kickstart Configurator")
		data = self.basic_class.getData()
		if data:
			list = list + data
		else:
			return
		list = list + self.bootloader_class.getData()
		list = list + self.install_class.getData()

 		#only write partition info if performing an install
 		if self.install_radiobutton.get_active():
 			list = list + self.partition_class.getData()
 		list = list + self.network_class.getData()
 		list = list + self.auth_class.getData()
 		list = list + self.firewall_class.getData()
		list = list + self.X_class.getData()

#		if self.install_radiobutton.get_active():
#			list = list + self.packages_class.getData()

		list = list + self.scripts_class.getData()

 	        #show confirm dialog window
		confirmDialog = savefile.saveFile (list, self.xml)
