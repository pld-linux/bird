Summary:	Routing daemon
Summary(pl):	Demon dynamicznego routingu
Name:		bird
Version:	1.0.6
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://bird.network.cz/pub/bird/%{name}-%{version}.tar.gz
# Source0-md5	e21533bf0223c3a1fd2b984a5952fd45
Source1:	ftp://bird.network.cz/pub/bird/%{name}-doc-%{version}.tar.gz
# Source1-md5	a8fb98281a918a725ded174c3f9655a3
Source2:	%{name}.init
URL:		http://bird.network.cz/
BuildRequires:	readline-devel >= 4.2
Prereq:		/sbin/chkconfig
Provides:	routingdaemon
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

%prep
%setup -q -a 1

%build
%configure2_13 \
	--disable-memcheck \
	--enable-client \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}

install bird $RPM_BUILD_ROOT%{_sbindir}
install birdc $RPM_BUILD_ROOT%{_sbindir}

install doc/bird.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%doc doc/*.html %{name}-doc-*/doc/*.ps TODO README

%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.conf
