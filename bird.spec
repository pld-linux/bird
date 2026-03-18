# Conditional build:
%bcond_without	libssh	# RPKI SSH transport support
#
Summary:	The BIRD Internet Routing Daemon
Summary(pl.UTF-8):	Demon BIRD Internetowego Routingu Dynamicznego
Name:		bird
Version:	3.2.0
Release:	1.1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	https://bird.nic.cz/download/%{name}-%{version}.tar.gz
# Source0-md5:	96c1da55667ca6c08b4d41ecfb871efc
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	https://bird.nic.cz/download/%{name}-doc-%{version}.tar.gz
# Source3-md5:	77fd807bdd8ff4369fe7653b5b6a7137
Source4:	%{name}.service
Source5:	%{name}.tmpfiles
Patch0:		%{name}-xbasename-const.patch
Patch1:		%{name}-krt-gr-export-fix.patch
URL:		https://bird.nic.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
%{?with_libssh:BuildRequires:	libssh-devel}
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 6.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/useradd
Provides:	bird-daemon
Provides:	group(bird)
Provides:	routingdaemon
Provides:	user(bird)
Obsoletes:	gated
Obsoletes:	mrt
Obsoletes:	zebra
Obsoletes:	zebra-guile
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The BIRD project is an attempt to create a routing daemon running on
UNIX-like systems (but not necessarily limited to them) with full
support of all modern routing protocols, easy to use configuration
interface and powerful route filtering language.

%description -l pl.UTF-8
Projekt BIRD ma na celu utworzenie daemona dynamicznego routingu
pracującego na systemach UNIX z pełnym wsparciem dla nowoczesnych
protokołów routingu, łatwym interfejsem konfiguracji i językiem
filtrów o dużych możliwościach.

%prep
%setup -q -a 3
%patch -P0 -p1
%patch -P1 -p1

%build
cp -f /usr/share/automake/config.* tools
%{__autoconf}

%configure \
	--runstatedir=/var/run/bird \
	--enable-client \
	%{?with_libssh:--enable-libssh}%{!?with_libssh:--disable-libssh}

%{__make} VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{_sbindir}} \
	$RPM_BUILD_ROOT{%{systemdunitdir},%{systemdtmpfilesdir}}

install bird $RPM_BUILD_ROOT%{_sbindir}
install birdc $RPM_BUILD_ROOT%{_sbindir}
install birdcl $RPM_BUILD_ROOT%{_sbindir}
install doc/bird.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
install %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 271 bird
%useradd -u 271 -d /usr/share/empty -s /bin/false -c "bird routing daemon" -g bird bird

%post
/sbin/chkconfig --add bird
%service bird restart "routing daemon"
%systemd_post bird.service

%preun
if [ "$1" = "0" ]; then
	%service bird stop
	/sbin/chkconfig --del bird
fi
%systemd_preun bird.service

%postun
if [ "$1" = "0" ]; then
	%userremove bird
	%groupremove bird
fi
%systemd_reload

%files
%defattr(644,root,root,755)
%doc doc/reply_codes ChangeLog NEWS README
%doc %{name}-doc-%{version}/doc/*.html
%doc %{name}-doc-%{version}/doc/*.pdf
%attr(755,root,root) %{_sbindir}/bird
%attr(755,root,root) %{_sbindir}/birdc
%attr(755,root,root) %{_sbindir}/birdcl
%attr(754,root,root) /etc/rc.d/init.d/bird
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/bird
%attr(640,root,bird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bird.conf
%{systemdunitdir}/bird.service
%{systemdtmpfilesdir}/bird.conf
