%define major 2
%define libname %mklibname ggz %{major}
%define develname %mklibname -d ggz

# Enable encryption support?
%define enable_encrypt 0
%{?_with_encrypt: %global enable_encrypt 1}

# select between GNUTLS or OpenSSL
%define use_openssl 0
%{?_with_openssl: %global use_openssl 1}

Name:		libggz
Summary:	Common library for the GGZ Gaming Zone
Version:	0.0.14.1
Release:	10
License:	GPL
Group:		System/Libraries
URL:		http://ggzgamingzone.org/
Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2

%if %{enable_encrypt}
%if %{use_openssl}
BuildRequires:	pkgconfig(openssl)
%else
BuildRequires:	pkgconfig(gnutls)
%endif
%endif

%description
The GGZ Gaming Zone server allows other computers to connect to yours via
the Internet and play network games. This library provides features required
for running both clients and the server.

Build Option:
--with encrypt      Enable encryption support
--with openssl      Prefer OpenSSL to GNUTLS, for encryption support
                    (Useless unless "--with encrypt" is also used)

%package	-n %{libname}
Summary:	Common library for running GGZ Gaming Zone applications
Group:		Games/Other
Provides:	%{name} = %{version}-%{release}

%description	-n %{libname}
The GGZ Gaming Zone server allows other computers to connect to yours
via the Internet and play network games. 

This package contains the shared library that provides features
required for running both clients and the server.

%package	-n %{develname}
Summary:	Development files used to build GGZ Gaming Zone applications
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description	-n %{develname}
The GGZ Gaming Zone server allows other computers to connect to yours
via the Internet and play network games. 

This package contains the libraries required for building both clients
and the server.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
%if %enable_encrypt
	--with-gcrypt=yes	\
%if %use_openssl
	--with-tls=OpenSSL	\
%else
	--with-tls=GnuTLS	\
%endif
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%files -n %{libname}
%doc AUTHORS COPYING NEWS README README.GGZ QuickStart.GGZ
%{_libdir}/libggz.so.%{major}*
%{_mandir}/man?/*

%files -n %{develname}
%doc COPYING ChangeLog
%{_includedir}/*
%{_libdir}/libggz.so

%changelog
* Tue Dec 06 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.0.14.1-9
+ Revision: 738075
- rebuild
- cleaned up spec
- removed defattr, mkrel, BuildRoot, clean section
- removed old ldconfig scriptlets
- removed .la files
- disabled static build

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-8
+ Revision: 661463
- mass rebuild

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-7mdv2011.0
+ Revision: 602548
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-6mdv2010.1
+ Revision: 520804
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.0.14.1-5mdv2010.0
+ Revision: 425546
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.0.14.1-4mdv2009.0
+ Revision: 264804
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sat May 03 2008 Funda Wang <fwang@mandriva.org> 0.0.14.1-3mdv2009.0
+ Revision: 200665
- drop debug detection
- new devel package policy

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-2mdv2008.1
+ Revision: 189657
- Fix groups
- protect major

* Mon Feb 25 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-1mdv2008.1
+ Revision: 174506
- New version

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 0.0.14-3mdv2008.1
+ Revision: 150566
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.0.14-2mdv2008.0
+ Revision: 89837
- rebuild


* Sun Feb 04 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-1mdv2007.0
+ Revision: 116120
- New version 0.0.14
- rebuild
- Import libggz

* Mon May 22 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-2mdk
- fix man pages package location

* Mon May 22 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-1mdk
- New version
- mkrel

* Wed Oct 19 2005 Emmanuel Blindauer <blindauer@mandriva.org> 0.0.12-1mdk
- New version

* Sat Nov 27 2004 Abel Cheung <deaddog@mandrake.org> 0.0.9-1mdk
- New version

* Tue Feb 10 2004 Abel Cheung <deaddog@deaddog.org> 0.0.8-1mdk
- New version
- Disable encryption altogether, it is expecting old gcrypt
  (anyway I can't get encryption to work so far in old release)

