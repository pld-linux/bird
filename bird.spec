Summary:	Routing daemon
Summary(pl):	Demon dynamicznego routingu
Name:		bird
Version:	1.0.9
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://bird.network.cz/pub/bird/%{name}-%{version}.tar.gz
# Source0-md5:	6a1d94b8a33b80e754ea4f9cc0ac1ff3
Source1:	ftp://bird.network.cz/pub/bird/%{name}-doc-%{version}.tar.gz
# Source1-md5:	a65161e37449da5303cbe454125c3c9c
Source2:	%{name}.init
Patch0:		%{name}-posix.patch
Patch1:		%{name}-flex.patch
URL:		http://bird.network.cz/
BuildRequires:	automake
BuildRequires:	readline-devel >= 4.2
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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
pracuj�cego na systemach UNIX z pe�nym wsparciem dla nowoczesnych
protoko��w routingu, �atwym interfejsem konfiguracji i j�zykiem
filtr�w o du�ych mo�liwo�ciach.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.* tools
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
