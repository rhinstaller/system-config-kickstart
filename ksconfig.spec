Summary: A graphical interface for making kickstart files.
Name: ksconfig
Version: 2.1
Release: 1
URL: http://www.redhat.com
Copyright: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/ksconfig-%{version}-root
BuildArch: noarch
Source: ksconfig-%{version}.tar.gz
BuildRequires: python-devel
BuildRequires: gnome-libs-devel
Requires: pygtk 
Requires: pygtk-libglade 
Requires: python2
Requires: hwdata

%description
ksconfig is a graphical tool for creating kickstart files.  

%prep
%setup -q

%install
make INSTROOT=$RPM_BUILD_ROOT install

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d /usr/share/ksconfig ] ; then
  rm -rf /usr/share/ksconfig/*.pyc
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc doc/*
/usr/sbin/ksconfig
%dir /usr/share/ksconfig
/usr/share/ksconfig/*
%{_mandir}/man8/ksconfig*
%lang(ja) %{_mandir}/ja/man8/ksconfig*
%config /etc/X11/applnk/System/ksconfig.desktop

%changelog
* Fri Jun 14 2002 Tammy Fox <tfox@redhat.com>
- Added optional ftp username and password
- Added preview menu item
- Added bootloader --upgrade
- Added swap --recommended

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

