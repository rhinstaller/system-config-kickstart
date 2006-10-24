#License: GPL
#Copyright Red Hat Inc.  Jan 2001

PKGNAME=system-config-kickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
CVSTAG=r$(subst .,_,$(VERSION)-$(RELEASE))
SUBDIRS=man po

PREFIX=/usr

MANDIR=${PREFIX}/share/man
DATADIR=${PREFIX}/share

PKGDATADIR=${DATADIR}/${PKGNAME}

default: subdirs

tag:
	cvs tag -FR $(CVSTAG)

subdirs:
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE)) \
	|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

install: ${PKGNAME}.desktop
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)$(PKGDATADIR)/pixmaps
	mkdir -p $(INSTROOT)/usr/bin
	mkdir -p $(INSTROOT)/usr/share/applications
	mkdir -p $(INSTROOT)/usr/share/icons/hicolor/48x48/apps
	install src/system-config-kickstart $(INSTROOT)/usr/bin
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

archive: tag
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@CVSROOT=`cat CVS/Root`; cd /tmp; cvs -d $$CVSROOT export -r$(CVSTAG) ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar -czSpf $$dir/${PKGNAME}-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

snapsrc: archive
	@rpmbuild -ta $(PKGNAME)-$(VERSION).tar.bz2

local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.gz
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cp -a $$dir /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar -czSpf $$dir/${PKGNAME}-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

clean:
	@rm -f *~
	@rm -f src/*~
	@rm -f src/*.pyc
	@rm -f ${PKGNAME}.desktop
	@rm -f ${PKGNAME}-$(VERSION).tar.gz

%.desktop: %.desktop.in
	@intltool-merge -d -u po/ $< $@
