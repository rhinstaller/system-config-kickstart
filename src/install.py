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
import kickstartGui

##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class install:
  
    def __init__(self, xml, store, view, notebook, bootloader_class):
        self.xml = xml
        self.store = store
        self.view = view
        self.notebook = notebook
        self.bootloader_class = bootloader_class
        self.install_radiobutton = xml.get_widget("install_radiobutton")
        self.upgrade_radiobutton = xml.get_widget("upgrade_radiobutton")
        self.partitioning_frame = xml.get_widget("partitioning_frame")
        self.pkg_selection_frame = xml.get_widget("pkg_selection_frame")
        self.install_option_vbox = xml.get_widget("install_option_vbox")

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
        self.ftpuser_entry.set_sensitive(gtk.FALSE)
        self.ftppasswd_entry.set_sensitive(gtk.FALSE)

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
            if self.nfsserver_entry.get_text() == "":
                self.showDialog(_("Please enter an NFS server."), self.nfsserver_entry)
                return
            if self.nfsdir_entry.get_text() == "":
                self.showDialog(_("Please enter an NFS directory."), self.nfsdir_entry)
                return
            buf = buf + " --server " + self.nfsserver_entry.get_text()
            buf = buf + " --dir " + self.nfsdir_entry.get_text()
            data.append(buf)
        elif self.ftp_radiobutton.get_active():
            if self.ftpserver_entry.get_text() == "":
                self.showDialog(_("Please enter an FTP server."), self.ftpserver_entry)
                return
            if self.ftpdir_entry.get_text() == "":
                self.showDialog(_("Please enter an FTP directory."), self.ftpserver_entry)
                return

            data.append("#Use FTP installation media")
            buf = "url"
            buf = buf + " --url ftp://"
            if self.ftpuserpass_checkbutton.get_active():
                if self.ftpuser_entry.get_text() == "":
                    self.showDialog(_("Please enter an FTP user name."), self.ftpuser_entry)
                    return
                if self.ftppasswd_entry.get_text() == "":
                    self.showDialog(_("Please enter an FTP password."), self.ftpuser_entry)
                    return

                buf = buf + self.ftpuser_entry.get_text() + ":" + self.ftppasswd_entry.get_text() + "@"
            
            buf = buf + self.ftpserver_entry.get_text()
            directory = self.ftpdir_entry.get_text()		
            if directory[0] == '/':
                buf = buf + directory
            else:
                buf = buf + "/" + directory

            data.append(buf)
        elif self.http_radiobutton.get_active():
            if self.httpserver_entry.get_text() == "":
                self.showDialog(_("Please enter an HTTP server."), self.httpserver_entry)
                return
            if self.httpdir_entry.get_text() == "":
                self.showDialog(_("Please enter an HTTP server directory."), self.httpdir_entry)
                return
            data.append("#Use HTTP installation media")
            buf = "url"
            buf = buf + " --url http://" + self.httpserver_entry.get_text()
            directory = self.httpdir_entry.get_text()		
            if directory[0] == '/':
                buf = buf + directory
            else:
                buf = buf + "/" + directory

            data.append(buf)
        elif self.hd_radiobutton.get_active():
            if self.hddir_entry.get_text() == "":
                self.showDialog(_("Please enter a hard drive directory."), self.hddir_entry)
                return
            if self.hdpart_entry.get_text() == "":
                self.showDialog(_("Please enter a hard drive partition."), self.hdpart_entry)
                return
            data.append("#Use Hard drive installation media")
            buf = "harddrive"
            buf = buf + " --dir " + self.hddir_entry.get_text()
            buf = buf + " --partition " + self.hdpart_entry.get_text()        
            data.append(buf)
        return data

    def showDialog(self, text, widget):
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_icon(kickstartGui.iconPixbuf)
            dlg.set_border_width(2)
            dlg.set_modal(gtk.TRUE)
            toplevel = self.xml.get_widget("main_window")
            dlg.set_transient_for(toplevel)
            dlg.run()
            dlg.hide()

            iter = self.store.get_iter_first()
            iter = self.store.iter_next(iter)
            self.view.get_selection().select_iter(iter)
            self.notebook.set_current_page(1)
            widget.grab_focus()
            return
        
