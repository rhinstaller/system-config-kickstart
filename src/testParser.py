#!/usr/bin/python

import kickstartData
import kickstartParser

data = kickstartData.KickstartData()
kickstartParser.KickstartParser(data, "ks.cfg")
data.getAll()
