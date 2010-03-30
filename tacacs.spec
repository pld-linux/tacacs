
%bcond_with     skey		# with S/KEY support

Summary:	TACACS+ Daemon
Summary(pl.UTF-8):	Demon TACACS+
Name:		tacacs
Version:	F4.0.4.19
Release:	1
Epoch:		0
License:	BSD-like, GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.shrubbery.net/pub/%{name}/tacacs+-%{version}.tar.gz 
# Source0-md5:	4979127f60f1a83c55e8a7cec285a797
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.pam
Source6:	%{name}.rotate
Source8:	%{name}.sysconfig
URL:		http://www.shrubbery.net/tac_plus/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libwrap-devel
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
%if %{with skey}
BuildRequires:	skey-static
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	fileutils
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		__make		/usr/bin/make -j1

%description
TACACS+ daemon using with Cisco's NASs (or other vendors) for AAA
(Authentication, Authorization and Accounting) propose.

%description -l pl.UTF-8
Demon TACACS+ używany wraz z NAS-ami Cisco (lub innych producentów) do
celów uwierzytelniania, autoryzacji i rozliczania (AAA -
Authentication, Authorization and Accounting).

%prep
%setup -q -n %{name}+-%{version}

%build
%configure 

%{__make} \
	%{?with_skey:DEFINES="-DSKEY" LIBS="/usr/lib/libskey.a" INCLUDES="-I/usr/include/security/"}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/tacacs,/etc/{logrotate.d,pam.d,rc.d/init.d,sysconfig}}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/tacacs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/tacacs
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/tac_plus
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/tacacs
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/tacacs

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add tacacs
%service tacacs restart

%preun
if [ "$1" = "0" ]; then
	%service tacacs stop
	/sbin/chkconfig --del tacacs
fi

%files
%defattr(644,root,root,755)
%doc users_guide CHANGES
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/tacacs
%dir %{_datadir}/tacacs+
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tacacs/tacacs.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/tacacs
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/tac_plus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/tacacs
%attr(754,root,root) /etc/rc.d/init.d/tacacs
%{_mandir}/man?/*
%{_includedir}/tacacs.h
%{_libdir}/*
%{_datadir}/tacacs+/*
