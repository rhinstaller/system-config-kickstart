Summary: A graphical interface for making kickstart files.
Name: redhat-config-kickstart
Version: 2.3.7
Release: 1
URL: http://www.redhat.com
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArch: noarch
Source0: %{name}-%{version}.tar.bz2
Obsoletes: ksconfig
BuildRequires: desktop-file-utils
Requires: pygtk2 >= 1.99.11
Requires: pygtk2-libglade 
Requires: python2
Requires: hwdata
Requires: rhpl

%description
Kickstart Configurator is a graphical tool for creating kickstart files.  

%prep
%setup -q

%install
make INSTROOT=$RPM_BUILD_ROOT install
desktop-file-install --vendor redhat --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-category Application \
  --add-category System \
  --add-category X-Red-Hat-Base          \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d /usr/share/%{name} ] ; then
  rm -rf /usr/share/%{name}/*.pyc
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc doc/*
/usr/sbin/%{name}
/usr/sbin/ksconfig
%dir /usr/share/%{name}
/usr/share/%{name}/*
/usr/share/%{name}/pixmaps/%{name}.png
%{_mandir}/man8/%{name}*
%lang(ja) %{_mandir}/ja/man8/%{name}*
%attr(0644,root,root) %{_datadir}/applications/%{name}.desktop

%changelog
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

