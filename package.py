#!/usr/bin/env python

#Kickstart Configurator Package Options
#Copyright Red Hat, Inc. 2001
#Written by Brent Fox (bfox@redhat.com) and Tammy Fox (tfox@redhat.com)
#Created February, 2000 Brent Fox
#Last Modified: February 6, 2001 Brent Fox

from gtk import *
import GtkExtra
import GdkImlib
from gnome.ui import *


class packageWindow(GtkWindow):
    def okClicked(self, args):        
        self.data = "%packages \n"
#        print self.getData()
        boxes = self.pkgVBox.children()

        for box in boxes:
            checkbox = box.children()
#            print checkbox
            checkbox = checkbox[0]

            hbox = checkbox.children()
            hbox = hbox[0]
            data = hbox.children()
            label = data[1]
            package = label.get()
#            print data

            if checkbox.get_active():
#                print "active"
#                print package
                self.data = self.data + "@" + package + "\n"
            else:
#                print "inactive"
                pass

#        print self.data
        self.destroy()

    def cancelClicked(self, args):
        self.destroy()

    def getData(self):
	return self.data

#    def itemToggled(self, widget, item):
#        if widget.get_active():
#            print "activate"
#        else:
#            print "deactivate"

    def __init__(self, quit_cb=None):
        GtkWindow.__init__(self, WINDOW_TOPLEVEL)
        self.set_modal(TRUE)
        self.set_border_width(6)
        self.set_default_size(400, 550)		
        self.set_title("Package Group Selection")

        self.vbox = GtkVBox()
        self.add(self.vbox)

        frame3 = GtkFrame("Package Group Selection")
        self.vbox.pack_start(frame3)

        self.pkgVBox = GtkVBox()
#        frame3.add(partVbox)

        sw = GtkScrolledWindow ()
        frame3.add(sw)
        sw.set_policy (POLICY_AUTOMATIC, POLICY_AUTOMATIC)


        package_list = { "Printer Support": "printer-support.png", "X Window System": "x-window-system.png",
                         "GNOME" :"gnome.png", "KDE":"kde.png", "Mail/WWW/News Tools":"mail-www-news-tools.png",
                         "DOS/Windows Connectivity":"dos-windows-connectivity.png",
                         "Graphics Manipulation":"graphics-manipulation.png", "Games":"games.png",
                         "Multimedia Support": "multimedia-support.png", "Laptop Support": "laptop-support.png",
                         "Networked Workstation": "networked-workstation.png",
                         "Dialup Workstation":"dialup-workstation.png",
                         "News Server":"news-server.png", "NFS Server":"nfs-server.png",
                         "SMB (Samba) Server":"smb--samba--server.png",
                         "IPX/Netware(tm) Connectivity": "ipx-netware-tm--connectivity.png",
                         "Anonymous FTP Server":"anonymous-ftp-server.png", "Web Server":"web-server.png",
                         "DNS Name Server":"dns-name-server.png", "SQL Server":"sql-server.png",
                         "Network Management Workstation":"network-management-workstation.png",
                         "Authoring/Publishing":"authoring-publishing.png",
                         "Emacs":"emacs.png", "Development":"development.png",
                         "Kernel Development":"kernel-development.png", "Utilities":"utilities.png",
                         "Everything":"everything.png"
                         }

        pkgs =  package_list.keys()
        pkgs.sort()

        for pkg in pkgs:

            hbox = GtkHBox (FALSE, 5)


            label = GtkLabel (pkg)
            label.set_alignment (0.0, 0.5)

#            print package_list[pkg]
            pixname = "/usr/share/anaconda/pixmaps/" + package_list[pkg]
#            print pixname

            im = GdkImlib.Image (pixname)
#            im = self.ics.readPixmap (pixname)
            if im:
                im.render ()
                pix = im.make_pixmap ()
                checkbox = GtkCheckButton()
#                checkbox.connect('toggled', self.itemToggled, pkg)
                hb = GtkHBox()
                hb.pack_start (pix, FALSE, FALSE, 0)
                hb.pack_start (label, TRUE, TRUE, 0)
                checkbox.add(hb)
                hbox.pack_start (checkbox, TRUE)

            else:
                pass

            self.pkgVBox.pack_start (hbox)

        sw.add_with_viewport(self.pkgVBox)

        #----------Ok and Cancel Buttons for Authenication window--------#
        self.hbox2 = GtkHBox()
        self.vbox.pack_start(self.hbox2, FALSE)

        self.okButton = GtkButton("Ok")
        self.okButton.connect("clicked", self.okClicked)
        self.hbox2.pack_start(self.okButton)

        self.cancelButton = GtkButton("Cancel")
        self.cancelButton.connect("clicked", self.cancelClicked)
        self.hbox2.pack_start(self.cancelButton)



        self.show_all()
