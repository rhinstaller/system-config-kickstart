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

class scripts:

    def __init__(self, xml, kickstartData):
        self.kickstartData = kickstartData
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
        if self.pre_interpreter_checkbutton.get_active():
            pre_command = "--interpreter=" + self.pre_interpreter_entry.get_text()
            self.kickstartData.setPreLine(pre_command)
        else:
            self.kickstartData.setPreLine(None)

        pre_buffer = self.pre_textview.get_buffer()
        data = pre_buffer.get_text(pre_buffer.get_start_iter(),pre_buffer.get_end_iter(),gtk.TRUE)
        data = string.strip(data)

        if data != "":
            self.kickstartData.setPreList([data])


    def postData(self):
        post_command = ""
        if self.chroot_checkbutton.get_active():
            post_command = "--nochroot "

        if self.interpreter_checkbutton.get_active():
            post_command = post_command + "--interpreter=" + self.interpreter_entry.get_text()

        if post_command == "":
            self.kickstartData.setPostLine(None)
        else:
            self.kickstartData.setPostLine(post_command)

        post_buffer = self.post_textview.get_buffer()
        data = post_buffer.get_text(post_buffer.get_start_iter(),post_buffer.get_end_iter(),gtk.TRUE)

        data = string.strip(data)

        if data == "":
            self.kickstartData.setPostList([])
        else:
            self.kickstartData.setPostList([data])

    def fillData(self):
        if self.kickstartData.getPreLine():
            line = self.kickstartData.getPreLine()

            opts, args = getopt.getopt(line, "i:", ["interpreter="])

            for opt, value in opts:
                if opt == "--interpreter":
                    self.pre_interpreter_checkbutton.set_active(gtk.TRUE)
                    self.pre_interpreter_entry.set_text(value)
            
            if self.kickstartData.getPreList():
                list = self.kickstartData.getPreList()
                iter = self.pre_textview.get_buffer().get_iter_at_offset(0)

                for line in list:
                    self.pre_textview.get_buffer().insert(iter, (line + "\n"))

        if self.kickstartData.getPostLine():
            line = self.kickstartData.getPostLine()

            opts, args = getopt.getopt(line, "i:", ["interpreter=", "nochroot"])

            for opt, value in opts:
                if opt == "--interpreter":
                    self.interpreter_checkbutton.set_active(gtk.TRUE)
                    self.interpreter_entry.set_text(value)

                if opt == "--nochroot":
                    self.chroot_checkbutton.set_active(gtk.TRUE)
            
            if self.kickstartData.getPostList():
                list = self.kickstartData.getPostList()
                iter = self.post_textview.get_buffer().get_iter_at_offset(0)

                for line in list:
                    self.post_textview.get_buffer().insert(iter, (line + "\n"))



