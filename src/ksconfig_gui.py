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
import string

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

xml = libglade.GladeXML ("./ksconfig.glade", domain="ksconfig")

class ksconfig_gui:
	
	def destroy(self, args):
		gtk.mainquit()

	def __init__ (self):
		self.toplevel = xml.get_widget("main_window")
		self.toplevel.connect ("destroy", self.destroy)

		#bring in widgets from glade file
		self.partClist = xml.get_widget("partClist")
		self.ksconfig_about = xml.get_widget("ksconfig_about")
		self.confirm_options_dialog = xml.get_widget("confirm_option_dialog")
		self.options_notebook = xml.get_widget("options_notebook")
		lang_combo = xml.get_widget("lang_combo")
		lang_support_combo = xml.get_widget("lang_support_combo")
		mouse_combo = xml.get_widget("mouse_combo")
		keyboard_combo = xml.get_widget("keyboard_combo")		
		timezone_combo = xml.get_widget("timezone_combo")
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
		self.category_clist.append(["Package Selection"])

		#populate partitions table with default values
		bootPartition = ["/boot", "ext2", "35", "No"]
		self.partClist.append(bootPartition)
		swapPartition = ["", "Linux Swap", "128", "No"]
		self.partClist.append(swapPartition)
		rootPartition = ["/", "ext2", "1000", "Yes"]
		self.partClist.append(rootPartition)

		#populate language combo
		list_items = [ "Czech", "English", "French", "German", "Hungarian",
			       "Icelandic", "Italian","Japanese", "Norwegian", "Romanian",
			       "Russian", "Serbian", "Slovak", "Slovenian", "Spanish",
			       "Swedish", "Turkish", "Ukrainian" ]
		lang_combo.set_popdown_strings(list_items)
		lang_combo.list.select_item(1)
		lang_combo.entry.set_editable(FALSE)

		#populate language support combo
		list_items = [ "Czech", "English", "French", "German", "Hungarian",
			       "Icelandic", "Italian","Japanese", "Norwegian", "Romanian",
			       "Russian", "Serbian", "Slovak", "Slovenian", "Spanish",
			       "Swedish", "Turkish", "Ukrainian" ]
		lang_support_combo.set_popdown_strings(list_items)
		lang_support_combo.list.select_item(1)
		lang_support_combo.entry.set_editable(FALSE)				

		#populate keyboard combo
		list_items = [ "azerty", "be-latin1", "be2-latin1",
		"fr-latin0", "fr-pc", "fr", "wangbe", "ANSI-dvorak",
		"dvorak-1", "dvorak-r", "dvorak", "pc-dvorak-latin1",
		"tr_f-latin5", "trf", "bg", "cf", "cz-lat2-prog",
		"cz-lat2", "defkeymap", "defkeymap_V1.0", "dk-latin1",
		"dk.emacs", "emacs2", "es", "fi-latin1", "fi",
		"gr-pc", "gr", "hebrew", "hu101", "is-latin",
		"it-ibm", "it", "it2", "jp106", "la-latin1", "lt",
		"lt.l4", "nl", "no-latin1", "no", "pc110", "pl",
		"pt-latin1", "pt-old", "ro", "ru-cp1251", "ru-ms",
		"ru-yawerty", "ru", "ru1", "ru2", "ru_win",
		"se-latin1", "sk-prog-qwerty", "sk-prog", "sk-qwerty",
		"tr_q-latin5", "tralt", "trf", "trq", "ua", "uk",
		"us", "croat", "cz-us-qwerty", "de-latin1-nodeadkeys",
		"de-latin1", "de", "fr_CH-latin1", "fr_CH", "hu",
		"sg-latin1-lk450", "sg-latin1", "sg",
		"sk-prog-qwertz", "sk-qwertz", "slovene" ]
		keyboard_combo.set_popdown_strings(list_items)
		keyboard_combo.list.select_item(63)
		keyboard_combo.entry.set_editable(FALSE)		

		#populate mouse combo
		list_items = [ "Generic - 2 Button Mouse (serial)",
 				"Generic - 2 Button Mouse (PS/2)",
 				"Logitech - MouseMan/FirstMouse (serial)",
			        "Logitech - MouseMan/FirstMouse (PS/2)" ]

		mouse_combo.set_popdown_strings(list_items)
		mouse_combo.list.select_item(1)
		mouse_combo.entry.set_editable(FALSE)		

		#populate time zone combo
		tz = open ("/usr/share/zoneinfo/zone.tab", "r")
		lines = tz.readlines()
		tz.close()
		list_items = []
		
		clockfile = open ("/etc/sysconfig/clock", "r")
		clocklines = clockfile.readlines()
		clockfile.close()
		for line in clocklines:
			if line[:4] == "ZONE":
				tmp = string.split(line, "=")
				zone = tmp[1]
				zone = zone[1:-2]

		for line in lines:
			if line[:1] == "#":
				pass
			else:
				tokens = string.split(line)
				list_items.append(tokens[2])

		list_items.sort()

 	        #--Search timezone list for default
		if zone in list_items:
			select = list_items.index(zone)

		timezone_combo.set_popdown_strings(list_items)
		timezone_combo.list.select_item(select)
		timezone_combo.entry.set_editable(FALSE)		

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
		elif  self.category_clist.get_text(row,0)== "Package Selection":
			self.options_notebook.set_page(6)
			return		

	#about box
	def on_about_activate(self, args):
		aboutDialog = gnome.ui.GnomeAbout ("Kickstart Configurator", "2.0",
						   "Copyright (c) 2000, 2001 Red Hat, Inc.",
						   ["Brent Fox <bfox@redhat.com>",
						    "Tammy Fox <tfox@redhat.com>"],
						   "A graphical interface for creating a basic kickstart file.")
		aboutDialog.run_and_close()

	#show choosen options for confirmation
	def on_activate_confirm_options (self, *args):
	    buf = "#Generated by Kickstart Configurator"
#	    buf = buf + self.basic_class.getData()
#	    print buf
#	    buf = buf + self.install_class.getData()
#	    print buf
#            buf = buf + self.partition_class.getData()
#           print buf
#	    buf = buf + self.network_class.getData()
#	    print buf
	    buf = buf + self.auth_class.getData()
	    print buf
	    
#	    confirmDialog = savefile.saveFile ()
