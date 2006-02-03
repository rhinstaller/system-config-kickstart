#License: GPL
#Copyright Red Hat Inc.  Jan 2001

PKGNAME=system-config-kickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
CVSTAG=r$(subst .,-,$(VERSION))
SUBDIRS=man po

PREFIX=/usr

MANDIR=/usr/share/man
DATADIR=${PREFIX}/share

PKGDATADIR=${DATADIR}/${PKGNAME}

PAMD_DIR=/etc/pam.d
SECURITY_DIR=/etc/security/console.apps

default:

subdirs:
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE)) \
	|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

install: ${PKGNAME}.desktop
	mkdir -p $(INSTROOT)/$(PAMD_DIR)
	mkdir -p $(INSTROOT)/$(SECURITY_DIR)
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(PKGDATADIR)/pixmaps
	mkdir -p $(INSTROOT)/usr/bin
	mkdir -p $(INSTROOT)/usr/share/applications
	mkdir -p $(INSTROOT)/usr/share/icons/hicolor/48x48/apps
	ln -sf consolehelper $(INSTROOT)/usr/bin/$(PKGNAME)
	install $(PKGNAME).console $(INSTROOT)$(SECURITY_DIR)/$(PKGNAME)
	install $(PKGNAME).pam $(INSTROOT)$(PAMD_DIR)/$(PKGNAME)
	install src/*.py $(INSTROOT)$(PKGDATADIR)
	for py in src/*.py ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(INSTROOT)$(PKGDATADIR)/`basename $${py}` ; \
	done
	install src/${PKGNAME}.glade $(INSTROOT)$(PKGDATADIR)
	install pixmaps/*.png $(INSTROOT)$(PKGDATADIR)/pixmaps
	install pixmaps/${PKGNAME}.png $(INSTROOT)/usr/share/icons/hicolor/48x48/apps
	install ${PKGNAME}.desktop $(INSTROOT)/usr/share/applications/${PKGNAME}.desktop
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) INSTROOT=$(INSTROOT) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

archive:
	cvs tag -F $(CVSTAG) .
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@cvsroot=`cat CVS/Root` 2>/dev/null; \
	cd /tmp; cvs -d$$cvsroot export -r$(CVSTAG) ${PKGNAME}; exit
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

snapsrc: archive
	@rpmbuild -ta $(PKGNAME)-$(VERSION).tar.bz2

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.bz2
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cd /tmp; cp -a $$dir ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

clean:
	@rm -f *~
	@rm -f src/*~
	@rm -f src/*.pyc
	@rm -f ${PKGNAME}.desktop

%.desktop: %.desktop.in
	@intltool-merge -d -u po/ $< $@
