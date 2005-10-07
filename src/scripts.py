## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
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

#Kickstart Configurator Scripts

import gtk
import gtk.glade
import getopt
import string
from pykickstart.parser import Script

class scripts:
    def __init__(self, xml, ksdata):
        self.ksdata = ksdata
        self.chroot_checkbutton = xml.get_widget("chroot_checkbutton")
        self.interpreter_checkbutton = xml.get_widget("interpreter_checkbutton")
        self.interpreter_entry = xml.get_widget("interpreter_entry")
        self.pre_interpreter_checkbutton = xml.get_widget("pre_interpreter_checkbutton")
        self.pre_interpreter_entry = xml.get_widget("pre_interpreter_entry")
        self.pre_textview = xml.get_widget("pre_textview")
        self.post_textview = xml.get_widget("post_textview")

        self.interpreter_checkbutton.connect("toggled", self.interpreter_cb)
        self.pre_interpreter_checkbutton.connect("toggled", self.pre_interpreter_cb)        

    def interpreter_cb(self, args):
        self.interpreter_entry.set_sensitive(self.interpreter_checkbutton.get_active())

    def pre_interpreter_cb(self, args):
        self.pre_interpreter_entry.set_sensitive(self.pre_interpreter_checkbutton.get_active())        

    def getData(self):
        self.preData()
        self.postData()
    
    def preData(self):
        pre_buffer = self.pre_textview.get_buffer()
        data = pre_buffer.get_text(pre_buffer.get_start_iter(),pre_buffer.get_end_iter(),True)
        data = string.strip(data)

        if data == "":
            return
        
        if len(self.ksdata.preScripts) == 0:
            script = Script("")
        else:
            script = self.ksdata.preScripts[0]

        if self.pre_interpreter_checkbutton.get_active():
            script.interp = self.pre_interpreter_entry.get_text()

        script.script = data

        if len(self.ksdata.preScripts) == 0:
            self.ksdata.preScripts.append(script)

    def postData(self):
        post_buffer = self.post_textview.get_buffer()
        data = post_buffer.get_text(post_buffer.get_start_iter(),post_buffer.get_end_iter(),True)
        data = string.strip(data)

        if data == "":
            return

        if len(self.ksdata.postScripts) == 0:
            script = Script("")
        else:
            script = self.ksdata.postScripts[0]

        if self.chroot_checkbutton.get_active():
            script.inChroot = False
        else:
            script.inChroot = True

        if self.interpreter_checkbutton.get_active():
            script.interp = self.interpreter_entry.get_text()

        script.script = data

        if len(self.ksdata.postScripts) == 0:
            self.ksdata.postScripts.append(script)

    def fillData(self):
        # We're kind of a crappy UI and assume they only have one script.
        if len(self.ksdata.preScripts) > 0:
            script = self.ksdata.preScripts[0]

            if script.interp != "":
                self.pre_interpreter_checkbutton.set_active(True)
                self.pre_interpreter_entry.set_text(script.interp)

            self.pre_textview.get_buffer().set_text(script.script)

        if len(self.ksdata.postScripts) > 0:
            script = self.ksdata.postScripts[0]

            if script.interp != "":
                self.interpreter_checkbutton.set_active(True)
                self.interpreter_entry.set_text(script.interp)

            if script.inChroot == False:
                self.chroot_checkbutton.set_active(True)

            self.post_textview.get_buffer().set_text(script.script)
