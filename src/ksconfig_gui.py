#!/usr/bin/env python

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

from gtk import *
from gnome.ui import *
import GtkExtra

import gtk
import signal
import libglade
import gnome.ui
import gnome.help

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

xml = libglade.GladeXML ("/usr/share/ksconfig/ksconfig.glade", domain="ksconfig")
#xml = libglade.GladeXML ("./ksconfig.glade", domain="ksconfig")

class ksconfig_gui:
	
	def destroy(self, args):
		gtk.mainquit()

	def __init__ (self):
		self.toplevel = xml.get_widget("main_window")
		self.toplevel.connect ("destroy", self.destroy)

		#bring in widgets from glade file
		self.ksconfig_about = xml.get_widget("ksconfig_about")
		self.confirm_options_dialog = xml.get_widget("confirm_option_dialog")
		self.options_notebook = xml.get_widget("options_notebook")
		self.install_radiobutton = xml.get_widget("install_radiobutton")
		self.category_clist = xml.get_widget("category_clist")
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
		self.packages_class = packages.Packages(xml)	
		#bring in scripts function
		self.scripts_class = scripts.scripts(xml)	

		#show gui
		self.toplevel.show_all()

		#bring in signals from glade file
 		xml.signal_autoconnect (
			{ "on_cancel_button_clicked" : gtk.mainquit,
			  "on_exit_activate" : gtk.mainquit,
 			  "select_category" : self.select_category,
			  "on_about_activate" : self.on_about_activate,
			  "on_activate_confirm_options" : self.on_activate_confirm_options,
			  "on_help_button_clicked" : self.on_help_button_clicked,
			  } )

		#populate category list
		self.category_clist = xml.get_widget("category_clist")
		self.category_clist.append([_("Basic Configuration")])
		self.category_clist.append([_("Boot Loader Options")])		
		self.category_clist.append([_("Installation Method")])
		self.category_clist.append([_("Partition Information")])
		self.category_clist.append([_("Network Configuration")])
		self.category_clist.append([_("Authentication")])
		self.category_clist.append([_("Firewall Configuration")])
		self.category_clist.append([_("X Configuration")])
		self.category_clist.append([_("Package Selection")])
		self.category_clist.append([_("Pre-Installation Script")])
		self.category_clist.append([_("Post-Installation Script")])		
		gtk.mainloop ()

	def select_category(self, event, row, column, data):
		self.options_notebook.set_page(row)
		return

	#about box
	def on_about_activate(self, args):
		aboutDialog = gnome.ui.GnomeAbout (_("Kickstart Configurator"), "@VERSION@",
						   "Copyright (c) 2000, 2001 Red Hat, Inc.",
						   ["Brent Fox <bfox@redhat.com>",
						    "Tammy Fox <tfox@redhat.com>"],
						   _("A graphical interface for creating a kickstart file."))
		aboutDialog.run_and_close()

	#display help manual
	def on_help_button_clicked (self, args):
	
		help_pages = ["file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-basic.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-bootloader.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-install.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-partitions.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-network.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-auth.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-firewall.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-xconfig.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-pkgs.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-prescript.html",
			      "file:///usr/share/doc/ksconfig-" + "@VERSION@" + "/ksconfig-postinstall.html",
			      ]
		gnome.help.goto (help_pages [self.options_notebook.get_current_page ()])

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

		if self.install_radiobutton.get_active():
			list = list + self.packages_class.getData()

		list = list + self.scripts_class.getData()

 	        #show confirm dialog window
		confirmDialog = savefile.saveFile (list, xml)
