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

#Kickstart Configurator X Configuration

import gtk
import gtk.glade
import gobject
import string
import getopt

class xconfig:

    def __init__(self, xml, kickstartData):
        self.kickstartData = kickstartData
        self.config_x_button = xml.get_widget("config_x_button")
        self.card_view = xml.get_widget("card_view")
        self.monitor_view = xml.get_widget("monitor_view")
        self.sync_button = xml.get_widget("sync_button")
        self.sync_table = xml.get_widget("sync_table")        
        self.startx_on_boot_button = xml.get_widget("startx_on_boot_button")
        self.xconfig_notebook = xml.get_widget("xconfig_notebook")        
        self.hsync_entry = xml.get_widget("hsync_entry")
        self.vsync_entry = xml.get_widget("vsync_entry")
        self.color_depth_combo = xml.get_widget("color_depth_combo")
        self.resolution_combo = xml.get_widget("resolution_combo")
        self.videoram_combo = xml.get_widget("videoram_combo")
        self.gnome_radiobutton = xml.get_widget("gnome_radiobutton")
        self.kde_radiobutton = xml.get_widget("kde_radiobutton")
        self.startxonboot_checkbutton = xml.get_widget("startxonboot_checkbutton")
        self.card_vbox = xml.get_widget("card_vbox")
        self.monitor_vbox = xml.get_widget("monitor_vbox")
        self.card_probe_check = xml.get_widget("card_probe_check")
        self.monitor_probe_check = xml.get_widget("monitor_probe_check")
        
        self.card_store = gtk.ListStore(gobject.TYPE_STRING)
        self.card_view.set_model(self.card_store)
        self.card_col = gtk.TreeViewColumn("", gtk.CellRendererText(), text = 0)
        self.card_view.append_column(self.card_col)
        
        self.monitor_store = gtk.ListStore(gobject.TYPE_STRING)
        self.monitor_view.set_model(self.monitor_store)
        self.monitor_col = gtk.TreeViewColumn("", gtk.CellRendererText(), text = 0)
        self.monitor_view.append_column(self.monitor_col)

        self.config_x_button.connect("toggled", self.toggleXconfig)
        self.monitor_probe_check.connect("toggled", self.on_monitor_probe_check_toggled)
        self.card_probe_check.connect("toggled", self.on_card_probe_check_toggled)
        self.sync_button.connect("toggled", self.toggle_sync)

        self.fill_card_list()
        self.fill_monitor_list()

        #add color depths
        color_depths = ["8", "16", "24", "32"]
        self.color_depth_combo.set_popdown_strings(color_depths)
        self.color_depth_combo.entry.set_editable(gtk.FALSE)

        #add resolutions
        resolutions = ["640x480", "800x600", "1024x768", "1152x864", "1280x1024", "1400x1050",
                       "1600x1200", "1920x1440", "2048x1536"]
        self.resolution_combo.set_popdown_strings(resolutions)
        self.resolution_combo.entry.set_editable(gtk.FALSE)
        
        #add video card RAM sizes to option menu
        vram_list = ["256 KB", "512 KB", "1 MB", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB"]
        self.videoram_combo.set_popdown_strings(vram_list)
        self.videoram_combo.entry.set_editable(gtk.FALSE)

        self.ramsize_dict = {"256 KB" : "256",
                             "512 KB" : "512",
                             "1 MB" : "1024",
                             "2 MB" : "2048",
                             "4 MB" : "4096",
                             "8 MB" : "8192",
                             "16 MB" : "16384",
                             "32 MB" : "32768",
                             "64 MB" : "65536",
                             }

    def fill_card_list(self):
        #add video cards to list
        try:
            cardsFile = open("/usr/share/hwdata/Cards", "r")
        except:
            raise RuntimeError, (_("Could not read video card database"))
            
        lines = cardsFile.readlines ()
        cardsFile.close ()
        lines.sort()
        for line in lines:
            line = string.strip (line)

            if len (line) > 4 and line[0:4] == 'NAME':
                name = line[5:]
                iter = self.card_store.append()
                self.card_store.set_value(iter, 0, name)

    def fill_monitor_list(self):
        #add monitors to list
        try:
            monitorFile = open("/usr/share/hwdata/MonitorsDB", "r")
        except:
            raise RuntimeError, (_("Could not read monitor database"))

        lines=monitorFile.readlines()
        lines.sort()
        monitorFile.close()
        mon_list = []
        
        for line in lines:
            line = string.strip (line)

            if line and line[0] != "#":
                values=string.split(line,";")
                manufacturer = string.strip(values[0])
                model = string.strip(values[1])
                id = string.strip(values[2])
                hsync = string.strip(values[3])
                vsync = string.strip(values[4])
                if model not in mon_list:
                    mon_list.append(model)
                    iter = self.monitor_store.append()
                    self.monitor_store.set_value(iter, 0, model)

    def on_card_probe_check_toggled(self, *args):
        self.card_vbox.set_sensitive(not self.card_probe_check.get_active())

    def on_monitor_probe_check_toggled(self, *args):
        self.monitor_vbox.set_sensitive(not self.monitor_probe_check.get_active())

    def toggleXconfig (self, args):
        config = self.config_x_button.get_active()
        #disable xconfig notebook
        self.xconfig_notebook.set_sensitive(config)

    def toggle_sync (self, args):
        sync_instead = self.sync_button.get_active()
        self.sync_table.set_sensitive(sync_instead)
        self.monitor_view.set_sensitive(not sync_instead)        

    def getData(self):
        if self.config_x_button.get_active():
            self.kickstartData.setSkipX(None)
            buf = ""
            #color depth - translate
            buf = "--depth=" + self.color_depth_combo.entry.get_text()
            #resolution
            buf = buf + " --resolution=" + self.resolution_combo.entry.get_text()            
            #default desktop
            if self.gnome_radiobutton.get_active():
                buf = buf + " --defaultdesktop=GNOME"
            elif self.kde_radiobutton.get_active():
                buf = buf + " --defaultdesktop=KDE"
            #startxonboot
            if self.startxonboot_checkbutton.get_active():
                buf = buf + " --startxonboot"

            if not self.card_probe_check.get_active():
                #video card and monitor
                temp, iter = self.card_view.get_selection().get_selected()
                card = self.card_store.get_value(iter, 0)
                buf = buf + " --card=\"" + card + "\""

                #translate MB to KB 
                buf = buf + " --videoram=" + self.ramsize_dict [self.videoram_combo.entry.get_text()]

            if not self.monitor_probe_check.get_active():
                if self.sync_button.get_active():
                    buf = buf + " --hsync=" + self.hsync_entry.get_text()
                    buf = buf + " --vsync=" + self.vsync_entry.get_text()
                else:
                    temp, iter = self.monitor_view.get_selection().get_selected()
                    name = self.monitor_store.get_value(iter, 0)
                    buf = buf + " --monitor=\"" + name + "\""

            self.kickstartData.setXconfig([buf])
        else:
            self.kickstartData.setSkipX(["skipx"])
            self.kickstartData.setXconfig(None)

    def fillData(self):
        if self.kickstartData.getSkipX():
            self.config_x_button.set_active(gtk.FALSE)
        elif self.kickstartData.getXconfig():
            self.config_x_button.set_active(gtk.TRUE)
            xLine = self.kickstartData.getXconfig()
            xLine = string.join (xLine, " ")
            xList = string.split(xLine, " --")

            for item in xList:
                if item[:2] != "--":
                    xList[xList.index(item)] = ("--" + item)

            for opt in xList:
                opt = string.replace(opt, "=", " ")
            
                if opt == "--startxonboot":
                    self.startxonboot_checkbutton.set_active(gtk.TRUE)

                if opt[:16] == "--defaultdesktop":
                    value = opt[16:]
                    if string.lower(value) == "gnome":
                        self.gnome_radiobutton.set_active(gtk.TRUE)
                    if string.lower(value) == "kde":
                        self.kde_radiobutton.set_active(gtk.TRUE)

                if opt[:7] == "--depth":
                    value = opt[7:]
                    self.color_depth_combo.entry.set_text(string.strip(value))

                if opt[:12] == "--resolution":
                    value = opt[12:]
                    self.resolution_combo.entry.set_text(string.strip(value))

                if opt[:6] == "--card":
                    value = string.strip(opt[6:])
                    self.card_probe_check.set_active(gtk.FALSE)
                    value = string.replace(value, '"', '')

                    iter = self.card_store.get_iter_first()

                    while iter:
                        if self.card_store.get_value(iter, 0) == value:
                            path = self.card_store.get_path(iter)
                            self.card_view.set_cursor(path, self.card_col, gtk.FALSE)
                            self.card_view.scroll_to_cell(path, self.card_col, gtk.TRUE, 0.5, 0.5)
                        iter = self.card_store.iter_next(iter)

                if opt[:10] == "--videoram":
                    value = opt[10:]

                    for size in self.ramsize_dict.keys():
                        if int(value) == int(self.ramsize_dict[size]):
                            self.videoram_combo.entry.set_text(size)                            

                if opt[:9] == "--monitor":
                    opt = string.strip(opt[9:])
                    self.monitor_probe_check.set_active(gtk.FALSE)
                    value = string.replace(value, '"', '')

                    iter = self.monitor_store.get_iter_first()

                    while iter:
                        if self.monitor_store.get_value(iter, 0) == value:
                            path = self.monitor_store.get_path(iter)
                            self.monitor_view.set_cursor(path, self.monitor_col, gtk.FALSE)
                            self.monitor_view.scroll_to_cell(path, self.monitor_col, gtk.TRUE, 0.5, 0.5)
                        iter = self.monitor_store.iter_next(iter)

                if opt[:7] == "--hsync":
                    value = opt[7:]
                    self.sync_button.set_active(gtk.TRUE)
                    self.hsync_entry.set_text(string.strip(value))
                    self.monitor_probe_check.set_active(gtk.FALSE)

                if opt[:7] == "--vsync":
                    value = opt[7:]
                    self.sync_button.set_active(gtk.TRUE)
                    self.vsync_entry.set_text(string.strip(value))
                    self.monitor_probe_check.set_active(gtk.FALSE)
