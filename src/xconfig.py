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

        xml.signal_autoconnect (
            { "toggleXconfig" : self.toggleXconfig,
              "toggle_vc_monitor": self.toggle_vc_monitor,
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
        
    def toggleXconfig (self, args):
        config = self.config_x_button.get_active()
        #disable xconfig notebook
        self.xconfig_notebook.set_sensitive(config)

    def toggle_vc_monitor (self, args):
        config = self.probe_x_button.get_active()
        print config
        self.video_card_swindow.set_sensitive(config)
        self.monitor_swindow.set_sensitive(config)
        self.video_card_list.set_sensitive(config)
        self.monitor_list.set_sensitive(config)

    def getData(self):
        if self.config_x_button.get_active():
            buf = "\n" + "xconfig "
        else:
            buf = "\n" + "#Do not configure the X Window System"
        return buf


