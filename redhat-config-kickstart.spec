Summary: A graphical interface for making kickstart files.
Name: redhat-config-kickstart
Version: 2.3.2
Release: 3
URL: http://www.redhat.com
License: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/redhat-config-kickstart-%{version}-root
BuildArch: noarch
Source0: redhat-config-kickstart-%{version}.tar.gz
Obsoletes: ksconfig
Requires: pygtk2 >= 1.99.11
Requires: pygtk2-libglade 
Requires: python2
Requires: hwdata
Requires: rhpl

%description
redhat-config-kickstart is a graphical tool for creating kickstart files.  

%prep
%setup -q

%install
make INSTROOT=$RPM_BUILD_ROOT install

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d /usr/share/redhat-config-kickstart ] ; then
  rm -rf /usr/share/redhat-config-kickstart/*.pyc
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc doc/*
/usr/sbin/redhat-config-kickstart
/usr/sbin/ksconfig
%dir /usr/share/redhat-config-kickstart
/usr/share/redhat-config-kickstart/*
%{_mandir}/man8/redhat-config-kickstart*
%lang(ja) %{_mandir}/ja/man8/redhat-config-kickstart*
%config /etc/X11/applnk/System/redhat-config-kickstart.desktop

%changelog
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

