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


#define mice, add mice here
mouseDict = { "No Mouse" : "none",
                   "ALPS GlidePoint (PS/2)" : "alpsps/2",
                   "ASCII MieMouse (serial)" : "ascii",
                   "ASCII MieMouse (PS/2)" : "asciips/2",
                   "ATI Bus Mouse" : "atibm",
                   "Generic Mouse (serial)" : "generic",
                   "Generic 3 Button Mouse (serial)" : "generic3",
                   "Generic Mouse (PS/2)" : "genericps/2",
                   "Generic 3 Button Mouse (PS/2)" : "generic3ps/2",
                   "Generic Mouse (USB)" : "genericusb",
                   "Generic 3 Button Mouse (USB)" : "generic3usb",
                   "Genius NetMouse (serial)" : "geniusnm",
                   "Genius NetMouse (PS/2)" : "geniusnmps/2",
                   "Genius NetMouse Pro (PS/2)" : "geniusprops/2",
                   "Genius NetScroll (PS/2)" : "geniusscrollps/2",
                   "Kensington Thinking Mouse (serial)" : "thinking",
                   "Kensington Thinking Mouse (PS/2)" : "thinkingps/2",
                   "Logitech Mouse (serial, old C7 type)" : "logitech",
                   "Logitech CC Series (serial)" : "logitechcc",
                   "Logitech Bus Mouse" : "logibm",
                   "Logitech MouseMan/FirstMouse (serial)" : "logimman",
                   "Logitech MouseMan/FirstMouse (PS/2)" : "logimmanps/2",
                   "Logitech MouseMan+/FirstMouse+ (serial)" : "logimman+",
                   "Logitech MouseMan+/FirstMouse+ (PS/2)" : "logimman+ps/2",
                   "Logitech MouseMan Wheel (USB)" : "logimmusb",
                   "Microsoft compatible (serial)" : "microsoft",
                   "Microsoft Rev 2.1A or higher (serial)" : "msnew",
                   "Microsoft IntelliMouse (serial)" : "msintelli",
                   "Microsoft IntelliMouse (PS/2)" : "msintellips/2",
                   "Microsoft IntelliMouse (USB)" : "msintelliusb",
                   "Microsoft Bus Mouse" : "msbm",
                   "Mouse Systems (serial)" : "mousesystems",
                   "MM Series (serial)" : "mmseries",
                   "MM HitTablet (serial)" : "mmhittab",
                   "Sun Mouse" : "sun",
                   }
