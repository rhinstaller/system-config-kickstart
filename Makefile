PKGNAME=system-config-kickstart
VERSION=$(shell awk '/Version:/ { print $$2 }' ${PKGNAME}.spec)
RELEASE=$(shell awk '/Release:/ { print $$2 }' ${PKGNAME}.spec | sed -e 's|%.*$$||g')
TAG=r$(VERSION)-$(RELEASE)
SUBDIRS=man po

TX_PULL_ARGS = -a --disable-overwrite
TX_PUSH_ARGS = -s

PREFIX=/usr

MANDIR=${PREFIX}/share/man
DATADIR=${PREFIX}/share

PKGDATADIR=${DATADIR}/${PKGNAME}

po-pull:
	tx pull $(TX_PULL_ARGS)

tag:
	git tag -a -m "Tag as $(TAG)" -f $(TAG)
	@echo "Tagged as $(TAG)"

subdirs:
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE)) \
	|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"

install: ${PKGNAME}.desktop po-pull
	mkdir -p $(INSTROOT)$(PKGDATADIR)
	mkdir -p $(INSTROOT)/usr/bin
	mkdir -p $(INSTROOT)/usr/share/applications
	mkdir -p $(INSTROOT)/usr/share/icons/hicolor/48x48/apps
	install src/system-config-kickstart $(INSTROOT)/usr/bin
	install src/*.py $(INSTROOT)$(PKGDATADIR)
	for py in src/* ; do \
		sed -e s,@VERSION@,$(VERSION),g $${py} > $(INSTROOT)$(PKGDATADIR)/`basename $${py}` ; \
	done
	install src/${PKGNAME}.glade $(INSTROOT)$(PKGDATADIR)
	install pixmaps/${PKGNAME}.png $(INSTROOT)/usr/share/icons/hicolor/48x48/apps
	install ${PKGNAME}.desktop $(INSTROOT)/usr/share/applications/${PKGNAME}.desktop
	for d in $(SUBDIRS); do \
	(cd $$d; $(MAKE) INSTROOT=$(INSTROOT) MANDIR=$(MANDIR) install) \
		|| case "$(MFLAGS)" in *k*) fail=yes;; *) exit 1;; esac; \
	done && test -z "$$fail"
	git checkout -- po/$(PKGNAME).pot

archive: tag
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(TAG) | gzip -9c > $(PKGNAME)-$(VERSION).tar.gz
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

snapsrc: archive
	@rpmbuild -ta $(PKGNAME)-$(VERSION).tar.gz

local: po-pull
	@rm -rf ${PKGNAME}-$(VERSION).tar.gz
	@rm -rf /tmp/${PKGNAME}-$(VERSION) /tmp/${PKGNAME}
	@dir=$$PWD; cp -a $$dir /tmp/${PKGNAME}-$(VERSION)
	@dir=$$PWD; cd /tmp; tar --exclude=.git/* -czSpf $$dir/${PKGNAME}-$(VERSION).tar.gz ${PKGNAME}-$(VERSION)
	@rm -rf /tmp/${PKGNAME}-$(VERSION)	
	@echo "The archive is in ${PKGNAME}-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(TAG).. |sed -e 's/@.*)/)/'
	@echo

bumpver: po-pull
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 3` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1-2,4` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog system-config-kickstart.spec |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) system-config-kickstart.spec > speclog ; \
	(head -n $$cl system-config-kickstart.spec ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > system-config-kickstart.spec.new ; \
	mv system-config-kickstart.spec.new system-config-kickstart.spec ; rm -f speclog ; \
	sed -i "s/Version: $(VERSION)/Version: $$NEWVERSION/" system-config-kickstart.spec ; \
	@make -C po $(PKGNAME).pot-update ; \
	tx push $(TX_PUSH_ARGS)

clean:
	@rm -f *~
	@rm -f src/*~
	@rm -f src/*.pyc
	@rm -f ${PKGNAME}.desktop
	@rm -f ${PKGNAME}-$(VERSION).tar.gz

%.desktop: %.desktop.in
	@intltool-merge -d -u po/ $< $@
