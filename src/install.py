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
        self.nfsdir_entry = xml.get_widget("nfsdir_entry")
        self.nfsserver_entry = xml.get_widget("nfsserver_entry")
        self.ftpdir_entry = xml.get_widget("ftpdir_entry")
        self.ftpserver_entry = xml.get_widget("ftpserver_entry")
        self.hdpart_entry = xml.get_widget("hdpart_entry")
        self.hddir_entry = xml.get_widget("hddir_entry")

        xml.signal_autoconnect (
            { "enableFTP" : self.enableFTP,
              "enableNFS" : self.enableNFS,
              "enableHD" : self.enableHD,
              "disableFTP" : self.disableFTP,
              "disableNFS" : self.disableNFS,
              "disableHD" : self.disableHD,
              } )

    def enableNFS(self, args):
            self.nfsserver_entry.set_sensitive(self.nfs_radiobutton.get_active())
            self.nfsdir_entry.set_sensitive(self.nfs_radiobutton.get_active())

    def disableNFS(self, args):
            self.nfsserver_entry.set_state(STATE_INSENSITIVE)
            self.nfsdir_entry.set_state(STATE_INSENSITIVE)

    def enableFTP(self, args):
            self.ftpserver_entry.set_sensitive(self.ftp_radiobutton.get_active())
            self.ftpdir_entry.set_sensitive(self.ftp_radiobutton.get_active())

    def disableFTP(self, args):
            self.ftpserver_entry.set_state(STATE_INSENSITIVE)
            self.ftpdir_entry.set_state(STATE_INSENSITIVE)

    def enableHD(self, args):
            self.hdpart_entry.set_sensitive(self.hd_radiobutton.get_active())
            self.hddir_entry.set_sensitive(self.hd_radiobutton.get_active())

    def disableHD(self, args):
            self.hdpart_entry.set_state(STATE_INSENSITIVE)
            self.hddir_entry.set_state(STATE_INSENSITIVE)

    def getData(self):
        buf = ""
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
