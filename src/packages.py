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
import comps

CHECK_CHAIN	= 0
FORCE_SELECT	= 1
FORCE_UNSELECT	= 2

class Package:
    def __getitem__(self, item):
	return self.h[item]

    def __repr__(self):
	return "%s" % self.name

    def select(self):
	self.state = FORCE_SELECT
	self.selected = 1

    def unselect(self):
	self.state = FORCE_UNSELECT
	self.selected = 0

    def isSelected(self):
	return self.selected

    def updateSelectionCache(self):
	if self.state == FORCE_SELECT or self.state == FORCE_UNSELECT:
	    return

	self.selected = 0
	for chain in self.chains:
	    on = 1
	    for comp in chain:
		if not comp.isSelected(justManual = 0):
		    on = 0
                else:
                    if comp.pkgDict[self] != None:
                        on = 0
                        for expr in comp.pkgDict[self]:
                            if comp.set.exprMatch (expr):
                                on = 1
	    if on: 
		self.selected = 1

    def getState(self):
	return (self.state, self.selected)

    def setState(self, state):
	(self.state, self.selected) = state

    def addSelectionChain(self, chain):
	self.chains.append(chain)

    def __init__(self, header):
	self.h = header
	self.chains = []
	self.selected = 0
	self.state = CHECK_CHAIN
	self.name = header[rpm.RPMTAG_NAME]
	self.size = header[rpm.RPMTAG_SIZE]




class headerList:

    def keys(self):
        return self.packages.keys()
    
    def __init__(self, xml):
        print "here"
        hdlist = rpm.readHeaderListFromFile("hdlist")
        noscore = 0
        
#        print hdlist
        self.hdlist = hdlist
	self.packages = {}
	newCompat = []
 	for h in hdlist:
 	    name = h[rpm.RPMTAG_NAME]

            self.packages[name] = Package(h)
#            print self.packages[name]

            score1 = rpm.archscore(h['arch'])
            if (score1):
		if self.packages.has_key(name):
		    score2 = rpm.archscore(self.packages[name].h['arch'])
		    if (score1 < score2):
			newCompat.append(self.packages[name])
			self.packages[name] = Package(h)
		    else:
			newCompat.append(Package(h))
		else:
		    self.packages[name] = Package(h)                
        print self.packages
