#!/usr/bin/env python

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002 Brent Fox <bfox@redhat.com>
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

import gtk
import gtk.glade
#from gtk import *
#import GtkExtra
#import libglade

class install:
  
    def __init__(self, xml, bootloader_class):
        self.bootloader_class = bootloader_class
        self.install_radiobutton = xml.get_widget("install_radiobutton")
        self.upgrade_radiobutton = xml.get_widget("upgrade_radiobutton")
        self.partitioning_frame = xml.get_widget("partitioning_frame")
        self.pkg_selection_frame = xml.get_widget("pkg_selection_frame")

        self.cdrom_radiobutton = xml.get_widget("cdrom_radiobutton")
        self.nfs_radiobutton = xml.get_widget("nfs_radiobutton")
        self.ftp_radiobutton = xml.get_widget("ftp_radiobutton")
        self.http_radiobutton = xml.get_widget("http_radiobutton")
        self.hd_radiobutton = xml.get_widget("hd_radiobutton")		

        self.nfsdir_label = xml.get_widget("nfsdir_label")
        self.nfsserver_label = xml.get_widget("nfsserver_label")
        self.ftpdir_label = xml.get_widget("ftpdir_label")
        self.ftpserver_label = xml.get_widget("ftpserver_label")
        self.ftpuser_label = xml.get_widget("ftpuser_label")
        self.ftppasswd_label = xml.get_widget("ftppasswd_label")        
        self.hdpart_label = xml.get_widget("hdpart_label")
        self.hddir_label = xml.get_widget("hddir_label")
        self.httpserver_label = xml.get_widget("httpserver_label")
        self.httpdir_label = xml.get_widget("httpdir_label")

        self.nfsdir_entry = xml.get_widget("nfsdir_entry")
        self.nfsserver_entry = xml.get_widget("nfsserver_entry")
        self.ftpdir_entry = xml.get_widget("ftpdir_entry")
        self.ftpserver_entry = xml.get_widget("ftpserver_entry")
        self.ftpuser_entry = xml.get_widget("ftpuser_entry")
        self.ftppasswd_entry = xml.get_widget("ftppasswd_entry")        
        self.hdpart_entry = xml.get_widget("hdpart_entry")
        self.hddir_entry = xml.get_widget("hddir_entry")
        self.httpserver_entry = xml.get_widget("httpserver_entry")
        self.httpdir_entry = xml.get_widget("httpdir_entry")

        self.ftpuserpass_checkbutton = xml.get_widget("ftpuserpass_checkbutton")

        self.install_notebook = xml.get_widget("install_notebook")
        
        self.install_radiobutton.connect("toggled", self.toggleInstall)
        self.cdrom_radiobutton.connect("toggled", self.setState)
        self.nfs_radiobutton.connect("toggled", self.setState)
        self.ftp_radiobutton.connect("toggled", self.setState)
        self.http_radiobutton.connect("toggled", self.setState)
        self.hd_radiobutton.connect("toggled", self.setState)

        self.ftpuserpass_checkbutton.connect("toggled", self.toggleFtp)

    def toggleFtp (self, args):
        userpass = self.ftpuserpass_checkbutton.get_active()
        self.ftpuser_entry.set_sensitive(userpass)
        self.ftppasswd_entry.set_sensitive(userpass)
    

    def toggleInstall (self, args):
        #gray out package selection and partitions if upgrade
        install = self.install_radiobutton.get_active()
        self.partitioning_frame.set_sensitive(install)
        self.pkg_selection_frame.set_sensitive(install)            
        self.bootloader_class.upgrade_bootloader_radio.set_sensitive(not install)

    def setState (self, args):
        if self.cdrom_radiobutton.get_active():
            self.install_notebook.set_current_page(0)
            return
        elif self.nfs_radiobutton.get_active():
            self.install_notebook.set_current_page(1)
            return
        elif self.ftp_radiobutton.get_active():
            self.install_notebook.set_current_page(2)
            return
        elif self.http_radiobutton.get_active():
            self.install_notebook.set_current_page(3)
            return
        elif self.hd_radiobutton.get_active():
            self.install_notebook.set_current_page(4)
                                     
    def getData(self):
        data = []
        data.append("")
        if self.install_radiobutton.get_active():
            data.append("#Install Red Hat Linux instead of upgrade")
            data.append("install")
        elif self.upgrade_radiobutton.get_active():
            data.append("#Upgrade existing installation")
            data.append("upgrade")

        data.append("")
        if self.cdrom_radiobutton.get_active():
            data.append("#Use CDROM installation media")
            data.append("cdrom")
        elif self.nfs_radiobutton.get_active():
            data.append("#Use NFS installation media")
            buf = "nfs"
            buf = buf + " --server " + self.nfsserver_entry.get_text()
            buf = buf + " --dir " + self.nfsdir_entry.get_text()
            data.append(buf)
        elif self.ftp_radiobutton.get_active():
            data.append("#Use FTP installation media")
            buf = "url"
            buf = buf + " --url ftp://"
            if self.ftpuserpass_checkbutton.get_active():
                buf = buf + self.ftpuser_entry.get_text() + ":" + self.ftppasswd_entry.get_text() + "@"

            
            buf = buf + self.ftpserver_entry.get_text()
            buf = buf + "/" + self.ftpdir_entry.get_text()		
            data.append(buf)
        elif self.http_radiobutton.get_active():
            data.append("#Use HTTP installation media")
            buf = "url"
            buf = buf + " --url http://" + self.httpserver_entry.get_text()
            buf = buf + "/" + self.httpdir_entry.get_text()        
            data.append(buf)
        elif self.hd_radiobutton.get_active():
            data.append("#Use Hard drive installation media")
            buf = "harddrive"
            buf = buf + " --dir " + self.hddir_entry.get_text()
            buf = buf + " --partition " + self.hdpart_entry.get_text()        
            data.append(buf)
        return data
