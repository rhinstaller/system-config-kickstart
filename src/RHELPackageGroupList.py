#!/usr/bin/python2

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)


desktopsList = [N_("X Window System"),
               N_("GNOME Desktop Environment"),
               N_("KDE (K Desktop Environment)")
                ]
applicationsList = [N_("Editors"),
                    N_("Engineering and Scientific"),
                    N_("Graphical Internet"),
                    N_("Text-based Internet"),
                    N_("Office/Productivity"),
                    N_("Sound and Video"),
                    N_("Graphics"),
                    N_("Games and Entertainment"),
                    N_("Authoring and Publishing")
                    ]
serversList = [N_("Server Configuration Tools (AS and ES only)"),
               N_("Web Server"),
               N_("Mail Server"),
               N_("Windows File Server"),
               N_("DNS Name Server"), 
               N_("FTP Server"),
               N_("SQL Database Server"),
               N_("News Server"),
               N_("Network Servers (AS and ES only)")
               ]
developmentList = [N_("Development Tools"),
                   N_("Kernel Development"),
                   N_("X Software Development"),
                   N_("GNOME Software Development"),
                   N_("KDE Software Development")
                   ]
systemList = [N_("Administration Tools"),
              N_("System Tools"),
              N_("Printing Support")
              ]
