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

#Kickstart Configurator Package Selection

import gtk
import gtk.glade
import gobject
import string


class Packages:

    def __init__(self, xml):
        self.package_view = xml.get_widget("package_view")
        self.resolve_deps_checkbutton = xml.get_widget("resolve_deps_checkbutton")
        self.ignore_deps_checkbutton = xml.get_widget("ignore_deps_checkbutton")

        self.resolve_deps_checkbutton.connect("toggled", self.on_resolve_deps_toggled)
        self.ignore_deps_checkbutton.connect("toggled", self.on_ignore_deps_toggled)        
        
        self.package_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.package_view.set_model(self.package_store)
        self.checkbox = gtk.CellRendererToggle()
        col = gtk.TreeViewColumn('', self.checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.checkbox.connect("toggled", self.packageToggled)
        self.package_view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        self.package_view.append_column(col)

        packageList = ["Printing Support","Classic X Window System",
        "X Window System","GNOME","KDE",
        "Sound and Multimedia Support","Network Support",
        "Dialup Support","Messaging and Web Tools",
        "Graphics and Image Manipulation","News Server",
        "NFS File Server","Windows File Server",
        "Anonymous FTP Server","SQL Database Server",
        "Web Server","Router / Firewall","DNS Name Server",
        "Network Managed Workstation","Authoring and Publishing",
        "Emacs","Utilities","Legacy Application Support",
        "Software Development","Kernel Development",
        "Windows Compatibility / Interoperability",
        "Games and Entertainment", "Everything"]

        for pkg in packageList:
            iter = self.package_store.append()
            self.package_store.set_value(iter, 1, pkg)

    def on_resolve_deps_toggled(self, *args):
        active = self.resolve_deps_checkbutton.get_active()
        self.ignore_deps_checkbutton.set_sensitive(not active)

    def on_ignore_deps_toggled(self, *args):
        active = self.ignore_deps_checkbutton.get_active()
        self.resolve_deps_checkbutton.set_sensitive(not active)        

    def packageToggled(self, data, row):
        iter = self.package_store.get_iter((int(row),))
        val = self.package_store.get_value(iter, 0)
        self.package_store.set_value(iter, 0 , not val)

    def getData(self):
        data = []
        data.append("")

        if self.resolve_deps_checkbutton.get_active() == 1:
            data.append("%packages --resolvedeps")
        elif self.ignore_deps_checkbutton.get_active() == 1:
            data.append("%packages --ignoredeps")
        else:
            data.append("%packages")            

        iter = self.package_store.get_iter_first()

        #Loop over the package list and see what was selected
        while iter:
            if self.package_store.get_value(iter, 0) == gtk.TRUE:
                data.append("@" + self.package_store.get_value(iter, 1))
            iter = self.package_store.iter_next(iter)

        return data
