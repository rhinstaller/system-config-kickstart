#!/usr/bin/python2

## Kickstart Configurator - A graphical kickstart file generator
## Copyright (C) 2000, 2001, 2002, 2003 Red Hat, Inc.
## Copyright (C) 2000, 2001, 2002, 2003  Brent Fox <bfox@redhat.com>
##                                       Tammy Fox <tfox@redhat.com>

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

import sys
import signal
import getopt
import os

if __name__ == "__main__":
    signal.signal (signal.SIGINT, signal.SIG_DFL)

##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)

# FIXME
def useCliMode(value):
    import kickstartData
    import profileSystem
    data = kickstartData.KickstartData()
    profileSystem = profileSystem.ProfileSystem(data)
    file = data.getAll()
    fd = open(value, "w")

    for line in file:
        fd.write(line + "\n")

    fd.close()

    
file = None
opts, file = getopt.getopt(sys.argv[1:], "g:h", ["generate=", "help"])
    
for (opt, value) in opts:
    if opt == "--generate" or opt == "-g":
        useCliMode(value)
        sys.exit(1)
    if opt == "--help" or opt == "-h":
        print _("""Usage: system-config-kickstart [--help] [--generate <filename>] [<kickstart_filename>]
        
--help                  Print out this message
--generate <filename>   Generate a kickstart file from the current machine and write
                        it to <filename>.  This option runs on the console, so it is
                        useful for servers that do not have X currently running.
<kickstart_filename>    This option will cause the GUI to launch with the values from
                        the kickstart file already filled in.""")
        sys.exit(1)


if file:
    file = file[0]

try:
    import kickstartGui
except:
    print (_("Could not open display because no X server is running."))
    print (_("Try running 'system-config-kickstart --help' for a list of options."))
    sys.exit(0)

kickstartGui.kickstartGui(file)
