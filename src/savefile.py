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
import string
import savedialog
import signal
import kickstartGui

##
## I18N
##
import gettext
gtk.glade.bindtextdomain("system-config-kickstart")
_ = lambda x: gettext.ldgettext("system-config-kickstart", x)

class PreviewDialog:
    def __init__(self, buf):
        self.buf = buf
        self.rc = 0

        self.dialog = gtk.Dialog(_("Preview Options"),
                                 flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                 buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                          gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
        self.dialog.set_size_request(400, 550)
        self.dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.dialog.vbox.set_spacing(6)

        label = gtk.Label(_("You have choosen the following configuration. Click Save File to save the kickstart file."))
        label.set_line_wrap(True)

        self.dialog.vbox.pack_start(label, expand=False, fill=False)

        view = gtk.TextView(gtk.TextBuffer())
        view.get_buffer().set_text(unicode(self.buf))
        view.set_editable(False)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add_with_viewport(view)

        self.dialog.vbox.pack_start(scroll, expand=True, fill=True)
        self.dialog.show_all()

    def getrc(self):
        return self.rc

    def run(self):
        self.rc = self.dialog.run()
        self.dialog.hide()

class saveFile:
    def __init__(self, buf, xml):
        self.buf = buf
        self.dialog = PreviewDialog(buf)
        self.xml = xml

    def run(self):
        self.dialog.run()
        rc = self.dialog.getrc()

        if rc == gtk.RESPONSE_REJECT:
            del self.dialog
            return
        elif rc == gtk.RESPONSE_ACCEPT:
            del self.dialog
            fileDialog = savedialog.saveDialog(self.buf, self.xml)
