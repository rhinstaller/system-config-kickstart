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
import string
import savedialog
import signal
import kickstartGui

class saveFile:
	
	def destroy(self, args):
		self.dialog.destroy()

        def __init__ (self, buf, xml):
		self.xml = xml
		self.buf = buf

		self.dialog = self.xml.get_widget("preview_options_dialog")
		self.dialog.connect("delete-event", self.on_confirm_options_cancel_button)
		toplevel = self.xml.get_widget("main_window")
		self.dialog.set_transient_for(toplevel)
		self.textview = self.xml.get_widget("confirm_options_textview")
		self.confirm_options_ok_button = xml.get_widget("confirm_options_ok_button")
		self.confirm_options_cancel_button = xml.get_widget("confirm_options_cancel_button")

		self.dialog.connect ("destroy", self.destroy)
		self.confirm_options_ok_button.connect("clicked", self.saveFile_cb)
		self.confirm_options_cancel_button.connect("clicked", self.on_confirm_options_cancel_button)
		
		#display choosen options in textview
		self.confirm_buffer = gtk.TextBuffer(None)
		self.confirm_buffer.set_text(self.buf)
		self.textview.set_buffer(self.confirm_buffer)
				
		self.dialog.show_all()

        def on_confirm_options_cancel_button(self, *args):
		#using hide because destroy crashes application after second instance
		self.dialog.hide()
		return True

	def saveFile_cb(self, *args):
		self.dialog.hide()
 		fileDialog = savedialog.saveDialog(self.buf, self.xml)
