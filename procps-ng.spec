%define major_version	3
%define minor_version	3
%define revision	3

%define major 0
%define libname %mklibname procps %{major}
%define develname %mklibname procps -d

Summary:	Utilities for monitoring your system and processes on your system
Name:		procps-ng
Version:	%{major_version}.%{minor_version}.%{revision}
Release:	1
License:	GPL
Group:		Monitoring
URL:		http://gitorious.org/procps
Source0:	http://gitorious.org/procps/procps/archive-tarball/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
#BuildRequires:	ncursesw-devel
Provides:	libproc.so.%{major_version}.%{minor_version}
Provides:	procps3
Obsoletes:	procps3 < 3.3.3
%rename		procps

%description
The procps package contains a set of system utilities
which provide system information.

%package -n %{libname}
Summary:	Main libary for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Main library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development headers and library for the %{name} library.

%prep
%setup -q -n procps-procps
sed -e 's#${exec_prefix}/usr/bin#${bindir}#' -i configure.ac

./autogen.sh

%build
%configure2_5x \
	--sbindir=/sbin \
	--libdir=/%{_lib} \
	--disable-rpath \
	--disable-static \
	--disable-watch8bit \
	--disable-kill

%make

%install
%makeinstall_std

# (tpg) move some binaries and provide compat symlinks
mkdir -p %{buildroot}/{/bin,%{_libdir},%{_libdir}/pkgconfig}

mv %{buildroot}%{_bindir}/free %{buildroot}/bin
mv %{buildroot}%{_bindir}/ps %{buildroot}/bin
mv %{buildroot}/%{_lib}/pkgconfig/libprocps.pc %{buildroot}%{_libdir}/pkgconfig

ln -s ../../bin/free %{buildroot}%{_bindir}/free
ln -s ../../%{_lib}/libprocps.so %{buildroot}%{_libdir}/libprocps.so
ln -s ../../%{_lib}/libprocps.so.%{major} %{buildroot}%{_libdir}/libprocps.so.%{major}

# get rid of this
rm -rf %{buildroot}/share/doc/%{name}

%files
%doc NEWS AUTHORS
%doc top/README.top Documentation/FAQ Documentation/BUGS
/bin/ps
/bin/free
/sbin/sysctl
%{_bindir}/free
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
%{_libdir}/libprocps.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/proc
%{_includedir}/proc/*.h
/%{_lib}/libprocps.so
%{_libdir}/libprocps.so
%{_libdir}/pkgconfig/libprocps.pc
