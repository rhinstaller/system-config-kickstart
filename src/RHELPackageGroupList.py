#!/usr/bin/python2

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)


desktopsList = [_("X Window System"),
               _("GNOME Desktop Environment"),
               _("KDE Desktop Environment")
                ]
applicationsList = [_("Editors"),
                    _("Engineering and Scientific"),
                    _("Graphical Internet"),
                    _("Text-based Internet"),
                    _("Office/Productivity"),
                    _("Sound and Video"),
                    _("Graphics"),
                    _("Games and Entertainment"),
                    _("Authoring and Publishing")
                    ]
serversList = [_("Server Configuration Tools (AS and ES only)"),
               _("Web Server"),
               _("Mail Server"),
               _("Windows File Server"),
               _("DNS Name Server"), 
               _("FTP Server"),
               _("SQL Database Server"),
               _("News Server"),
               _("Network Servers (AS and ES only)")
               ]
developmentList = [_("Development Tools"),
                   _("Kernel Development"),
                   _("X Software Development"),
                   _("GNOME Software Development"),
                   _("KDE Software Development")
                   ]
systemList = [_("Administration Tools"),
              _("System Tools"),
              _("Printing Support")
              ]
