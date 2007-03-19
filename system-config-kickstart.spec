Summary: A graphical interface for making kickstart files.
Name: system-config-kickstart
Version: 2.7.4
Release: 1%{?dist}
URL: http://fedora.redhat.com/projects/config-tools/
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Source0: %{name}-%{version}.tar.gz
Obsoletes: ksconfig
Obsoletes: redhat-config-kickstart
BuildRequires: desktop-file-utils
BuildRequires: intltool gettext
Requires: pygtk2 >= 1.99.11
Requires: pygtk2-libglade 
Requires: python >= 2.3.3
Requires: hwdata
Requires: rhpl
Requires: system-config-language
Requires: system-config-securitylevel
Requires: pykickstart >= 0.96
Requires: yum
Requires: pirut
Requires: hicolor-icon-theme
Requires(post): gtk2 >= 2.6
Requires(postun): gtk2 >= 2.6

%description
Kickstart Configurator is a graphical tool for creating kickstart files.  

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor system --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-category Application \
  --add-category System \
  --add-category X-Red-Hat-Base          \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%preun
if [ -d /usr/share/%{name} ] ; then
  rm -rf /usr/share/%{name}/*.pyc
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc doc/*
/usr/bin/%{name}
%dir /usr/share/%{name}
/usr/share/%{name}/*
%{_mandir}/man8/%{name}*
%lang(ja) %{_mandir}/ja/man8/%{name}*
%attr(0644,root,root) %{_datadir}/applications/%{name}.desktop
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/system-config-kickstart.png

%changelog
* Mon Mar 19 2007 Chris Lumens <clumens@redhat.com> 2.7.4-1
- Fix loading packages section (#232285).
- Fix preview/save on upgrade (#232282).
- Add UI for authconfig's --ldaploadcert option (#232664).

* Wed Feb 28 2007 Chris Lumens <clumens@redhat.com> 2.7.3-1
- Updated for the newer pykickstart interface.

* Wed Feb 07 2007 Chris Lumens <clumens@redhat.com> 2.7.2-1
- Add package-level selection and removal (#222592).
- Add UI for the key command (#226718).
- Fix iter handling on the partition screen for auto partitions (#225087).

* Tue Jan 16 2007 Chris Lumens <clumens@redhat.com> 2.7.1-1
- Update to use new pykickstart.
- Don't traceback if no monitor or x driver is selected.
- Handle pykickstart exceptions by displaying an error dialog.

* Fri Dec 22 2006 Chris Lumens <clumens@redhat.com> 2.7.0-1
- Use system-config-securitylevel to provide the firewall page.
- Speed up startup and shutdown.
- If package selection is disabled, don't forget whatever was in the
  original kickstart file (#217165).

* Thu Nov 30 2006 Chris Lumens <clumens@redhat.com> 2.6.19-1
- Update translation files (#216593).

* Mon Nov 20 2006 Chris Lumens <clumens@redhat.com> 2.6.18-1
- Don't require a root password (#215190).
- Disable package screen if yum couldn't download (#216439).

* Wed Nov 08 2006 Chris Lumens <clumens@redhat.com> 2.6.17-1
- Fix traceback when looking for the base Fedora repo (#190999).

* Fri Nov 03 2006 Chris Lumens <clumens@redhat.com> 2.6.16-1
- Fix partition growing traceback (#212955).

* Tue Oct 24 2006 Chris Lumens <clumens@redhat.com> 2.6.15-1
- Don't need to be root to run system-config-kickstart (patch from
  Panu Matilainen <Panu.Matilainen@nokia.com>, #211998).

* Mon Oct 16 2006 Chris Lumens <clumens@redhat.com> 2.6.14-1
- Use updated translations (#210728).
- Update documentation (#210863).
- Don't enable yum plugins.
- Disable popup menu on the package selection screen.

* Thu Jul 27 2006 Chris Lumens <clumens@redhat.com> 2.6.13-1
- Fix for yum config API changes again (#200095).
- Add 1280x800 to the resolution list (#156585).

* Mon Jul 10 2006 Chris Lumens <clumens@redhat.com> 2.6.12-1
- Fix for yum config API changes (#196841).

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 2.6.11-2
- Add gettext as a BR
- Fix up requires(post) and (postun)

* Mon Jun 05 2006 Chris Lumens <clumens@redhat.com> 2.6.11-1
- Write out a mount point for swap and raid partitions (#193262).
- Fix RAID member list printing.

* Fri May 05 2006 Chris Lumens <clumens@redhat.com> 2.6.10-1
- Fix unencrypted root password traceback (#190487).
- Try harder to get a base repo enabled (#190508).

* Fri Apr 21 2006 Chris Lumens <clumens@redhat.com> 2.6.9-1
- Add support for more device names.
- Display a progress bar while yum is working (#187435).

* Mon Mar 27 2006 Chris Lumens <clumens@redhat.com> 2.6.8-1 
- Fix loading kickstart files (#186944).

* Mon Mar 27 2006 Chris Lumens <clumens@redhat.com> 2.6.7-1 
- Fix support for --generate (#186635).

* Fri Feb 24 2006 Chris Lumens <clumens@redhat.com> 2.6.6-2
- Add requirement for scriptlets (#182865, #182866).

* Thu Feb 09 2006 Chris Lumens <clumens@redhat.com> 2.6.6-1
- Fix .desktop file, other references to /usr/sbin.

* Tue Feb 07 2006 Chris Lumens <clumens@redhat.com> 2.6.5-1
- Smarter repo-enabling code (#180097).

* Fri Feb 03 2006 Chris Lumens <clumens@redhat.com> 2.6.4-1
- Convert package selection to using pirut (#178759).
- Partitioning screen fixes for cciss.
- Use consolehelper.

* Wed Jan 04 2006 Chris Lumens <clumens@redhat.com> 2.6.3-1
- Remove references to monitor in xconfig (#176537).

* Mon Dec 12 2005 Chris Lumens <clumens@redhat.com> 2.6.2-1
- Use monitor keyword instead of deprecated xconfig options.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 03 2005 Chris Lumens <clumens@redhat.com> 2.6.1-1
- Remove requirement on rhpxl since we can work around it.

* Wed Nov 02 2005 Chris Lumens <clumens@redhat.com> 2.6.0-1
- Use pykickstart instead of our own kickstart file parsing code.

* Tue Sep 13 2005 Chris Lumens <clumens@redhat.com> 2.5.24-1
- Remove mouse and langsupport.  These two options have been removed from
  kickstart so we shouldn't be generating invalid files.
- Fail if we read a line we don't understand instead of being silent.
- Deal with drivers instead of cards due to kudzu changes.

* Tue May 31 2005 Chris Lumens <clumens@redhat.com> 2.5.23-1
- Use random module instead of whrandom (#159115).

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 2.5.22-2
- silence %%post

* Mon Apr 11 2005 Chris Lumens <clumens@redhat.com> 2.5.23-1
- Fixed string translation problems (#154247).

* Mon Apr 04 2005 Chris Lumens <clumens@redhat.com> 2.5.22-1
- Use the new GTK file selection dialogs for loading and saving (#152995).

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com> 2.5.21-4
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 2.5.21-3
- Update the GTK+ theme icon cache on (un)install

* Wed Mar 23 2005 Chris Lumens <clumens@redhat.com> 2.5.21-2
- Rebuilt translation files.

* Wed Mar 23 2005 Chris Lumens <clumens@redhat.com> 2.5.21-1
- Add SELinux support to the firewall page (#148966).
- Fix gtk deprecation warnings.

* Wed Jan 12 2005 Chris Lumens <clumens@redhat.com> 2.5.20-1 
- Default to English (USA) instead of English (Singapore).

* Mon Dec 20 2004 Chris Lumens <clumens@redhat.com> - 2.5.19-1
- Fixed a segfault in pygtk on the partitioning screen.
- Fixed RAID editing screen so the config values don't change if you
  repeatedly edit a RAID volume.

* Fri Dec 10 2004 Chris Lumens <clumens@redhat.com> - 2.5.18-1
- Get package group lists and their translations out of the comps.xml file
  instead of reying on a built-in (and out of date) list.
- Added an "Install Everything" button (#134679).

* Thu Dec 02 2004 Chris Lumens <clumens@redhat.com> - 2.5.17-1
- Remove obsolete dependency resolution radio buttons.

* Tue Nov 23 2004 Chris Lumens <clumens@redhat.com> - 2.5.16-1
- Fix display in indic locale (#138310) and (#138601)
- Monitor order (#127477)
- Translation of RAID message (#127687)
- Unencrypted root passwords (#134678)
- Broken nfs line parsing (#134681)

* Fri Oct 01 2004 Paul Nasrat <pnasrat@redhat.com> - 2.5.15-1
- Translations

* Tue Sep 21 2004 Paul Nasrat <pnasrat@redhat.com> - 2.5.14-1
- ks.cfg parsing errors

* Tue Sep 07 2004 Paul Nasrat <pnasrat@redhat.com> - 2.5.13-1
- i18n .desktop 

* Mon Sep 06 2004 Paul Nasrat <pnasrat@redhat.com> - 2.5.12-4
- PyGTK API fix

* Tue Aug 10 2004 Paul Nasrat <pnasrat@redhat.com> - 2.5.12-3
- Fix for mouse autoprobe (#129504)

* Mon Aug 02 2004 Paul Nasrat <pnasrat@redhat.com> 2.5.12-2 
- fix Japanese man page encoding (bug #128767)

* Wed Jun 23 2004 Brent Fox <bfox@redhat.com> - 2.5.12-1
- use base names for packages (bug #122755)

* Thu Jun 17 2004 Brent Fox <bfox@redhat.com> - 2.5.11-3
- comps name changed for KDE (bug #124612)
- format of rhpl mouse dict changed (bug #125361)

* Tue May 25 2004 Brent Fox <bfox@redhat.com> 2.5.11-2
- handle missing mouse line (bug #124341)
- use N_ instead of _ in packages.py (bug #124144)
- remove code for dead firewall widgets (bug #124342)

* Wed Apr 28 2004 Brent Fox <bfox@redhat.com> 2.5.11-1
- convert doc/ directory from redhat-config to system-config (bug #121554)

* Thu Apr  8 2004 Brent Fox <bfox@redhat.com> 2.5.10-2
- fix icon path (bug #120176)

* Tue Apr  6 2004 Brent Fox <bfox@redhat.com> 2.5.10-1
- fix typo in package.py (bug #119257)

* Mon Mar 29 2004 Brent Fox <bfox@redhat.com> 2.5.9-1
- fix rhpl mouse bug (#119258)
- more code to handle multi-platform

* Fri Mar 26 2004 Brent Fox <bfox@redhat.com> 
- first stab at making system-config-kickstart arch aware (bug #91905)
- removed LILO widgets

* Thu Mar 11 2004 Brent Fox <bfox@redhat.com> 2.5.8-1
- pull out package lists

* Fri Mar  5 2004 Brent Fox <bfox@redhat.com> 2.5.7-1
- support PPC PReP partitions (bug #116847)
- require Python2.3 for getopt.gnu_getopt() call

* Fri Mar  5 2004 Brent Fox <bfox@redhat.com> 2.5.6-1
- don't crash on file with no bootloader line (bug #117593)

* Thu Mar  4 2004 Brent Fox <bfox@redhat.com> 2.5.5-1
- fix capitalization problem (bug #117490)

* Thu Jan  8 2004 Brent Fox <bfox@redhat.com> 2.5.4-1
- only add --default to langsupport if more than one lang is selected (bug #111600)

* Tue Jan  6 2004 Brent Fox <bfox@redhat.com> 2.5.3-1
- add a requires for system-config-language
- get list of langs from system-config-language

* Mon Dec  1 2003 Brent Fox <bfox@redhat.com> 2.5.2-1
- change sync rate string (bug #107500)

* Wed Nov 19 2003 Brent Fox <bfox@redhat.com> 2.5.1-1
- rebuild

* Wed Nov 12 2003 Brent Fox <bfox@redhat.com> 2.5.0-1
- rename to system-config-kickstart
- change for Python2.3
- obsoletes redhat-config-kickstart

* Tue Oct 14 2003 Brent Fox <bfox@redhat.com> 2.4.2-1
- call language_backend correctly (bug #103625)

* Tue Sep 23 2003 Brent Fox <bfox@redhat.com> 2.4.1-1
- rebuild with latest docs

* Wed Sep 17 2003 Brent Fox <bfox@redhat.com> 2.3.19-2
- bump release

* Wed Sep 17 2003 Brent Fox <bfox@redhat.com> 2.3.19-1
- firstboot flag is "enable" not "enabled" (bug #104552)

* Mon Sep 15 2003 Brent Fox <bfox@redhat.com> 2.3.18-2
- bump relnum and rebuild

* Mon Sep 15 2003 Brent Fox <bfox@redhat.com> 2.3.18-1
- fix software raid code (bug #91812)

* Fri Aug 22 2003 Brent Fox <bfox@bfox.devel.redhat.com> 2.3.17-2
- bump relnum and rebuild

* Fri Aug 22 2003 Brent Fox <bfox@bfox.devel.redhat.com> 2.3.17-1
- handle maxsize, grow, and onpart correctly from existing files

* Thu Aug 14 2003 Brent Fox <bfox@redhat.com> 2.3.16-1
- tag on every build

* Tue Aug 12 2003 Brent Fox <bfox@redhat.com> 2.3.15-2
- bump relnum and rebuild

* Tue Aug 12 2003 Brent Fox <bfox@redhat.com> 2.3.15-1
- new security levels are "enabled" and "disabled" 

* Thu Jul 24 2003 Brent Fox <bfox@redhat.com> 2.3.14-2
- bump relnum and rebuild

* Thu Jul 24 2003 Brent Fox <bfox@redhat.com> 2.3.14-1
- fix typo(bug #100654)

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 2.3.13-2
- bump relnum and rebuild

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 2.3.13-1
- fix gladefile bug

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 2.3.12-2
- bump relnum and rebuild

* Tue Jul 22 2003 Brent Fox <bfox@redhat.com> 2.3.12-1
- add a firstboot widget (bug #100408)

* Fri Jul 18 2003 Brent Fox <bfox@redhat.com> 2.3.11-2
- bump relnum and rebuild

* Fri Jul 18 2003 Brent Fox <bfox@redhat.com> 2.3.11-1
- add the 'recommended' swap ks flag (bug #98156)

* Thu Jul 10 2003 Brent Fox <bfox@redhat.com> 2.3.10-2
- bump relnum and rebuild

* Thu Jul 10 2003 Brent Fox <bfox@redhat.com> 2.3.10-1
- clear network data when opening a new ks file

* Tue Jun  3 2003 Brent Fox <bfox@redhat.com> 2.3.9-1
- fix most of bug #92102

* Wed May 28 2003 Tammy Fox <tfox@redhat.com> 2.3.8-3
- bump release and rebuild

* Tue May 27 2003 Tammy Fox <tfox@redhat.com> 2.3.8-2
- removed length argument to GtkTextBuffer.insert() call
  since it is deprecated

* Fri May 23 2003 Brent Fox <bfox@redhat.com> 2.3.8-1
- remove midline comment for mouse in basic.py (bug #91502)

* Wed May 21 2003 Brent Fox <bfox@redhat.com> 2.3.7-1
- fall back to us keymap if the current keymap is not found (bug #88844)

* Mon Feb 24 2003 Brent Fox <bfox@redhat.com> 2.3.6-4
- apply patch from katzj to fix bug #84745

* Fri Feb 21 2003 Brent Fox <bfox@redhat.com> 2.3.6-3
- delete partitions properly (bug #84747)

* Tue Feb 11 2003 Brent Fox <bfox@redhat.com> 2.3.6-2
- rebuild with latest docs and translations

* Thu Jan 30 2003 Brent Fox <bfox@redhat.com> 2.3.6-1
- bump and build

* Tue Jan 21 2003 Brent Fox <bfox@redhat.com> 2.3.5-11
- update desktop file translations 
* Thu Jan 16 2003 Brent Fox <bfox@redhat.com> 2.3.5-10
- replace xconfig.py getopt calls with manual parsing (bug #80592)
* Thu Jan  9 2003 Brent Fox <bfox@redhat.com> 2.3.5-9
- fix bug while parsing network section of kickstart file
* Tue Jan  7 2003 Brent Fox <bfox@redhat.com> 2.3.5-8
- explicitly kill about box
- handle window delete-events correctly
* Thu Jan  2 2003 Brent Fox <bfox@redhat.com> 2.3.5-7
- add Dutch (bug #80594)
* Wed Dec 18 2002 Brent Fox <bfox@redhat.com> 2.3.5-6
- set the glade encoding correctly (bug #79980)
* Mon Dec 16 2002 Brent Fox <bfox@redhat.com> 2.3.5-5
- remove helpBrowser and use htmlview instead (bug #71858)
* Fri Dec 13 2002 Brent Fox <bfox@redhat.com> 2.3.5-4
- Change string from Language to Default Language (bug #70189)
* Wed Dec 11 2002 Brent Fox <bfox@redhat.com> 2.3.5-3
- Add a button for utc clocks (bug #70188)
* Tue Dec 10 2002 Brent Fox <bfox@redhat.com> 2.3.5-2
- update strings
- present an error message if run in console mode (bug #78737)
* Tue Dec 10 2002 Brent Fox <bfox@redhat.com> 2.3.5-1
- Rebuild for completeness
* Tue Dec 02 2002 Brent Fox <bfox@redhat.com> 2.3.4-3
- more work on the profiling.  exposed it with a command line option.  I think that's good enough.
* Mon Dec 02 2002 Brent Fox <bfox@redhat.com> 2.3.4-2
- rebuild for completeness
- added some new system profiling code, but it's not exposed in the UI yet
* Tue Nov 26 2002 Brent Fox <bfox@redhat.com> 2.3.4-1
- Handle opening existing kickstart files
- Handle multiple ethernet interfaces
- Don't require rootpassword on upgrades

* Tue Nov 05 2002 Brent Fox <bfox@redhat.com> 2.3.3-5
- Remove Minimal and Everything options from packages.py since they aren't in comps.xml

* Wed Oct 16 2002 Tammy Fox <tfox@redhat.com>
- Set modal windows to transient as well so they can't get hidden

* Mon Oct 14 2002 Brent Fox <bfox@redhat.com> 2.3.3-4
- Fix bug 75001.  Fix some reset states in partWindow.py

* Fri Aug 30 2002 Brent Fox <bfox@redhat.com> 2.3.3-3
- pull in latest translations

* Thu Aug 29 2002 Brent Fox <bfox@redhat.com> 2.3.3-2
- Pull in latest translations

* Tue Aug 27 2002 Brent Fox <bfox@redhat.com> 2.3.3-1
- Make customizing the firewall settings work again

* Thu Aug 23 2002 Brent Fox <bfox@redhat.com> 2.3.2-17
- bump release num

* Sat Aug 17 2002 Brent Fox <bfox@redhat.com> 2.3.2-16
- Don't write out --emulthree if No Mouse is selected
- Fix gtk.glade.bindtextdomain so that the glade screens pull in translations

* Wed Aug 14 2002 Tammy Fox <tfox@redhat.com> 2.3.2-15
- new icon from garrett

* Wed Aug 14 2002 Brent Fox <bfox@redhat.com> 2.3.2-14
- Rebuild with the latest docs and translations

* Wed Aug 14 2002 Brent Fox <bfox@redhat.com> 2.3.2-13
- Allow raid parititions and raid devices to be unformatted

* Tue Aug 13 2002 Tammy Fox <tfox@redhat.com> 2.3.2-12
- clarify language and language support options in docs

* Tue Aug 13 2002 Brent Fox <bfox@redhat.com> 2.3.2-11
- Fix bug 69667 with bootloader option overlap

* Mon Aug 12 2002 Tammy Fox <tfox@redhat.com> 2.3.2-10
- rebuilt with updated docs

* Sat Aug 10 2002 Brent Fox <bfox@redhat.com> 2.3.2-9
- Add error checking dialogs to install screen

* Wed Aug 07 2002 Brent Fox <bfox@redhat.com> 2.3.2-8
- fix desensitize bug in install screen

* Tue Aug 06 2002 Brent Fox <bfox@redhat.com> 2.3.2-7
- fix bug 70757

* Tue Aug 06 2002 Tammy Fox <tfox@redhat.com>
- Add window icons

* Mon Aug 05 2002 Brent Fox <bfox@redhat.com> 2.3.2-6
- More software raid code

* Fri Aug 02 2002 Tammy Fox <tfox@redhat.com>
- Reworked package group selection

* Thu Aug 01 2002 Brent Fox <bfox@redhat.com> 2.3.2-5
- Reworked GUI for bootloader screen
- Changed the order so that install appears before bootloader

* Fri Jul 26 2002 Tammy Fox <tfox@redhat.com>
- Changed Help menu item to Contents

* Thu Jul 25 2002 Brent Fox <bfox@redhat.com> 2.3.2-4
- Fixed bug 68147
- Write out the console keyboard keymap, not the X keymap

* Fri Jul 19 2002 Brent Fox <bfox@redhat.com> 2.3.2-3
- Added version dependency for pygtk2 API change

* Fri Jul 19 2002 Tammy Fox <tfox@redhat.com>
- Updated docs for latest interface and features

* Thu Jul 18 2002 Brent Fox <bfox@redhat.com>
- Added buttons for LVM and RAID.  I will wire them up later

* Thu Jul 18 2002 Tammy Fox <tfox@redhat.com> 2.3.2-2
- Updated list of langs
- Reimplemented keyboard list to use list from rhpl
- Fix for iter_next change

* Thu Jul 18 2002 Tammy Fox <tfox@redhat.com> 2.3.1-1
- Fixed bug 69169

* Mon Jul 15 2002 Brent Fox <bfox@redhat.com> 2.3-2
- Renamed doc files to redhat-config-kickstart

* Wed Jul 10 2002 Brent Fox <bfox@redhat.com> 2.3-1
- Renamed ksconfig to redhat-config-kickstart

* Fri Jun 28 2002 Brent Fox <bfox@redhat.com> 2.2-2
- Fix bug 66258

* Thu Jun 27 2002 Brent Fox <bfox@redhat.com> 2.2-1
- Install gtk2 glade file instead of the old one

* Tue Jun 25 2002 Brent Fox <bfox@redhat.com>
- Check to make sure that there's something in the partition window

* Mon Jun 17 2002 Brent Fox <bfox@redhat.com>
- completed the port to gtk2
- Fixed bug 65835
- Fixed bug 66815
- Fixed bug 64453 (with help from menthos@menthos.com)

* Fri Jun 14 2002 Tammy Fox <tfox@redhat.com>
- Added optional ftp username and password
- Added preview menu item
- Added bootloader --upgrade
- Added swap --recommended
- Added %packages -- resolvedeps and %packages --ignoredeps

* Wed May 22 2002 Brent Fox <bfox@redhat.com> 2.0-9
- Fixed bug #65323 to handle partition minimum size better

* Mon May 13 2002 Brent Fox <bfox@redhat.com> 2.0-8
- Fixed bug #64835 to make UK keyboard 'uk' not 'gb'

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.0-7
- Update translations

* Thu Apr 11 2002 Brent Fox <bfox@redhat.com>
- Added msw's code snippet to disable threads
- Fixed bug #63191

* Tue Apr 02 2002 Tammy Fox <tfox@redhat.com>
- updated docs

* Sun Jan 20 2002 Brent Fox <bfox@redhat.com>
- fixed bug #58570

* Sun Nov 11 2001 Tammy Fox <tfox@redhat.com>
- added encrypt GRUB password

* Thu Sep 13 2001 Tammy Fox <tfox@redhat.com>
- fixed bug #53408

* Thu Aug 09 2001 Tammy Fox <tfox@redhat.com>
- Updated docs for encrypt root password option

* Thu Aug 09 2001 Brent Fox <bfox@redhat.com>
- Allow user to select plaintext or encrypted root password

* Fri Jul 20 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese translation
- Some fix around gettext

* Wed Jul 18 2001 Tammy Fox <tfox@redhat.com>
- added po directory
- added grub password and initialize the disk label
- added help manual and function to display it

* Mon Jul 16 2001 Brent Fox <bfox@redhat.com>
- finished partitioning page

* Tue Jul 10 2001 Tammy Fox <tfox@redhat.com>
- added boot loader options page
- added text mode install 

* Sat Jul 07 2001 Tammy Fox <tfox@redhat.com>
- added reboot after installation option

* Fri Jul 06 2001 Tammy Fox <tfox@redhat.com>
- added xconfig page
- added install and upgrade radiobuttons

* Thu Jul 05 2001 Brent Fox <bfox@redhat.com>
- added package page

* Tue Jun 26 2001 Tammy Fox <tfox@redhat.com>
- added emulate three buttons and probe for mouse options
- added preview configuration window
- modified basic.py to use dictionaries to store combo box selections

* Sat Jun 23 2001 Brent Fox <bfox@redhat.com>
- fixed auth callback for new interface

* Fri Jun 22 2001 Tammy Fox <tfox@redhat.com>
- redesigned interface
- redesigned code to be more modular

* Wed Jun 13 2001 Tammy Fox <tfox@redhat.com>
- added more info to man page

* Wed Mar  7 2001 Bill Nottingham <notting@redhat.com>
- put the GPL in %doc

* Thu Mar 01 2001 Tammy Fox <tfox@redhat.com>
- fixed end of line between auth and firewall lines

* Fri Feb 23 2001 Tammy Fox <tfox@redhat.com>
- moved package icons into package instead of requiring anaconda for them

* Fri Feb 16 2001 Tammy Fox <tfox@redhat.com>
- added scrollwindow around partition information
- made all widgets except partition scrollwindow unexpandable so that when the main window is resized only the partition list gets bigger
- increased release number

* Wed Feb 14 2001 Brent Fox <bfox@redhat.com>
- fixed bug with the firewall screen

* Thu Feb 8 2001 Brent Fox <bfox@redhat.com>
- made code modular
- improved package selection screen
- implemented firewall screen

* Sat Jan 27 2001 Tammy Fox <tfox@redhat.com>
- added file dialog box
- cleaned up code
- renamed okButton to saveButton in ksconfig.py
- renamed Cancel button to Exit in interface
- added /boot to default partition list
- added menu icon

* Tue Jan 16 2001 Brent Fox <bfox@redhat.com>
- initial packaging

