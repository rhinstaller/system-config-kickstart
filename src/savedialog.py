#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2 or, at your option, any later version.  This
# program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 

import gtk
import gtk.glade
import savefile
import signal
import kickstartGui

class saveDialog:
	
	def destroy(self, args):
		self.dialog.destroy()

        def __init__ (self, buf, xml):
		self.xml = xml
		self.buf = buf
		self.dialog = self.xml.get_widget("save_dialog")
		self.dialog.connect("delete-event", self.hide)
		self.dialog.set_modal(True)
		toplevel = self.xml.get_widget("main_window")
		self.dialog.set_transient_for(toplevel)
		self.save_ok_button = self.xml.get_widget("save_ok_button")
		self.save_cancel_button = self.xml.get_widget("save_cancel_button")

		self.dialog.set_current_name("ks.cfg")

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
                ksFile.write(self.buf)
		ksFile.close()
		self.dialog.hide()

	def hide(self, *args):
		self.dialog.hide()
		return True
