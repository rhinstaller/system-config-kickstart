#License: GPL
#Copyright Red Hat Inc.  Jan 2001

default: install

install:
	mkdir -p $(RPM_BUILD_ROOT)/usr/sbin
	install ksconfig.py $(RPM_BUILD_ROOT)/usr/sbin

