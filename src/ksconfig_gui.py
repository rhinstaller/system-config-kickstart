#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001 Red Hat, Inc.
## Copyright (C) 2000, 2001 Brent Fox <bfox@redhat.com>
##                          Tammy Fox <tfox@redhat.com>

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

import basic
import install
import partition
import network
import auth
import firewall
import savefile
import xconfig
import packages
import scripts

xml = libglade.GladeXML ("./ksconfig.glade", domain="ksconfig")

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
		#bring in basic functions
		self.basic_class = basic.basic(xml)
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
		self.packages_class = packages.headerList(xml)	
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
			  } )

		#populate category list
		self.category_clist = xml.get_widget("category_clist")
		self.category_clist.append(["Basic Configuration"])
		self.category_clist.append(["Installation Source"])
		self.category_clist.append(["Partition Information"])
		self.category_clist.append(["Networking Options"])
		self.category_clist.append(["Authentication"])
		self.category_clist.append(["Firewall Configuration"])
		self.category_clist.append(["X Configuration"])
		self.category_clist.append(["Package Selection"])
		self.category_clist.append(["Pre-Installation Script"])
		self.category_clist.append(["Post-Installation Script"])		
		
		gtk.mainloop ()

	def select_category(self, event, row, column, data):
		if self.category_clist.get_text(row,0)== "Basic Configuration":
			#change notebook tab
			self.options_notebook.set_page(0)
			return
		elif  self.category_clist.get_text(row,0)== "Installation Source":
			self.options_notebook.set_page(1)
			return
		elif  self.category_clist.get_text(row,0)== "Partition Information":
			self.options_notebook.set_page(2)
			return
		elif  self.category_clist.get_text(row,0)== "Networking Options":
			self.options_notebook.set_page(3)
			return
		elif  self.category_clist.get_text(row,0)== "Authentication":
			self.options_notebook.set_page(4)
			return
		elif  self.category_clist.get_text(row,0)== "Firewall Configuration":
			self.options_notebook.set_page(5)
			return
		elif  self.category_clist.get_text(row,0)== "X Configuration":
			self.options_notebook.set_page(6)
			return
		elif  self.category_clist.get_text(row,0)== "Package Selection":
			self.options_notebook.set_page(7)
			return
		elif  self.category_clist.get_text(row,0)== "Pre-Installation Script":
			self.options_notebook.set_page(8)
			return				
		elif  self.category_clist.get_text(row,0)== "Post-Installation Script":
			self.options_notebook.set_page(9)
			return				

	#about box
	def on_about_activate(self, args):
		aboutDialog = gnome.ui.GnomeAbout ("Kickstart Configurator", "1.9",
						   "Copyright (c) 2000, 2001 Red Hat, Inc.",
						   ["Brent Fox <bfox@redhat.com>",
						    "Tammy Fox <tfox@redhat.com>"],
						   "A graphical interface for creating a basic kickstart file.")
		aboutDialog.run_and_close()

	#show choosen options for confirmation
	def on_activate_confirm_options (self, *args):
		buf = "#Generated by Kickstart Configurator"
		buf = buf + self.basic_class.getData()
		buf = buf + self.install_class.getData()
		buf = buf + self.partition_class.getData()
		buf = buf + self.network_class.getData()
		buf = buf + self.auth_class.getData()
		buf = buf + self.firewall_class.getData()
		buf = buf + self.X_class.getData()
##	        buf = buf + self.packages_class.getData()
		buf = buf + self.scripts_class.getData()
		
	        #show confirm dialog window
		confirmDialog = savefile.saveFile (buf)
