
MANDIR=/usr/share/man

all:

install:
	mkdir -p $(INSTROOT)$(MANDIR)/man8
	install -m 644 en/ksconfig.8 $(INSTROOT)$(MANDIR)/man8
	for d in $(shell ls | grep -v en | grep -v Makefile |grep -v CVS); do \
	        mkdir -p  $(INSTROOT)$(MANDIR)/$$d/man8 ; \
		install -m 644 $$d/ksconfig.8 $(INSTROOT)$(MANDIR)/$$d/man8 ; \
	done

clean:
