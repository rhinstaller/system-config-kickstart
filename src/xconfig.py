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

#Kickstart Configurator X Configuration

from gtk import *
import GtkExtra
import libglade
import string

class xconfig:

    def __init__(self, xml):
        self.config_x_button = xml.get_widget("config_x_button")
        self.probe_x_button = xml.get_widget("probe_x_button")
        self.video_card_swindow = xml.get_widget("video_card_swindow")
        self.video_card_clist = xml.get_widget("video_card_clist")
        self.monitor_swindow = xml.get_widget("monitor_swindow")
        self.monitor_clist = xml.get_widget("monitor_clist")
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

        xml.signal_autoconnect (
            { "toggleXconfig" : self.toggleXconfig,
              "toggle_vc_monitor" : self.toggle_vc_monitor,
              "select_monitor" : self.select_monitor,
              "select_videocard" : self.select_videocard,
              })

        #add video cards to list
        cardsFile = open("Cards")
        lines = cardsFile.readlines ()
        cardsFile.close ()
        card = {}
        Video_cardslist = {}
        name = None
        for line in lines:
            line = string.strip (line)
            if not line and name:
                Video_cardslist[name] = card
                name = None
                continue
            #skip comments
            if line and line[0] == '#':
                continue
            if len (line) > 4 and line[0:4] == 'NAME':
                name = line[5:]
                name_list = [name]
                self.video_card_clist.append(name_list)


        #add monitors to list
        monitorFile = open("MonitorsDB", "r")
        lines=monitorFile.readlines()
        monitorFile.close()
        
        monitors = []
        for line in lines:
            line = string.strip (line)
            if not line:
                continue
            if line and line[0] == "#":
                continue
            values=string.split(line,";")
            manufacturer = string.strip(values[0])
            model = string.strip(values[1])
            id = string.strip(values[2])
            hsync = string.strip(values[3])
            vsync = string.strip(values[4])
            model_list = [model]
            self.monitor_clist.append(model_list)
            #grab hsync and vsync from cards DB
            #FIXME

        #add color depths
        color_depths = ["8", "16", "32", "64"]
        self.color_depth_combo.set_popdown_strings(color_depths)
        self.color_depth_combo.entry.set_editable(FALSE)

        #add resolutions
        resolutions = ["640x480", "800x600", "1024x768", "1152x864", "1280x1024", "1400x1050", "1600x1200"]
        self.resolution_combo.set_popdown_strings(resolutions)
        self.resolution_combo.entry.set_editable(FALSE)
        
        #add video card RAM sizes to option menu
        vram_list = ["256 KB", "512 KB", "1 MB", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB"]
        self.videoram_combo.set_popdown_strings(vram_list)
        self.videoram_combo.entry.set_editable(FALSE)

    def toggleXconfig (self, args):
        config = self.config_x_button.get_active()
        #disable xconfig notebook
        self.xconfig_notebook.set_sensitive(config)

    def toggle_vc_monitor (self, args):
        showLists = not self.probe_x_button.get_active()
        self.video_card_swindow.set_sensitive(showLists)
        self.monitor_swindow.set_sensitive(showLists)
        self.video_card_clist.set_sensitive(showLists)
        self.monitor_clist.set_sensitive(showLists)

    def select_monitor(self, event, row, column, data):
        self.selected_monitor_row = row
        
    def select_videocard(self, event, row, column, data):
        self.selected_vc_row = row

    def getData(self):
        if self.config_x_button.get_active():
            buf = "\n" + "xconfig "
            if self.probe_x_button.get_active():
                continue
            else:
                #monitor 
                buf = buf + " --monitor \"" + self.monitor_clist.get_text(self.selected_monitor_row,0) + "\""
                #card
                buf = buf + " --card \"" + self.video_card_clist.get_text(self.selected_vc_row,0) + "\""
            #hsync
            buf = buf + " --hsync " + self.hsync_entry.get_text()
            #vsync 
            buf = buf + " --vsync " + self.vsync_entry.get_text()           
            #color depth - translate
            buf = buf + " --depth " + self.color_depth_combo.entry.get_text()
            #resolution
            buf = buf + " --resolution " + self.resolution_combo.entry.get_text()            
            #default desktop
            if self.gnome_radiobutton.get_active():
                buf = buf + " defaultdesktop=GNOME"
            elif self.kde_radiobutton.get_active():
                buf = buf + " defaultdesktop=KDE"
            #startxonboot
            if self.startxonboot_checkbutton.get_active():
                buf = buf + "  --startxonboot"
        else:
            buf = "\n" + "#Do not configure the X Window System"
        return buf


