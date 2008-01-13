%define version 0.0.14
%define release %mkrel 3

%define major 2
%define libname %mklibname ggz %{major}

# Enable encryption support?
%define enable_encrypt 0
%{?_with_encrypt: %global enable_encrypt 1}

# select between GNUTLS or OpenSSL
%define use_openssl 0
%{?_with_openssl: %global use_openssl 1}

Name:		libggz
Summary:	Common library for the GGZ Gaming Zone
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://ggzgamingzone.org/
Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%if %enable_encrypt
%if %use_openssl
BuildRequires:	openssl-devel
%else
BuildRequires:	gnutls-devel
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


%package	-n %{libname}-devel
Summary:	Development files used to build GGZ Gaming Zone applications
Group:		Development/Other
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description	-n %{libname}-devel
The GGZ Gaming Zone server allows other computers to connect to yours
via the Internet and play network games. 

This package contains the libraries required for building both clients
and the server.

%prep
%setup -q

%build
%configure \
%{?_enable_debug_packages: " --enable-debug --enable-debug-gdb --enable-debug-mem"} \
%{!?_enable_debug_packages: " --enable-noregistry"} \
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

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README README.GGZ QuickStart.GGZ
%{_libdir}/libggz.so.*
%{_mandir}/man?/*


%files -n %{libname}-devel
%defattr(-,root,root)
%doc COPYING ChangeLog
%{_includedir}/*
%{_libdir}/libggz.a
%{_libdir}/libggz.la
%{_libdir}/libggz.so


