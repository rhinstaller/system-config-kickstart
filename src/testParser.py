#!/usr/bin/python2

import kickstartData
import kickstartParser

data = kickstartData.KickstartData()
kickstartParser.KickstartParser(data, "ks.cfg")
data.printData()
