#
# Chris Lumens <clumens@redhat.com>
# Brent Fox <bfox@redhat.com>
# Tammy Fox <tfox@redhat.com>
#
# Copyright (C) 2000-2007 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2 or, at your option, any later version.  This
# program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc. 

class partEntry:
    def __init__(self):
        self.mountPoint = ""
        self.fsType = ""
        self.size = 0
        self.fixedSize = ""
        self.setSize = ""
        self.setSizeVal = ""
        self.sizeStrategy = "fixed"
        self.maxSize = ""
        self.asPrimary = 0
        self.device = None
        self.partition = None
#        self.onDisk = ""
#        self.onDiskVal = ""
#        self.onPart = ""
#        self.onPartVal = ""
        self.doFormat = ""
        self.raidLevel = ""
        self.raidSpares = ""
        self.raidNumber = ""
        self.raidPartitions = []
        self.raidPartitionObjects = []
        self.raidDevice = ""
        self.isRaidDevice = None
