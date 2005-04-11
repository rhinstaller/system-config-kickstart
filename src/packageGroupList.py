##
## I18N
## 
from rhpl.translate import _, N_
import rhpl.translate as translate
domain = 'system-config-kickstart'
translate.textdomain (domain)
import rhpl.comps
import os
import string
import sys

compsPath = "/usr/share/comps/" + rhpl.getArch() + "/comps.xml"

try:
    comps_file = rhpl.comps.Comps(compsPath)
except:
    print (_("Could not start because there is no %s file." % compsPath))
    print(_("Please make sure the comps package is installed."))
    sys.exit(0)

desktopsList = []
applicationsList = []
serversList = []
developmentList = []
systemList = []

# Converts a single language into a "language search path". For example,
# fr_FR.utf8@euro would become "fr_FR.utf8@eueo fr_FR.utf8 fr_FR fr"
def expandLangs(str):
    langs = [str]
    # remove charset ...
    if '.' in str:
        langs.append(string.split(str, '.')[0])

    if '@' in str:
        langs.append(string.split(str, '@')[0])

    # also add 2 character language code ...
    if len(str) > 2:
        langs.append(str[:2])

    return langs

def do_translate (id):
    if os.environ.has_key("LANG"):
        langs = expandLangs(os.environ["LANG"])
    else:
        langs = []

    for lang in langs:
        if id.translated_name.has_key(lang):
            return id.translated_name[lang]

    return id.name

for subgroup in comps_file.hierarchy['Desktops']:
    id = comps_file.getGroupById(subgroup)
    if id != None:
        desktopsList.append ((do_translate(id), subgroup))

for subgroup in comps_file.hierarchy['Applications']:
    id = comps_file.getGroupById(subgroup)
    if id != None:
        applicationsList.append ((do_translate(id), subgroup))

for subgroup in comps_file.hierarchy['Servers']:
    id = comps_file.getGroupById(subgroup)
    if id != None:
        serversList.append ((do_translate(id), subgroup))

for subgroup in comps_file.hierarchy['Development']:
    id = comps_file.getGroupById(subgroup)
    if id != None:
        developmentList.append ((do_translate(id), subgroup))

for subgroup in comps_file.hierarchy['System']:
    id = comps_file.getGroupById(subgroup)
    if id != None:
        systemList.append ((do_translate(id), subgroup))
