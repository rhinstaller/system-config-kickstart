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

class packages:
    
    def __init__(self, xml):
        print "here"
        hdlist = rpm.readHeaderListFromFile("hdlist")
        noscore = 0
        
#        print hdlist
        self.hdlist = hdlist
	self.packages = {}
	newCompat = []
## 	for h in hdlist:
## 	    name = h[rpm.RPMTAG_NAME]
##             print name

##             if noscore:
##                 self.packages[name] = Package(h)
##                 continue
##             score1 = rpm.archscore(h['arch'])
##             if (score1):
##                 if self.packages.has_key(name):
##                     score2 = rpm.archscore(self.packages[name].h['arch'])
##                     if (score1 < score2):
##                         newCompat.append(self.packages[name])
##                         self.packages[name] = Package(h)
##                     else:
##                         newCompat.append(Package(h))
##                 else:
##                     self.packages[name] = Package(h)
