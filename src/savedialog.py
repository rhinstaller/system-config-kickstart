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

from gtk import *
from gnome.ui import *
import GtkExtra
import savefile

import gtk
import signal
import libglade
import gnome.ui

xml = libglade.GladeXML ("./ksconfig.glade", "save_dialog", domain="ksconfig")

class saveDialog:
	
	def destroy(self, args):
		self.dialog.destroy()

        def __init__ (self, buf):
		self.buf = buf
		self.dialog = xml.get_widget("save_dialog")
		self.dialog.set_filename("ks.cfg")
		self.dialog.cancel_button.connect("clicked",self.dialog.hide)
		self.dialog.filePath= ""
		self.dialog.connect ("destroy", self.destroy)
		
                #extract widgets, autoconnects
		xml.signal_autoconnect (
			{ "saveFile" : self.saveFile,
			  } )

		self.dialog.show_all()


	#save file
        def saveFile(self, *args):
		self.dialog.filePath = self.dialog.get_filename()
		ksFile = open(self.dialog.filePath, "w")
		ksFile.write(self.buf)
		ksFile.close()
		self.dialog.hide()
