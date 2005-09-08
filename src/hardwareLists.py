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
