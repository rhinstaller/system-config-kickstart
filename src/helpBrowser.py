#!/usr/bin/python2.2

## helpBrowser - a dirty little hack to find a decent way to display help since the
## GTK2 help browser isn't ready
## Copyright (C) 2002 Red Hat, Inc.
## Copyright (C) 2002 Brent Fox <bfox@redhat.com>

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

## Author: Brent Fox

import os

def find_browser():
    try:
        path = '/usr/bin/mozilla'
        os.stat(path)
        return path
    except:
        try:
            path = '/usr/bin/galeon'
            os.stat(path)
            return path
        except:
            try:
                path = '/usr/bin/konqueror'
                os.stat(path)
                return path
            except:
                return None
        
