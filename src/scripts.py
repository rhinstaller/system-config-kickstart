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

#Kickstart Configurator Scripts

from gtk import *
import GtkExtra
import libglade

class scripts:

    def __init__(self, xml):
        self.chroot_checkbutton = xml.get_widget("chroot_checkbutton")
        self.interpreter_checkbutton = xml.get_widget("interpreter_checkbutton")
        self.interpreter_entry = xml.get_widget("interpreter_entry")
        self.pre_text = xml.get_widget("pre_text")
        self.post_text = xml.get_widget("post_text")
        #bring in signals from glade file
        xml.signal_autoconnect (
            { "interpreter_cb" : self.interpreter_cb,
              } )

    def interpreter_cb(self, args):
        self.interpreter_entry.set_sensitive(self.interpreter_checkbutton.get_active())

    def getData(self):
        data = []
        data.append("")
        data.append(self.preData())
        data.append(self.postData())
        return data
    
    def preData(self):
        length = self.pre_text.get_length()
        if length > 0:
            data = self.pre_text.get_chars(0,length)
            buf = "%pre" + "\n" + data
        else:
            buf = ""
        return buf

    def postData(self):
        post_command = "%post"
        if self.chroot_checkbutton.get_active():
            post_command = post_command + " --nochroot  "
        if self.interpreter_checkbutton.get_active():
            post_command = post_command + "--interpreter " + self.interpreter_entry.get_text()
        length = self.post_text.get_length()
        if length > 0:
            data = self.post_text.get_chars(0,length)
            buf = "\n" + post_command + "\n" + data
        else:
            buf = ""
        return buf
