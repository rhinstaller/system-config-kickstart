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


##
## I18N
##
import gettext
gettext.bindtextdomain ("redhat-config-kickstart", "/usr/share/locale")
gettext.textdomain ("redhat-config-kickstart")
_=gettext.gettext

class Packages:

    def __init__(self, xml):

        self.resolve_deps_checkbutton = xml.get_widget("resolve_deps_checkbutton")
        self.ignore_deps_checkbutton = xml.get_widget("ignore_deps_checkbutton")

        self.resolve_deps_checkbutton.connect("toggled", self.on_resolve_deps_toggled)
        self.ignore_deps_checkbutton.connect("toggled", self.on_ignore_deps_toggled)        

        self.desktops_eventbox = xml.get_widget("desktops_eventbox")
        self.desktops_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.desktops_label = xml.get_widget("desktops_label")
        self.desktops_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.desktops_label.get(),))

        self.applications_eventbox = xml.get_widget("applications_eventbox")
        self.applications_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.applications_label = xml.get_widget("applications_label")
        self.applications_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.applications_label.get(),))

        self.servers_eventbox = xml.get_widget("servers_eventbox")
        self.servers_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.servers_label = xml.get_widget("servers_label")
        self.servers_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.servers_label.get(),))

        self.development_eventbox = xml.get_widget("development_eventbox")
        self.development_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.development_label = xml.get_widget("development_label")
        self.development_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.development_label.get(),))

        self.system_eventbox = xml.get_widget("system_eventbox")
        self.system_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.system_label = xml.get_widget("system_label")
        self.system_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.system_label.get(),))

        self.miscellaneous_eventbox = xml.get_widget("miscellaneous_eventbox")
        self.miscellaneous_eventbox.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#737db5"))
        self.miscellaneous_label = xml.get_widget("miscellaneous_label")
        self.miscellaneous_label.set_markup("<span foreground='white'><big><b>%s</b></big></span>" % (self.miscellaneous_label.get(),))

        self.desktops_view = xml.get_widget("desktops_view")
        self.desktops_view.get_selection().set_mode(gtk.SELECTION_NONE)
        self.applications_view = xml.get_widget("applications_treeview")
        self.applications_view.get_selection().set_mode(gtk.SELECTION_NONE)
        self.servers_view = xml.get_widget("servers_treeview")
        self.servers_view.get_selection().set_mode(gtk.SELECTION_NONE)
        self.development_view = xml.get_widget("development_treeview")
        self.development_view.get_selection().set_mode(gtk.SELECTION_NONE)
        self.systems_view = xml.get_widget("systems_treeview")
        self.systems_view.get_selection().set_mode(gtk.SELECTION_NONE)
        self.miscellaneous_view = xml.get_widget("miscellaneous_treeview")
        self.miscellaneous_view.get_selection().set_mode(gtk.SELECTION_NONE)

        self.desktops_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.desktops_view.set_model(self.desktops_store)

        self.applications_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.applications_view.set_model(self.applications_store)

        self.servers_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.servers_view.set_model(self.servers_store)

        self.development_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.development_view.set_model(self.development_store)

        self.system_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.systems_view.set_model(self.system_store)

        self.miscellaneous_store = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.miscellaneous_view.set_model(self.miscellaneous_store)

        self.create_columns(self.desktops_view, self.desktops_store)
        self.create_columns(self.applications_view, self.applications_store)
        self.create_columns(self.servers_view, self.servers_store)
        self.create_columns(self.development_view, self.development_store)
        self.create_columns(self.systems_view, self.system_store)
        self.create_columns(self.miscellaneous_view, self.miscellaneous_store)

        desktopsList = ["X Window System",
                       "GNOME Desktop Environment",
                       "KDE Desktop Environment"
                        ]
        applicationsList = ["Editors",
                            "Engineering and Scientific",
                            "Graphical Internet",
                            "Text-based Internet",
                            "Office/Productivity",
                            "Sound and Video",
                            "Graphics",
                            "Games and Entertainment",
                            "Authoring and Publishing"
                            ]
        serversList = ["Server Configuration Tools",                       
                       "Web Server",
                       "Mail Server",
                       "Windows File Server",
                       "DNS Name Server", 
                       "FTP Server",
                       "SQL Database Server",
                       "News Server",
                       "Network Servers"
                       ]
        developmentList = ["Development Tools",
                           "Kernel Development",
                           "X Software Development",                       
                           "GNOME Software Development",
                           "KDE Software Development"
                           ]
        systemList = ["Administration Tools",
                      "System Tools",
                      "Printing Support"
                      ]
        miscellaneousList = ["Minimal",
                             "Everything"                       
                             ]

        for pkg in desktopsList:
            iter = self.desktops_store.append()
            self.desktops_store.set_value(iter, 1, pkg)

        for pkg in applicationsList:
            iter = self.applications_store.append()
            self.applications_store.set_value(iter, 1, pkg)

        for pkg in serversList:
            iter = self.servers_store.append()
            self.servers_store.set_value(iter, 1, pkg)

        for pkg in developmentList:
            iter = self.development_store.append()
            self.development_store.set_value(iter, 1, pkg)

        for pkg in systemList:
            iter = self.system_store.append()
            self.system_store.set_value(iter, 1, pkg)

        for pkg in miscellaneousList:
            iter = self.miscellaneous_store.append()
            self.miscellaneous_store.set_value(iter, 1, pkg)

    def create_columns(self, view, store):
        self.checkbox = gtk.CellRendererToggle()
        col = gtk.TreeViewColumn('', self.checkbox, active = 0)
        col.set_fixed_width(20)
        col.set_clickable(gtk.TRUE)
        self.checkbox.connect("toggled", self.packageToggled, store)
        view.append_column(col)

        col = gtk.TreeViewColumn("", gtk.CellRendererText(), text=1)
        view.append_column(col)

    def on_resolve_deps_toggled(self, *args):
        active = self.resolve_deps_checkbutton.get_active()
        self.ignore_deps_checkbutton.set_sensitive(not active)

    def on_ignore_deps_toggled(self, *args):
        active = self.ignore_deps_checkbutton.get_active()
        self.resolve_deps_checkbutton.set_sensitive(not active)        

    def packageToggled(self, data, row, store):
        iter = store.get_iter((int(row),))
        val = store.get_value(iter, 0)
        store.set_value(iter, 0 , not val)

    def getData(self):
        data = []
        data.append("")

        if self.resolve_deps_checkbutton.get_active() == 1:
            data.append("%packages --resolvedeps")
        elif self.ignore_deps_checkbutton.get_active() == 1:
            data.append("%packages --ignoredeps")
        else:
            data.append("%packages")            

        data = self.getPkgData(self.desktops_store, data)
        data = self.getPkgData(self.applications_store, data)
        data = self.getPkgData(self.servers_store, data)
        data = self.getPkgData(self.development_store, data)
        data = self.getPkgData(self.system_store, data)
        data = self.getPkgData(self.miscellaneous_store, data)        

        return data

    def getPkgData(self, store, data):
        
        iter = store.get_iter_first()

        #Loop over the package list and see what was selected
        while iter:
            if store.get_value(iter, 0) == gtk.TRUE:
                data.append("@" + store.get_value(iter, 1))
            iter = store.iter_next(iter)

        return data
