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

#Kickstart Configurator Scripts

import gtk
import gtk.glade

class scripts:

    def __init__(self, xml):
        self.chroot_checkbutton = xml.get_widget("chroot_checkbutton")
        self.interpreter_checkbutton = xml.get_widget("interpreter_checkbutton")
        self.interpreter_entry = xml.get_widget("interpreter_entry")
        self.pre_textview = xml.get_widget("pre_textview")
        self.post_textview = xml.get_widget("post_textview")

        self.interpreter_checkbutton.connect("toggled", self.interpreter_cb)

    def interpreter_cb(self, args):
        self.interpreter_entry.set_sensitive(self.interpreter_checkbutton.get_active())

    def getData(self):
        data = []
        data.append("")
        data.append(self.preData())
        data.append(self.postData())
        return data
    
    def preData(self):
        pre_buffer = self.pre_textview.get_buffer()
        data = pre_buffer.get_text(pre_buffer.get_start_iter(),pre_buffer.get_end_iter(),gtk.FALSE)
        if data != "":
            buf = "%pre" + "\n" + data
        else:
            buf = ""
        return buf

    def postData(self):
        post_command = "%post "
        if self.chroot_checkbutton.get_active():
            post_command = post_command + "--nochroot  "
        if self.interpreter_checkbutton.get_active():
            post_command = post_command + "--interpreter " + self.interpreter_entry.get_text()
        post_buffer = self.post_textview.get_buffer()
        data = post_buffer.get_text(post_buffer.get_start_iter(),post_buffer.get_end_iter(),gtk.FALSE)
        if data != "":
            buf = "\n" + post_command + "\n" + data
        else:
            buf = ""
        return buf
