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

import gtk
import gtk.glade
import string
import savedialog
import signal

class saveFile:
	
	def destroy(self, args):
		self.dialog.destroy()

        def __init__ (self, buf, xml):
		self.xml = xml
		self.buf = buf

		self.dialog = self.xml.get_widget("preview_options_dialog")
		self.textview = self.xml.get_widget("confirm_options_textview")
		self.confirm_options_ok_button = xml.get_widget("confirm_options_ok_button")
		self.confirm_options_cancel_button = xml.get_widget("confirm_options_cancel_button")

		self.dialog.connect ("destroy", self.destroy)
		self.confirm_options_ok_button.connect("clicked", self.saveFile_cb)
		self.confirm_options_cancel_button.connect("clicked", self.on_confirm_options_cancel_button)
		
		#display choosen options in textview
		self.confirm_buffer = gtk.TextBuffer(None)
		iter = self.confirm_buffer.get_iter_at_offset (0)
		for line in self.buf:
			self.confirm_buffer.insert(iter,line + "\n",-1)

## 		baseSize = 10
## 		baseFont = 'sans'
## 		self.textTag = self.confirm_buffer.create_tag('text')
## 		self.textTag.set_property('font', '%s %d' % (baseFont, baseSize))
## 		self.textTag.set_property('pixels-above-lines', 1)
## 		self.textTag.set_property('pixels-below-lines', 1)

## 		self.confirm_buffer.apply_tag(self.textTag, self.confirm_buffer.get_start_iter(), self.confirm_buffer.get_end_iter())
		self.textview.set_buffer(self.confirm_buffer)
				
		self.dialog.show_all()

        def on_confirm_options_cancel_button(self, *args):
		#using hide because destroy crashes application after second instance
		self.dialog.hide()

	def saveFile_cb(self, *args):
		self.dialog.hide()
 		fileDialog = savedialog.saveDialog(self.buf, self.xml)
