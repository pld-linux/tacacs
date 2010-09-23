
%bcond_with	skey		# with S/KEY support
#skey_fn.c: In function 'skey_fn':
#skey_fn.c:167: error: too many arguments to function 'skeychallenge'

Summary:	TACACS+ daemon
Summary(pl.UTF-8):	Demon TACACS+
Name:		tacacs
Version:	F4.0.4.19
Release:	1
License:	BSD-like, GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.shrubbery.net/pub/tac_plus/tacacs+-%{version}.tar.gz
# Source0-md5:	4979127f60f1a83c55e8a7cec285a797
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.pam
Source6:	%{name}.rotate
Source8:	%{name}.sysconfig
URL:		http://www.shrubbery.net/tac_plus/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	pam-devel
BuildRequires:	perl-base
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_skey:BuildRequires:	skey-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	fileutils
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TACACS+ daemon using with Cisco's NASs (or other vendors) for AAA
(Authentication, Authorization and Accounting) propose.

%description -l pl.UTF-8
Demon TACACS+ używany wraz z NAS-ami Cisco (lub innych producentów) do
celów uwierzytelniania, autoryzacji i rozliczania (AAA -
Authentication, Authorization and Accounting).

%package devel
Summary:	Header files for tacacs+ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tacacs+
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header files for tacacs+ library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tacacs+.

%package static
Summary:        Static tacacs+ library
Summary(pl.UTF-8):      Statyczna biblioteka tacacs+
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static tacacs+ library.

%description static -l pl.UTF-8
Statyczna biblioteka tacacs+.

%prep
%setup -q -n %{name}+-%{version}

%build
%configure \
	--enable-finger \
	--enable-maxsess \
	--with-userid=29 \
	--with-groupid=29 \
	%{?with_skey:--with-skey}

%{__make} \
	%{?with_skey:INCLUDES="-I%{_includedir}/security"}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},/etc/{logrotate.d,pam.d,rc.d/init.d,sysconfig},/var/log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/tac_plus
install %{SOURCE6} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install %{SOURCE8} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

for n in tac_plus.acct tac_plus.log tacwho.log; do
	:> $RPM_BUILD_ROOT/var/log/$n
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 29 -r -f radius
%useradd -u 29 -d %{_localstatedir} -s /bin/false -M -r -c "%{name}" -g radius radius

%post
/sbin/ldconfig
for n in /var/log/{tac_plus.acct,tac_plus.log,tacwho.log}; do
	[ -f $n ] && continue
	touch $n
	chmod 660 $n
	chown root:radius $n
done
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove radius
	%groupremove radius
fi

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING FAQ users_guide
%attr(755,root,root) %{_bindir}/tac_p*
%dir %{_sysconfdir}/%{name}
%attr(640,root,radius) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/tacacs.cfg
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/tac_plus
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man5/tac_p*.5*
%{_mandir}/man8/tac_p*.8*
%attr(755,root,root) %{_libdir}/libtacacs.so.1.*.*
%attr(755,root,root) %ghost %{_libdir}/libtacacs.so.?
%{_datadir}/%{name}+
%attr(660,root,radius) %ghost /var/log/tac*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtacacs.so
%{_includedir}/tacacs.h
# doesn't it conflict with erlang?
%{_mandir}/man3/regexp.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtacacs.a
%{_libdir}/libtacacs.la
