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
import string
import savedialog

import gtk
import signal
import libglade
import gnome.ui

xml = libglade.GladeXML ("./ksconfig.glade", "confirm_options_dialog", domain="ksconfig")

class saveFile:
	
	def destroy(self, args):
            self.dialog.destroy()

        def __init__ (self):
            self.dialog = xml.get_widget("confirm_options_dialog")
            self.dialog.connect ("destroy", self.destroy)

	    self.confirm_options_textbox = xml.get_widget("confirm_options_textbox")
	    
            #extract widgets, autoconnects
            xml.signal_autoconnect (
                { "on_confirm_options_cancel_button" : self.on_confirm_options_cancel_button,
                  "saveFile_cb" : self.saveFile_cb,
                  } )

	    #display choosen options in text box
#	    self.confirm_options_textbox.gtk_text_insert("buf")
            
            
            self.dialog.show_all()

        def on_confirm_options_cancel_button(self, *args):
            #using hide because destroy crashes application after second instance
            self.dialog.hide()

	def saveFile_cb(self, *args):

		buf = ""

## 		try:
## 			buf = buf + networkWin.getData()
## 		except:
## 			pass

## 		buf = buf + "\n" + "install"

## 		buf = buf + "\n" + "auth"


## 		try:
## 			buf = buf + authWin.getData() + "\n"
## 			print buf
## 		except:
## 			pass

## 		try:
## 			buf = buf + "\n" + firewallWin.getData()
## 		except:
## 			pass

## 		try:
## 			buf = buf + "\n" + packageWin.getData()
## 		except:
## 			pass

		self.dialog.hide()
 		fileDialog = savedialog.saveDialog(buf)		


