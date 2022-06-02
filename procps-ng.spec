%define major 8
%define libname %mklibname procps %{major}
%define devname %mklibname procps -d
%bcond_with crosscompile
%global optflags %{optflags} -Oz

Summary:	Utilities for monitoring your system and processes on your system
Name:		procps-ng
Version:	3.3.17
Release:	3
License:	GPLv2+
Group:		Monitoring
Url:		http://sourceforge.net/projects/procps-ng/
Source0:	http://downloads.sourceforge.net/project/procps-ng/Production/%{name}-%{version}.tar.xz
Patch1:		https://src.fedoraproject.org/rpms/procps-ng/raw/rawhide/f/pwait-to-pidwait.patch
Patch2:		https://src.fedoraproject.org/rpms/procps-ng/raw/rawhide/f/covscan-findings.patch
Patch3:		https://src.fedoraproject.org/rpms/procps-ng/raw/rawhide/f/sysctl-hyphen-param.patch
BuildRequires:	libtool
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd-rpm-macros
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
%autosetup -p1 -n procps-%{version}

sed -e 's#${exec_prefix}/usr/bin#${bindir}#' -i configure.ac
autoreconf -fiv

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
%endif

%configure \
	--disable-static \
	--enable-watch8bit \
	--disable-kill \
	--enable-wide-percent \
	--enable-skill \
	--enable-sigwinch \
	--with-systemd \
	--enable-oomem \
	--enable-w-from \
	--enable-pidwait

%make_build

%install
%make_install

mkdir -p %{buildroot}/{bin,sbin}
for i in free ps pidof; do
    ln -s %{_bindir}/$i %{buildroot}/bin/$i
done
ln -s %{_bindir}/pidof %{buildroot}/sbin/pidof
ln -s %{_bindir}/pidof %{buildroot}/%{_sbindir}/pidof
ln -s %{_sbindir}/sysctl %{buildroot}/sbin/sysctl

rm -rf %{buildroot}%{_docdir}/%{name}

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
/bin/*
/sbin/*
%{_sbindir}/*
%{_bindir}/*
%doc %{_mandir}/man1/*.1*
%doc %{_mandir}/man5/*.5*
%doc %{_mandir}/man8/*.8*

%files -n %{libname}
%{_libdir}/libprocps.so.%{major}*

%files -n %{devname}
%doc NEWS AUTHORS
%doc Documentation/FAQ Documentation/bugs.md
%dir %{_includedir}/proc
%{_includedir}/proc/*.h
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
%doc %{_mandir}/man3/*.3*
