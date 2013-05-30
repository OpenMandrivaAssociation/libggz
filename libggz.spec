%define major	2
%define libname	%mklibname ggz %{major}
%define devname	%mklibname -d ggz

# Enable encryption support?
%define enable_encrypt 0
%{?_with_encrypt: %global enable_encrypt 1}

# select between GNUTLS or OpenSSL
%define use_openssl 0
%{?_with_openssl: %global use_openssl 1}

Summary:	Common library for the GGZ Gaming Zone
Name:		libggz
Version:	0.0.14.1
Release:	10
License:	GPLv2
Group:		System/Libraries
Url:		http://ggzgamingzone.org/
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

%package	-n %{devname}
Summary:	Development files used to build GGZ Gaming Zone applications
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description	-n %{devname}
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
%makeinstall_std

%files -n %{libname}
%{_libdir}/libggz.so.%{major}*

%files -n %{devname}
%doc AUTHORS COPYING NEWS README README.GGZ QuickStart.GGZ ChangeLog
%{_includedir}/*
%{_libdir}/libggz.so
%{_mandir}/man3/ggz.h.3*

