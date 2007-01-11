## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003 Brent Fox <bfox@redhat.com>
##                                      Tammy Fox <tfox@redhat.com>

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
import string
import kickstartGui

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class install:
  
    def __init__(self, parent_class, xml, store, view, notebook, ksHandler):
        self.xml = xml
        self.parent_class = parent_class
        self.store = store
        self.view = view
        self.notebook = notebook
        self.ks = ksHandler
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
        self.ftpuser_entry.set_sensitive(False)
        self.ftppasswd_entry.set_sensitive(False)

    def toggleFtp (self, args):
        userpass = self.ftpuserpass_checkbutton.get_active()
        self.ftpuser_entry.set_sensitive(userpass)
        self.ftppasswd_entry.set_sensitive(userpass)

    def toggleInstall (self, args):
        #gray out package selection and partitions if upgrade
        install = self.install_radiobutton.get_active()
        self.parent_class.installTypeChanged(install)

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
                                     
    def formToKickstart(self):
        self.ks.upgrade(upgrade=self.upgrade_radiobutton.get_active())

        if self.cdrom_radiobutton.get_active():
            self.ks.method.method = "cdrom"
        elif self.nfs_radiobutton.get_active():
            server = self.nfsserver_entry.get_text()
            dir = self.nfsdir_entry.get_text()

            if server == "":
                self.showDialog(_("Please enter an NFS server."), self.nfsserver_entry)
                return None
            if dir == "":
                self.showDialog(_("Please enter an NFS directory."), self.nfsdir_entry)
                return None
            if server [-1] == "/":
                server = server[:-1]

            self.ks.method.method = "nfs"
            self.ks.method.server = server
            self.ks.method.dir = dir
        elif self.ftp_radiobutton.get_active():
            ftpserver = string.strip(self.ftpserver_entry.get_text())
            if ftpserver == "":
                self.showDialog(_("Please enter an FTP server."), self.ftpserver_entry)
                return None
            if ftpserver[:6] == "ftp://":
                ftpserver = ftpserver[6:]
            if ftpserver[-1] == "/":
                ftpserver = ftpserver[:-1]
            if self.ftpdir_entry.get_text() == "":
                self.showDialog(_("Please enter an FTP directory."), self.ftpserver_entry)
                return None

            buf = "ftp://"
            if self.ftpuserpass_checkbutton.get_active():
                if self.ftpuser_entry.get_text() == "":
                    self.showDialog(_("Please enter an FTP user name."), self.ftpuser_entry)
                    return None
                if self.ftppasswd_entry.get_text() == "":
                    self.showDialog(_("Please enter an FTP password."), self.ftpuser_entry)
                    return None

                buf = buf + self.ftpuser_entry.get_text() + ":" + self.ftppasswd_entry.get_text() + "@"
            
            buf = buf + ftpserver
            directory = self.ftpdir_entry.get_text()		
            if directory[0] == '/':
                buf = buf + directory
            else:
                buf = buf + "/" + directory

            self.ks.method.method = "url"
            self.ks.method.url = buf
        elif self.http_radiobutton.get_active():
            if self.httpserver_entry.get_text() == "":
                self.showDialog(_("Please enter an HTTP server."), self.httpserver_entry)
                return None
            if self.httpdir_entry.get_text() == "":
                self.showDialog(_("Please enter an HTTP server directory."), self.httpdir_entry)
                return None

            loc = string.strip(self.httpserver_entry.get_text())

            if loc[:7] == "http://":
                #strip the "http://" out
                loc = loc[7:]
            if loc [-1] == "/":
                loc = loc[:-1]

            buf = "http://" + loc
            directory = self.httpdir_entry.get_text()		
            if directory[0] == '/':
                buf = buf + directory
            else:
                buf = buf + "/" + directory

            self.ks.method.method = "url"
            self.ks.method.url = buf
        elif self.hd_radiobutton.get_active():
            if self.hddir_entry.get_text() == "":
                self.showDialog(_("Please enter a hard drive directory."), self.hddir_entry)
                return None
            if self.hdpart_entry.get_text() == "":
                self.showDialog(_("Please enter a hard drive partition."), self.hdpart_entry)
                return None

            self.ks.method.method = "harddrive"
            self.ks.method.partition = self.hdpart_entry.get_text()
            self.ks.method.dir = self.hddir_entry.get_text()

        return 0

    def showDialog(self, text, widget):
            dlg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, text)
            dlg.set_title(_("Error"))
            dlg.set_default_size(100, 100)
            dlg.set_position (gtk.WIN_POS_CENTER)
            dlg.set_icon(kickstartGui.iconPixbuf)
            dlg.set_border_width(2)
            dlg.set_modal(True)
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

    def splitUrl(self, data):
        tokens = string.split(data, "/")
        host = tokens[0]
        dir = tokens[1:]
        dir = string.join(dir, '/')
        dir = "/" + dir
        return host, dir

    def applyKickstart(self):
        if self.ks.upgrade.upgrade == False:
            self.install_radiobutton.set_active(True)            
        else:
            self.upgrade_radiobutton.set_active(True)

        if self.ks.method.method == "cdrom":
            self.cdrom_radiobutton.set_active(True)

        elif self.ks.method.method == "harddrive":
            self.hd_radiobutton.set_active(True)

            if self.ks.method.partition != "":
                self.hdpart_entry.set_text(self.ks.method.partition)
            if self.ks.method.dir != "":
                self.hddir_entry.set_text(self.ks.method.dir)

        elif self.ks.method.method == "nfs":
            self.nfs_radiobutton.set_active(True)

            if self.ks.method.server != "":
                self.nfsserver_entry.set_text(self.ks.method.server)
            if self.ks.method.dir  != "":
                self.nfsdir_entry.set_text(self.ks.method.dir)

        elif self.ks.method.method == "url":
            tokens = string.split(self.ks.method.url, "://")

            protocol = tokens[0]
            data = tokens[1]

            if protocol == "ftp":
                self.ftp_radiobutton.set_active(True)

                if "@" in data:
                    self.ftpuserpass_checkbutton.set_active(True)

                    loginData, data = string.split(data, "@")

                    username, password = string.split(loginData, ":")
                    self.ftpuser_entry.set_text(username)
                    self.ftppasswd_entry.set_text(password)

                    host, dir = self.splitUrl(data)
                    self.ftpserver_entry.set_text(host)
                    self.ftpdir_entry.set_text(dir)

                else:
                    host, dir = self.splitUrl(data)

            elif protocol == "http":
                host, dir = self.splitUrl(data)
                
                self.http_radiobutton.set_active(True)
                self.httpserver_entry.set_text(host)
                self.httpdir_entry.set_text(dir)


