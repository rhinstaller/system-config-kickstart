#License: GPL
#Copyright Red Hat Inc.  Jan 2001

VERSION=$(shell awk '/Version:/ { print $$2 }' ksconfig.spec)
CVSTAG=r$(subst .,-,$(VERSION))
SUBDIRS=man po

PREFIX=/usr

MANDIR=/usr/share/man
DATADIR=${PREFIX}/share

PKGDATADIR=${DATADIR}/ksconfig
DESKTOPDIR=/etc/X11/applnk/System

default:

subdirs:
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE)) \
	|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

install:
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(DESKTOPDIR)
	install ksconfig $(INSTROOT)/usr/sbin/ksconfig
	install src/*.py $(INSTROOT)$(PKGDATADIR)
	for py in src/*.py ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(INSTROOT)$(PKGDATADIR)/`basename $${py}` ; \
	done
	install src/ksconfig.glade $(INSTROOT)$(PKGDATADIR)
	install src/Cards $(INSTROOT)$(PKGDATADIR)
	install src/MonitorsDB $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(DESKTOPDIR)
	install -m 644 ksconfig.desktop $(INSTROOT)$(DESKTOPDIR)
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) INSTROOT=$(INSTROOT) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

archive:
	cvs tag -F $(CVSTAG) .
	@rm -rf /tmp/ksconfig-$(VERSION) /tmp/ksconfig
	@cd /tmp; cvs export -r$(CVSTAG) ksconfig
	@mv /tmp/ksconfig /tmp/ksconfig-$(VERSION)
	@dir=$$PWD; cd /tmp; tar cvzf $$dir/ksconfig-$(VERSION).tar.gz ksconfig-$(VERSION)
	@rm -rf /tmp/ksconfig-$(VERSION)
	@echo "The archive is in ksconfig-$(VERSION).tar.gz"

clean:
	@rm -f *~
	@rm -f *.pyc
