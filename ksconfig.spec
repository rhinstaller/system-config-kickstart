Summary: A graphical interface for making kickstart files.
Name: ksconfig
Version: 1.0
Release: 2
Copyright: GPL
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/ksconfig-%{version}-root
Source: ksconfig-%{version}.tar.gz
ExclusiveArch: noarch
Requires: pygtk

%description
ksconfig is a graphical tool for creating kickstart files.  It will allow you to set most of the kickstart options.

%prep
%setup -q

%install
make INSTROOT=$RPM_BUILD_ROOT install

#%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

#%files -f %{name}.lang
%files
%defattr(-,root,root)
/usr/sbin/ksconfig
%{_mandir}/*/*

%changelog
* Tue Jan 16 2001 Brent Fox <bfox@redhat.com>
- initial packaging

* Sat Jan 27 2001 Tammy Fox <tfox@redhat.com>
- added file dialog box
- cleaned up code
- renamed okButton to saveButton
