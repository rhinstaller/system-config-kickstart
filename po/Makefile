#
# Makefile for the PO files (translation) catalog
#
# $Id$

TOP	 = ../..

# What is this package?
NLSPACKAGE	= ksconfig
POTFILE		= $(NLSPACKAGE).pot

# destination directory
INSTALL_NLS_DIR = $(RPM_BUILD_ROOT)/usr/share/locale

# PO catalog handling
MSGMERGE	= OLD_PO_FILE_INPUT=yes msgmerge -v
PYGETTEXT	= ./pygettext.py --default-domain=$(NLSPACKAGE) \
		  --verbose --output-file=$(NLSPACKAGE).po 
XGETTEXT	= xgettext --default-domain=$(NLSPACKAGE) \
		  --add-comments		  
MSGFMT		= OLD_PO_FILE_INPUT=yes msgfmt --statistics --verbose

# What do we need to do
POFILES		= $(wildcard *.po)
MOFILES		= $(patsubst %.po,%.mo,$(POFILES))
PYSRC		= $(wildcard ../src/*.py)
SRCFILES	= $(PYSRC) ksconfig.gladestrings
#SRCFILES	= $(PYSRC) configdlg.gladestrings gui.gladestrings \
#	progress.gladestrings advisorywin.gladestrings

all::  update-po $(MOFILES)

$(POTFILE): $(SRCFILES)
	@$(PYGETTEXT) --keyword=_ --keyword=N_ $(PYSRC)
	@if cmp -s $(NLSPACKAGE).po $(POTFILE); then \
	    rm -f $(NLSPACKAGE).po; \
	else \
	    mv -f $(NLSPACKAGE).po $(POTFILE); \
	fi; \
	$(XGETTEXT) --keyword=N_ ksconfig.gladestrings; \
	msghack --append $(NLSPACKAGE).po $(POTFILE) -o $(POTFILE)-; \
	mv -f $(POTFILE)- $(POTFILE); \
	rm -f $(NLSPACKAGE).po
#	$(XGETTEXT) --keyword=N_ gui.gladestrings; \
#	msghack --append $(NLSPACKAGE).po $(POTFILE) -o $(POTFILE)-; \
#	mv -f $(POTFILE)- $(POTFILE); \
#	rm -f $(NLSPACKAGE).po
#	$(XGETTEXT) --keyword=N_ progress.gladestrings; \
#	msghack --append $(NLSPACKAGE).po $(POTFILE) -o $(POTFILE)-; \
#	mv -f $(POTFILE)- $(POTFILE); \
#	rm -f $(NLSPACKAGE).po

update-po: Makefile $(POTFILE) refresh-po

refresh-po: Makefile
	for cat in $(POFILES); do \
		lang=`basename $$cat .po`; \
		if $(MSGMERGE) $$lang.po $(POTFILE) > $$lang.pot ; then \
			mv -f $$lang.pot $$lang.po ; \
			echo "$(MSGMERGE) of $$lang succeeded" ; \
		else \
			echo "$(MSGMERGE) of $$lang failed" ; \
			rm -f $$lang.pot ; \
		fi \
	done

clean:
	@rm -fv *mo *~ .depend

install: $(MOFILES)
	@for n in $(MOFILES); do \
	    l=`basename $$n .mo`; \
	    $(INSTALL_DIR) $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES; \
	    $(INSTALL_DATA) --verbose $$n $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES/$(NLSPACKAGE).mo; \
	done

%.mo: %.po
	$(MSGFMT) -o $@ $<

.PHONY: missing depend

