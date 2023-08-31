%define major 0
%define libname %mklibname proc2_ %{major}
%define devname %mklibname proc2 -d
%bcond_with crosscompile
%global optflags %{optflags} -Oz

Summary:	Utilities for monitoring your system and processes on your system
Name:		procps-ng
Version:	4.0.4
Release:	1
License:	GPLv2+
Group:		Monitoring
Url:		http://sourceforge.net/projects/procps-ng/
# Also: https://gitlab.com/procps-ng/procps
Source0:	http://downloads.sourceforge.net/project/procps-ng/Production/%{name}-%{version}.tar.xz
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
Obsoletes:	%{mklibname procps 8} < %{EVRD}
Obsoletes:	%{mklibname proc-2} < %{EVRD}

%description -n %{libname}
Main library for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
License:	LGPLv2+
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname -d procps} < %{EVRD}
Obsoletes:	%{mklibname -d proc-2} < %{EVRD}

%description -n %{devname}
Development headers and library for the %{name} library.

%prep
%autosetup -p1

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

rm -rf %{buildroot}%{_docdir}/%{name}

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
%{_bindir}/*
%doc %{_mandir}/man1/*.1*
%doc %{_mandir}/man5/*.5*
%doc %{_mandir}/man8/*.8*

%files -n %{libname}
%{_libdir}/libproc2.so.%{major}*

%files -n %{devname}
%doc NEWS AUTHORS
%{_includedir}/libproc2
%{_libdir}/libproc2.so
%{_libdir}/pkgconfig/libproc2.pc
%doc %{_mandir}/man3/*.3*
