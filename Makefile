#License: GPL
#Copyright Red Hat Inc.  Jan 2001

PKGNAME=redhat-config-kickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
CVSTAG=r$(subst .,-,$(VERSION))
SUBDIRS=man po

PREFIX=/usr

MANDIR=/usr/share/man
DATADIR=${PREFIX}/share

PKGDATADIR=${DATADIR}/${PKGNAME}

default:

subdirs:
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE)) \
	|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

install:
	mkdir -p $(INSTROOT)/usr/sbin
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)/usr/share/applications
	install ${PKGNAME} $(INSTROOT)/usr/sbin/${PKGNAME}
	install src/*.py $(INSTROOT)$(PKGDATADIR)
	for py in src/*.py ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(INSTROOT)$(PKGDATADIR)/`basename $${py}` ; \
	done
	install src/${PKGNAME}-gtk2.glade $(INSTROOT)$(PKGDATADIR)
	install pixmaps/*.png $(INSTROOT)$(PKGDATADIR)/pixmaps
	install ${PKGNAME}.desktop $(INSTROOT)/usr/share/applications/${PKGNAME}.desktop
	ln -sf /usr/sbin/${PKGNAME} $(INSTROOT)/usr/sbin/ksconfig
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) INSTROOT=$(INSTROOT) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

archive:
	cvs tag -F $(CVSTAG) .
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@cd /tmp; cvs export -r$(CVSTAG) ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

snapsrc: create-snapshot
	@rpmbuild -ta --nodeps $(PKGNAME)-$(VERSION).tar.bz2

create-snapshot:
	@rm -rf /tmp/$(PKGNAME)
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@tag=`cvs status Makefile | awk ' /Sticky Tag/ { print $$3 } '` 2> /dev/null; \
        [ x"$$tag" = x"(none)" ] && tag=HEAD; \
        echo "*** Pulling off $$tag!"; \
        cd /tmp ; cvs -Q -d $(CVSROOT) export -r $$tag $(PKGNAME) || echo "Um... export aborted."
	@mv /tmp/$(PKGNAME) /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp ; tar --bzip2 -cSpf $(PKGNAME)-$(VERSION).tar.bz2 $(PKGNAME)-$(VERSION)
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@cp /tmp/$(PKGNAME)-$(VERSION).tar.bz2 .
	@rm -f /tmp/$(PKGNAME)-$(VERSION).tar.bz2
	@echo ""
	@echo "The final archive is in $(PKGNAME)-$(VERSION).tar.bz2"


local:
	@rm -rf ${PKGNAME}-$(VERSION).tar.bz2
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@cd /tmp; cp -a ~/redhat/${PKGNAME} ${PKGNAME}
	@mv /tmp/${PKGNAME} /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --bzip2 -cSpf $$dir/${PKGNAME}-$(VERSION).tar.bz2 ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.bz2"

clean:
	@rm -f *~
	@rm -f src/*~
	@rm -f src/*.pyc
