#!/usr/bin/python2

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)


desktopsList = [[N_("X Window System"), "base-x"],
                [N_("GNOME Desktop Environment"), "gnome-desktop"],
                [N_("KDE (K Desktop Environment)"), "kde-desktop"]
                ]
applicationsList = [[N_("Editors"), "editors"],
                    [N_("Engineering and Scientific"), "engineering-and-scientific"],
                    [N_("Graphical Internet"), "graphical-internet"],
                    [N_("Text-based Internet"), "text-internet"],
                    [N_("Office/Productivity"), "office"],
                    [N_("Sound and Video"), "sound-and-video"],
                    [N_("Graphics"), "graphics"],
                    [N_("Games and Entertainment"), "games"],
                    [N_("Authoring and Publishing"), "authoring-and-publishing"]
                    ]
serversList = [[N_("Server Configuration Tools (AS and ES only)"), "server-cfg"],
               [N_("Web Server"), "web-server"],
               [N_("Mail Server"), "mail-server"],
               [N_("Windows File Server"), "smb-server"],
               [N_("DNS Name Server"), "dns-server"],
               [N_("FTP Server"), "ftp-server"],
               [N_("SQL Database Server"), "sql-server"],
               [N_("News Server"), "news-server"],
               [N_("Network Servers (AS and ES only)"), "network-server"]
               ]
developmentList = [[N_("Development Tools"), "development-tools"],
                   [N_("Kernel Development"), "kernel-development"], 
                   [N_("X Software Development"), "x-software-development"],
                   [N_("GNOME Software Development"), "gnome-software-development"],
                   [N_("KDE Software Development"), "kde-software-development"]
                   ]
systemList = [[N_("Administration Tools"), "admin-tools"],
              [N_("System Tools"), "system-tools"],
              [N_("Printing Support"), "printing"]
              ]
