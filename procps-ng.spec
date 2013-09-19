%define major 1
%define libname %mklibname procps %{major}
%define devname %mklibname procps -d
%bcond_with	crosscompile

Summary:	Utilities for monitoring your system and processes on your system
Name:		procps-ng
Version:	3.3.8
Release:	3
License:	GPLv2+
Group:		Monitoring
URL:		http://sourceforge.net/projects/procps-ng/
Source0:	http://downloads.sourceforge.net/project/procps-ng/Production/%{name}-%{version}.tar.xz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libsystemd-login)
Requires:	systemd-units
%rename		procps3
%rename		procps

%description
The procps package contains a set of system utilities
which provide system information.

%package -n	%{libname}
Summary:	Main libary for %{name}
Group:		System/Libraries
License:	LGPLv2+
Obsoletes:	%{mklibname procps 0} < 3.3.6

%description -n	%{libname}
Main library for %{name}.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPLv2+
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
Development headers and library for the %{name} library.

%prep
%setup -q
sed -e 's#${exec_prefix}/usr/bin#${bindir}#' -i configure.ac

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
%endif

autoreconf -fiv

%configure2_5x \
	--sbindir=/sbin \
	--disable-rpath \
	--disable-static \
	--disable-watch8bit \
	--disable-kill \
    --with-systemd

%make

%install
%makeinstall_std

mkdir %{buildroot}/{bin,%{_lib}}
mv %{buildroot}%{_bindir}/free %{buildroot}/bin
mv %{buildroot}%{_bindir}/ps %{buildroot}/bin

mv %{buildroot}%{_libdir}/libprocps.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libprocps.so.%{major}.*.* %{buildroot}%{_libdir}/libprocps.so

%files
%doc NEWS AUTHORS
%doc top/README.top Documentation/FAQ Documentation/BUGS
/bin/ps
/bin/free
/sbin/sysctl
%{_bindir}/pgrep
%{_bindir}/pmap
%{_bindir}/pwdx
%{_bindir}/pkill
%{_bindir}/slabtop
%{_bindir}/tload
%{_bindir}/top
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/w
%{_bindir}/watch
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files -n %{libname}
/%{_lib}/libprocps.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/proc
%{_includedir}/proc/*.h
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
