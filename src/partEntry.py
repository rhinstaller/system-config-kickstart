#!/usr/bin/python2.2

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

#Kickstart Configurator Partitions Data Structure

class partEntry:
    def __init__(self):
        self.mountPoint = ""
        self.fsType = ""
        self.size = 0
        self.fixedSize = ""
        self.setSize = ""
        self.setSizeVal = ""
        self.sizeStrategy = ""
        self.maxSize = ""
        self.asPrimary = ""
        self.onDisk = ""
        self.onDiskVal = ""
        self.onPart = ""
        self.onPartVal = ""
        self.doFormat = ""
        self.raidType = ""
        self.raidSpares = ""
        self.raidNumber = ""
        self.isRaidDevice = ""
