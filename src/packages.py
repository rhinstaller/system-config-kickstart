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

#Kickstart Configurator Package Selection

from gtk import *
import GtkExtra
import string
import checklist
import libglade
import rpm
import string


class Packages:

    def __init__(self, xml):
        self.list = xml.get_widget("list")

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
            checkbox = GtkCheckButton(pkg)
            self.list.pack_start(checkbox)


    def getData(self):
        buf = ""
        buf = buf + "\n" + "%packages"

        boxes = self.list.children()
        for box in boxes:
            if box.get_active():
                package = box.children()[0]
                label = package.get()
                buf = buf + "\n" + "@" + label

        return buf
