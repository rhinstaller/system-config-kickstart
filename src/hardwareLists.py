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

import string

#pull list of language from system-config-languages
langDict = {}

lines = open("/usr/share/system-config-language/locale-list", "r").readlines()

for line in lines:
    tokens = string.split(line)

    if '.' in tokens[0]:
        #Chop encoding off so we can compare to self.installedLangs
        langBase = string.split(tokens[0], '.')
        langBase = langBase[0]
    elif '@' in tokens[0]:
        langBase = string.split(tokens[0], '@')
        langBase = langBase[0]
    else:
        langBase = tokens[0]

    name = ""
    for token in tokens[3:]:
        name = name + " " + token

    name = string.strip(name)
    langDict[name] = langBase
