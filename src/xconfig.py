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

#Kickstart Configurator X Configuration

import gtk
import gtk.glade
import gobject
import string
import getopt
from pykickstart.constants import *

##
## I18N
##
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
gtk.glade.bindtextdomain(domain)

class xconfig:

    def __init__(self, xml, ksHandler):
        self.ks = ksHandler
        self.xconfig_vbox = xml.get_widget("xconfig_vbox")
        self.xconfig_label_box = xml.get_widget("xconfig_label_box")
        self.config_x_button = xml.get_widget("config_x_button")
        self.driver_view = xml.get_widget("driver_view")
        self.monitor_view = xml.get_widget("monitor_view")
        self.sync_button = xml.get_widget("sync_button")
        self.sync_table = xml.get_widget("sync_table")        
        self.xconfig_notebook = xml.get_widget("xconfig_notebook")        
        self.hsync_entry = xml.get_widget("hsync_entry")
        self.vsync_entry = xml.get_widget("vsync_entry")
        self.color_depth_combo = xml.get_widget("color_depth_combo")
        self.resolution_combo = xml.get_widget("resolution_combo")
        self.videoram_combo = xml.get_widget("videoram_combo")
        self.gnome_radiobutton = xml.get_widget("gnome_radiobutton")
        self.kde_radiobutton = xml.get_widget("kde_radiobutton")
        self.startxonboot_checkbutton = xml.get_widget("startxonboot_checkbutton")
        self.firstboot_optionmenu = xml.get_widget("firstboot_optionmenu")
        self.driver_vbox = xml.get_widget("driver_vbox")
        self.monitor_vbox = xml.get_widget("monitor_vbox")
        self.driver_probe_check = xml.get_widget("driver_probe_check")
        self.monitor_probe_check = xml.get_widget("monitor_probe_check")
        
        self.driver_store = gtk.ListStore(gobject.TYPE_STRING)
        self.driver_view.set_model(self.driver_store)
        self.driver_col = gtk.TreeViewColumn("", gtk.CellRendererText(), text = 0)
        self.driver_view.append_column(self.driver_col)
        
        self.monitor_store = gtk.ListStore(gobject.TYPE_STRING)
        self.monitor_view.set_model(None)
        self.monitor_col = gtk.TreeViewColumn("", gtk.CellRendererText(), text = 0)
        self.monitor_view.append_column(self.monitor_col)

        self.config_x_button.connect("toggled", self.toggleXconfig)
        self.monitor_probe_check.connect("toggled", self.on_monitor_probe_check_toggled)
        self.driver_probe_check.connect("toggled", self.on_driver_probe_check_toggled)
        self.sync_button.connect("toggled", self.toggle_sync)

        self.fill_driver_list()
        self.fill_monitor_list()

        #add color depths
        color_depths = ["8", "16", "24", "32"]
        self.color_depth_combo.set_popdown_strings(color_depths)
        self.color_depth_combo.entry.set_editable(False)

        #add resolutions
        resolutions = ["640x480", "800x600", "1024x768", "1152x864", "1280x800",
                       "1280x1024", "1400x1050", "1600x1200", "1920x1440",
                       "2048x1536"]
        self.resolution_combo.set_popdown_strings(resolutions)
        self.resolution_combo.entry.set_editable(False)
        
        #add video card RAM sizes to option menu
        vram_list = ["256 KB", "512 KB", "1 MB", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB", "128 MB", "256 MB"]
        self.videoram_combo.set_popdown_strings(vram_list)
        self.videoram_combo.entry.set_editable(False)

        self.ramsize_dict = {"256 KB" : "256",
                             "512 KB" : "512",
                             "1 MB" : "1024",
                             "2 MB" : "2048",
                             "4 MB" : "4096",
                             "8 MB" : "8192",
                             "16 MB" : "16384",
                             "32 MB" : "32768",
                             "64 MB" : "65536",
                             "128 MB" : "131072",
                             "256 MB" : "262144"
                             }

    def fill_driver_list(self):
        #add video drivers to list
        try:
            driverFile = open("/usr/share/hwdata/videodrivers", "r")
        except:
            raise RuntimeError, (_("Could not read video driver database"))
            
        lines = driverFile.readlines ()
        driverFile.close ()
        lines.sort()
        for line in lines:
            line = string.strip (line)
	    name = line.split("\t", 2)[0]
	    iter = self.driver_store.append()
	    self.driver_store.set_value(iter, 0, name)

    def fill_monitor_list(self):
        try:
            from rhpxl.xhwstate import XF86HardwareState
        except ImportError:
            return

        hardware_state = XF86HardwareState(None)
        db = hardware_state.monitor.readMonitorsDB()

	l = db.keys()
	l.sort()
	mon_list = []
        
	#put Generic LCD and Generic CRT at the front of the list
        tmp = l[l.index("Generic LCD Display")]
        l.remove(l[l.index("Generic LCD Display")])
        l = [tmp] + l

        tmp = l[l.index("Generic CRT Display")]
        l.remove(l[l.index("Generic CRT Display")])
        l = [tmp] + l

        for manufacturer in l:
            for mon in db[manufacturer]:
                model = mon[0]

                if model not in mon_list:
                    mon_list.append(model)
                    iter = self.monitor_store.append()
                    self.monitor_store.set_value(iter, 0, model)

        # Don't set the model on the view until after we've done those
        # thousands of appends.
        self.monitor_view.set_model(self.monitor_store)

    def on_driver_probe_check_toggled(self, *args):
        self.driver_vbox.set_sensitive(not self.driver_probe_check.get_active())

    def on_monitor_probe_check_toggled(self, *args):
        self.monitor_vbox.set_sensitive(not self.monitor_probe_check.get_active())

    def toggleXconfig (self, args):
        #disable xconfig notebook
        self.xconfig_notebook.set_sensitive(self.config_x_button.get_active())

    def toggle_sync (self, args):
        sync_instead = self.sync_button.get_active()
        self.sync_table.set_sensitive(sync_instead)
        self.monitor_view.set_sensitive(not sync_instead)        

    def setSensitive(self, boolean):
        if boolean == False:
            self.xconfig_vbox.hide()
            self.xconfig_label_box.show()
        else:
            self.xconfig_vbox.show()
            self.xconfig_label_box.hide()

    def formToKickstart(self):
        if self.ks.upgrade.upgrade == True:
            self.ks.firstboot.firstboot = FIRSTBOOT_SKIP
            return

        if self.config_x_button.get_active():
            if self.firstboot_optionmenu.get_history() == 0:
                self.ks.firstboot.firstboot = FIRSTBOOT_SKIP
            elif self.firstboot_optionmenu.get_history() == 1:
                self.ks.firstboot.firstboot = FIRSTBOOT_DEFAULT
            elif self.firstboot_optionmenu.get_history() == 2:
                self.ks.firstboot.firstboot = FIRSTBOOT_RECONFIG

            self.ks.skipx.skipx = False

            #color depth - translate
            self.ks.xconfig.depth = int(self.color_depth_combo.entry.get_text())
            #resolution
            self.ks.xconfig.resolution = self.resolution_combo.entry.get_text()
            #default desktop
            if self.gnome_radiobutton.get_active():
                self.ks.xconfig.defaultdesktop = "GNOME"
            elif self.kde_radiobutton.get_active():
                self.ks.xconfig.defaultdesktop = "KDE"

            #startxonboot
            self.ks.xconfig.startX = self.startxonboot_checkbutton.get_active()

            if self.driver_probe_check.get_active():
                self.ks.xconfig.driver = ""
                self.ks.xconfig.wideoRam = ""
            else:
                #video card driver and monitor
                temp, iter = self.driver_view.get_selection().get_selected()
                driver = self.driver_store.get_value(iter, 0)
                self.ks.xconfig.driver = driver

                #translate MB to KB 
                self.ks.xconfig.videoRam = self.ramsize_dict [self.videoram_combo.entry.get_text()]

            if self.monitor_probe_check.get_active():
                self.ks.monitor = self.ks.Monitor()
            else:
                if self.sync_button.get_active():
                    self.ks.monitor.hsync = self.hsync_entry.get_text()
                    self.ks.monitor.vsync = self.vsync_entry.get_text()
                else:
                    temp, iter = self.monitor_view.get_selection().get_selected()
                    name = self.monitor_store.get_value(iter, 0)
                    self.ks.monitor.monitor = name
        else:
            self.ks.skipx(skipx=True)
            self.ks.monitor = self.ks.Monitor()
            self.ks.xconfig = self.ks.XConfig()

    def applyKickstart(self):
        if self.ks.skipx.skipx == True:
            self.config_x_button.set_active(False)
        else:
            self.config_x_button.set_active(True)

            if self.ks.firstboot.firstboot == FIRSTBOOT_DEFAULT:
                self.firstboot_optionmenu.set_history(1)
            elif self.ks.firstboot.firstboot == FIRSTBOOT_RECONFIG:
                self.firstboot_optionmenu.set_history(2)

            if self.ks.xconfig.startX == True:
                self.startxonboot_checkbutton.set_active(True)

            if self.ks.xconfig.defaultdesktop != "":
                if string.lower(self.ks.xconfig.defaultdesktop) == "gnome":
                    self.gnome_radiobutton.set_active(True)
                if string.lower(self.ks.xconfig.defaultdesktop) == "kde":
                    self.kde_radiobutton.set_active(True)

            if self.ks.xconfig.depth != 0:
                self.color_depth_combo.entry.set_text(str(self.ks.xconfig.depth))

            if self.ks.xconfig.resolution != "":
                self.resolution_combo.entry.set_text(string.strip(self.ks.xconfig.resolution))

            if self.ks.xconfig.driver != "":
                self.driver_probe_check.set_active(False)
                value = string.replace(self.ks.xconfig.driver, '"', '')

                iter = self.driver_store.get_iter_first()

                while iter:
                    if self.driver_store.get_value(iter, 0) == value:
                        path = self.driver_store.get_path(iter)
                        self.driver_view.set_cursor(path, self.driver_col, False)
                        self.driver_view.scroll_to_cell(path, self.driver_col, True, 0.5, 0.5)
                    iter = self.driver_store.iter_next(iter)

            if self.ks.xconfig.videoRam != "":
                for size in self.ramsize_dict.keys():
                    if int(self.ks.xconfig.videoRam) == int(self.ramsize_dict[size]):
                        self.videoram_combo.entry.set_text(size)                            

            if self.ks.monitor.monitor != "":
                self.monitor_probe_check.set_active(False)
                value = string.replace(self.ks.monitor.monitor, '"', '')

                iter = self.monitor_store.get_iter_first()

                while iter:
                    if self.monitor_store.get_value(iter, 0) == value:
                        path = self.monitor_store.get_path(iter)
                        self.monitor_view.set_cursor(path, self.monitor_col, False)
                        self.monitor_view.scroll_to_cell(path, self.monitor_col, True, 0.5, 0.5)
                    iter = self.monitor_store.iter_next(iter)

            if self.ks.monitor.hsync != "":
                self.sync_button.set_active(True)
                self.hsync_entry.set_text(string.strip(self.ks.monitor.hsync))
                self.monitor_probe_check.set_active(False)

            if self.ks.monitor.vsync != "":
                self.sync_button.set_active(True)
                self.vsync_entry.set_text(string.strip(self.ks.monitor.vsync))
                self.monitor_probe_check.set_active(False)
