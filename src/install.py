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

#Kickstart Configurator Installation Methods

from gtk import *
import GtkExtra
import libglade

class install:

    def __init__(self, xml):
        self.cdrom_radiobutton = xml.get_widget("cdrom_radiobutton")
        self.nfs_radiobutton = xml.get_widget("nfs_radiobutton")
        self.ftp_radiobutton = xml.get_widget("ftp_radiobutton")
        self.hd_radiobutton = xml.get_widget("hd_radiobutton")		
        self.http_radiobutton = xml.get_widget("http_radiobutton")

        self.nfsdir_label = xml.get_widget("nfsdir_label")
        self.nfsserver_label = xml.get_widget("nfsserver_label")
        self.ftpdir_label = xml.get_widget("ftpdir_label")
        self.ftpserver_label = xml.get_widget("ftpserver_label")
        self.hdpart_label = xml.get_widget("hdpart_label")
        self.hddir_label = xml.get_widget("hddir_label")
        self.httpserver_label = xml.get_widget("httpserver_label")
        self.httpdir_label = xml.get_widget("httpdir_label")

        self.nfsdir_entry = xml.get_widget("nfsdir_entry")
        self.nfsserver_entry = xml.get_widget("nfsserver_entry")
        self.ftpdir_entry = xml.get_widget("ftpdir_entry")
        self.ftpserver_entry = xml.get_widget("ftpserver_entry")
        self.hdpart_entry = xml.get_widget("hdpart_entry")
        self.hddir_entry = xml.get_widget("hddir_entry")
        self.httpserver_entry = xml.get_widget("httpserver_entry")
        self.httpdir_entry = xml.get_widget("httpdir_entry")

        xml.signal_autoconnect (
            { "setState" : self.setState,
              } )

    def setState (self, args):
        self.nfsserver_label.set_sensitive(self.nfs_radiobutton.get_active())
        self.nfsdir_label.set_sensitive(self.nfs_radiobutton.get_active())
        self.ftpserver_label.set_sensitive(self.ftp_radiobutton.get_active())
        self.ftpdir_label.set_sensitive(self.ftp_radiobutton.get_active())
        self.hdpart_label.set_sensitive(self.hd_radiobutton.get_active())
        self.hddir_label.set_sensitive(self.hd_radiobutton.get_active())
        self.httpserver_label.set_sensitive(self.http_radiobutton.get_active())
        self.httpdir_label.set_sensitive(self.http_radiobutton.get_active())

        self.nfsserver_entry.set_sensitive(self.nfs_radiobutton.get_active())
        self.nfsdir_entry.set_sensitive(self.nfs_radiobutton.get_active())
        self.ftpserver_entry.set_sensitive(self.ftp_radiobutton.get_active())
        self.ftpdir_entry.set_sensitive(self.ftp_radiobutton.get_active())
        self.hdpart_entry.set_sensitive(self.hd_radiobutton.get_active())
        self.hddir_entry.set_sensitive(self.hd_radiobutton.get_active())
        self.httpserver_entry.set_sensitive(self.http_radiobutton.get_active())
        self.httpdir_entry.set_sensitive(self.http_radiobutton.get_active())
                                     
    def getData(self):
        #specify to perform a fresh install
        buf = "\n" + "install"
        if self.cdrom_radiobutton.get_active():
            buf = buf + "\n" + "cdrom"
        elif self.nfs_radiobutton.get_active():
            buf = buf + "\n" + "nfs"
            buf = buf + " --server " + self.nfsserver_entry.get_text()
            buf = buf + " --dir " + self.nfsdir_entry.get_text()
        elif self.ftp_radiobutton.get_active():
            buf = buf + "\n" + "url"
            buf = buf + " --url ftp://" + self.ftpserver_entry.get_text()
            buf = buf + self.ftpdir_entry.get_text()		
        elif self.hd_radiobutton.get_active():
            buf = buf + "\n" + "harddrive"
            buf = buf + " --dir " + self.hddir_entry.get_text()
            buf = buf + " --partition " + self.hdpart_entry.get_text()        
        return buf
