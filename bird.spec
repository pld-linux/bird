Summary:	Routing daemon
Summary(pl):	Daemon dynamicznego routingu
Name:		bird
Version:	1.0.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://bird.network.cz/pub/bird/%{name}-%{version}.tar.gz
Source1:	ftp://bird.network.cz/pub/bird/%{name}-doc-%{version}.tar.gz
Source2:	%{name}.init
URL:		http://bird.network.cz/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q -a 1

%build
%configure \
	--disable-memcheck \
	--enable-client \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_sbindir}

install bird			$RPM_BUILD_ROOT%{_sbindir}
install birdc			$RPM_BUILD_ROOT%{_sbindir}
install doc/bird.conf.example	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE2}		$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%post
/sbin/chkconfig --add %{name} >&2

if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run '/etc/rc.d/init.d/%{name} start' to start routing deamon." >&2
fi
    
%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
        /sbin/chkconfig --del %{name} >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.html %{name}-doc-%{version}/doc/*.ps TODO README

%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
