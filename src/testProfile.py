#!/usr/bin/python

import kickstartData
import profileSystem

data = kickstartData.KickstartData()
profileSystem = profileSystem.ProfileSystem(data)
#profileSystem(data)
data.getAll()
