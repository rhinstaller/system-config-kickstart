Summary: A graphical interface for making kickstart files.
Name: ksconfig
Version: 1.9.4
Release: 0
URL: http://www.redhat.com
Copyright: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/ksconfig-%{version}-root
BuildArch: noarch
Source: ksconfig-%{version}.tar.gz
Requires: pygnome pygtk pygtk-libglade pygnome-libglade
Requires: python >= 1.5.2

%description
ksconfig is a graphical tool for creating kickstart files.  It will 
allow you to set most of the kickstart options.

%prep
%setup -q

%install
make INSTROOT=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/System
cat > $RPM_BUILD_ROOT/etc/X11/applnk/System/ksconfig.desktop << EOF
[Desktop Entry]
Name=Kickstart Configurator
Comment=Kickstart file generator
Icon=redhat/shadowman-round-48.png
Exec=/usr/sbin/ksconfig
Type=Application
Terminal=false
EOF

#%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -d /usr/share/ksconfig ] ; then
  rm -rf /usr/share/ksconfig/*.pyc
fi

#%files -f %{name}.lang
%files
%defattr(-,root,root)
%doc COPYING
/usr/sbin/ksconfig
%dir /usr/share/ksconfig
/usr/share/ksconfig/*
%{_mandir}/man8/ksconfig*
%config /etc/X11/applnk/System/ksconfig.desktop

%changelog
* Tue Jul 18 2001 Tammy Fox <tfox@redhat.com>
- added i18n stuff
- added grub password and initialize the disk label

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

