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

import gtk
import gtk.glade
import savefile
import signal
import kickstartGui

class saveDialog:
	
	def destroy(self, args):
		self.dialog.destroy()

        def __init__ (self, dataList, xml):
		self.xml = xml
		self.dataList = dataList
		self.dialog = self.xml.get_widget("save_dialog")
		self.dialog.connect("delete-event", self.hide)
		self.dialog.set_modal(gtk.TRUE)
		toplevel = self.xml.get_widget("main_window")
		self.dialog.set_transient_for(toplevel)
		self.save_ok_button = self.xml.get_widget("save_ok_button")
		self.save_cancel_button = self.xml.get_widget("save_cancel_button")

		self.dialog.set_filename("ks.cfg")

		self.dialog.filePath= ""
		self.dialog.connect ("destroy", self.destroy)
		
		self.save_ok_button.connect("clicked", self.saveFile)
		self.save_cancel_button.connect("clicked", self.hide)

		self.dialog.set_icon(kickstartGui.iconPixbuf)

		self.dialog.show_all()

	#save file
        def saveFile(self, *args):		
		self.dialog.filePath = self.dialog.get_filename()
		ksFile = open(self.dialog.filePath, "w")
		for line in self.dataList:
			ksFile.write(line + "\n")
 
		ksFile.close()
		self.dialog.hide()

	def hide(self, *args):
		self.dialog.hide()
		return gtk.TRUE
