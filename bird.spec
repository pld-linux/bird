
%bcond_without ipv6	# disable IPv6 support (and building bird-ipv6 package) 
%bcond_without ipv4	# disable IPv4 support (and building bird-ipv4 package)

# TODO:
#	- trigger to clean up after old bird package (stop, chkconfig --del)

Summary:	Routing daemon
Summary(pl):	Demon dynamicznego routingu
Name:		bird
Version:	1.0.9
Release:	0.3
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://bird.network.cz/pub/bird/%{name}-%{version}.tar.gz
# Source0-md5:	6a1d94b8a33b80e754ea4f9cc0ac1ff3
Source1:	%{name}-ipv4.init
Source2:	%{name}-ipv4.sysconfig
Source3:	%{name}-ipv6.init
Source4:	%{name}-ipv6.sysconfig
Patch0:		%{name}-posix.patch
Patch1:		%{name}-flex.patch
URL:		http://bird.network.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	readline-devel >= 4.2
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	bird-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	gated
Obsoletes:	mrt
Obsoletes:	zebra
Obsoletes:	zebra-guile

%description
The BIRD project is an attempt to create a routing daemon running on
UNIX-like systems (but not necessarily limited to them) with full
support of all modern routing protocols, easy to use configuration
interface and powerful route filtering language.

%description -l pl
Projekt BIRD ma na celu utworzenie daemona dynamicznego routingu
pracuj±cego na systemach UNIX z pe³nym wsparciem dla nowoczesnych
protoko³ów routingu, ³atwym interfejsem konfiguracji i jêzykiem
filtrów o du¿ych mo¿liwo¶ciach.

%package ipv4
Summary:	Routing daemon for IPv4
Summary(pl):	Demon dynamicznego routingu IPv4
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	routingdaemon
Provides:	bird-daemon
Obsoletes:	gated
Obsoletes:	mrt
Obsoletes:	zebra
Obsoletes:	zebra-guile
Requires:	%{name} = %{version}-%{release}

%description ipv4
The BIRD project is an attempt to create a routing daemon running on
UNIX-like systems (but not necessarily limited to them) with full
support of all modern routing protocols, easy to use configuration
interface and powerful route filtering language.

%description -l pl ipv4
Projekt BIRD ma na celu utworzenie daemona dynamicznego routingu
pracuj±cego na systemach UNIX z pe³nym wsparciem dla nowoczesnych
protoko³ów routingu, ³atwym interfejsem konfiguracji i jêzykiem
filtrów o du¿ych mo¿liwo¶ciach.

%package ipv6
Summary:	Routing daemon for IPv6
Summary(pl):	Demon dynamicznego routingu IPv6
Group:		Networking/Daemons
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Provides:	routingdaemon
Provides:	bird-daemon
Obsoletes:	gated
Obsoletes:	mrt
Obsoletes:	zebra
Obsoletes:	zebra-guile
Requires:	%{name} = %{version}-%{release}

%description ipv6
The BIRD project is an attempt to create a routing daemon running on
UNIX-like systems (but not necessarily limited to them) with full
support of all modern routing protocols, easy to use configuration
interface and powerful route filtering language.

%description -l pl ipv6
Projekt BIRD ma na celu utworzenie daemona dynamicznego routingu
pracuj±cego na systemach UNIX z pe³nym wsparciem dla nowoczesnych
protoko³ów routingu, ³atwym interfejsem konfiguracji i jêzykiem
filtrów o du¿ych mo¿liwo¶ciach.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.* tools

%if %{with ipv6}
%{__autoconf}
%configure \
	--disable-memcheck \
	--enable-client \
	--enable-ipv6
%{__make}

mv bird bird-6

%{__make} clean
%endif

%if %{with ipv4}
%configure \
	--disable-memcheck \
	--enable-client \
	--disable-ipv6
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_sbindir}}

install birdc $RPM_BUILD_ROOT%{_sbindir}

%if %{with ipv6}
install bird $RPM_BUILD_ROOT%{_sbindir}
install doc/bird.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ipv4
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ipv4
%endif

%if %{with ipv6}
install bird-6 $RPM_BUILD_ROOT%{_sbindir}
cat <<EOF > $RPM_BUILD_ROOT%{_sbindir}/birdc-6
#!/bin/sh
exec %{_sbindir}/birdc -s /var/run/bird-6.ctl
EOF
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-ipv6
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/%{name}-ipv6
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post ipv4
/sbin/chkconfig --add %{name}-ipv4 >&2

if [ -f /var/lock/subsys/%{name}-ipv4 ]; then
	/etc/rc.d/init.d/%{name}-ipv4 restart >&2
else
	echo "Run '/etc/rc.d/init.d/%{name}-ipv4 start' to start routing deamon." >&2
fi

%preun ipv4
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name}-ipv4 ]; then
		/etc/rc.d/init.d/%{name}-ipv4 stop >&2
	fi
	/sbin/chkconfig --del %{name}-ipv4 >&2
fi

%post ipv6
/sbin/chkconfig --add %{name}-ipv6 >&2

if [ -f /var/lock/subsys/%{name}-ipv6 ]; then
	/etc/rc.d/init.d/%{name}-ipv6 restart >&2
else
	echo "Run '/etc/rc.d/init.d/%{name}-ipv6 start' to start routing deamon." >&2
fi

%preun ipv6
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name}-ipv6 ]; then
		/etc/rc.d/init.d/%{name}-ipv6 stop >&2
	fi
	/sbin/chkconfig --del %{name}-ipv6 >&2
fi

%files
%defattr(644,root,root,755)
%doc doc/*.html TODO README
%attr(755,root,root) %{_sbindir}/birdc

%if %{with ipv4}
%files ipv4
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/bird
%attr(754,root,root) /etc/rc.d/init.d/bird-ipv4
%attr(754,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/bird-ipv4
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bird.conf
%endif

%if %{with ipv6}
%files ipv6
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/bird-6
%attr(755,root,root) %{_sbindir}/birdc-6
%attr(754,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/bird-ipv6
%attr(754,root,root) %config(noreplace) %verify(not size mtime md5) /etc/rc.d/init.d/bird-ipv6
#%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/bird-6.conf
%endif
