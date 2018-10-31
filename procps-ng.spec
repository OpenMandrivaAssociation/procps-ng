%define major 7
%define libname %mklibname procps %{major}
%define devname %mklibname procps -d
%bcond_with crosscompile

Summary:	Utilities for monitoring your system and processes on your system
Name:		procps-ng
Version:	3.3.15
Release:	3
License:	GPLv2+
Group:		Monitoring
Url:		http://sourceforge.net/projects/procps-ng/
Source0:	http://downloads.sourceforge.net/project/procps-ng/Production/%{name}-%{version}.tar.xz
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libsystemd)
%rename		sysvinit-tools
%rename		procps3
%rename		procps

%description
The procps package contains a set of system utilities
which provide system information.

%package -n %{libname}
Summary:	Main libary for %{name}
Group:		System/Libraries
License:	LGPLv2+

%description -n %{libname}
Main library for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPLv2+
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development headers and library for the %{name} library.

%prep
%setup -q
%apply_patches
sed -e 's#${exec_prefix}/usr/bin#${bindir}#' -i configure.ac
autoreconf -fiv

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
%endif

%configure \
	--sbindir=/sbin \
	--disable-static \
	--enable-watch8bit \
	--disable-kill \
	--enable-wide-percent \
	--enable-skill \
	--enable-sigwinch \
	--with-systemd \
	--enable-oomem \
	--enable-w-from

%make

%install
%makeinstall_std

mkdir %{buildroot}/{bin,%{_lib}}
mv %{buildroot}%{_bindir}/free %{buildroot}/bin
mv %{buildroot}%{_bindir}/ps %{buildroot}/bin
mv %{buildroot}%{_bindir}/pidof %{buildroot}/bin
ln -s /bin/pidof %{buildroot}/sbin

mv %{buildroot}%{_libdir}/libprocps.so.%{major}* %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libprocps.so.%{major}.*.* %{buildroot}%{_libdir}/libprocps.so

rm -rf %{buildroot}%{_docdir}/%{name}

%find_lang %{name}

%files -f %{name}.lang
/bin/free
/bin/pidof
/bin/ps
/sbin/pidof
/sbin/sysctl
%{_bindir}/pgrep
%{_bindir}/pmap
%{_bindir}/pwdx
%{_bindir}/pkill
%{_bindir}/skill
%{_bindir}/slabtop
%{_bindir}/snice
%{_bindir}/tload
%{_bindir}/top
%{_bindir}/uptime
%{_bindir}/vmstat
%{_bindir}/w
%{_bindir}/watch
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files -n %{libname}
/%{_lib}/libprocps.so.%{major}*

%files -n %{devname}
%doc NEWS AUTHORS
%doc Documentation/FAQ Documentation/bugs.md
%dir %{_includedir}/proc
%{_includedir}/proc/*.h
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
