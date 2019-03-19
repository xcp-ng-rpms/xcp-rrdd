Name:           xcp-rrdd
Version:        1.9.0
Release:        4%{?dist}
Summary:        Statistics gathering daemon for the xapi toolstack
License:        LGPL
URL:            https://github.com/xapi-project/xcp-rrdd
Source0:        https://code.citrite.net/rest/archive/latest/projects/XSU/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xcp-rrdd/archive?at=v1.9.0&format=tar.gz&prefix=xcp-rrdd-1.9.0#/xcp-rrdd-1.9.0.tar.gz) = 4b2158731be2218d50c8005c01b668ea2b17c6f9
Source1:        xcp-rrdd.service
Source2:        xcp-rrdd-sysconfig
Source3:        xcp-rrdd-conf
Source4:        xcp-rrdd-tmp
BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-xenops-devel
BuildRequires:  ocaml-rrd-transport-devel
BuildRequires:  xen-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  xen-libs-devel
BuildRequires:  blktap-devel
BuildRequires:  systemd-devel
#Requires:       redhat-lsb-core
Requires(pre):  shadow-utils

%{?systemd_requires}

%description
Statistics gathering daemon for the xapi toolstack.

%prep
%autosetup -p1

%build
make

%pre
getent group rrdmetrics >/dev/null || groupadd -r rrdmetrics

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_tmpfilesdir}
make install DESTDIR=%{buildroot} SBINDIR=%{_sbindir}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xcp-rrdd
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xcp-rrdd.conf
%{__install} -D -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%files
%doc README.markdown LICENSE
%{_sbindir}/xcp-rrdd
%{_unitdir}/xcp-rrdd.service
%config(noreplace) %{_sysconfdir}/sysconfig/xcp-rrdd
%config(noreplace) %{_sysconfdir}/xcp-rrdd.conf
%{_tmpfilesdir}/%{name}.conf

%post
%systemd_post xcp-rrdd.service
%tmpfiles_create %{_tmpfilesdir}/%{name}.conf

%preun
%systemd_preun xcp-rrdd.service

%postun
%systemd_postun xcp-rrdd.service

%changelog
* Tue May 29 2018 Christian Lindig <christian.lindig@citrix.com> - 1.9.0-1
- rrdd: update interface for fd-send-recv >= 2.0.0
- opam: update dependencies bound

* Thu May 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.8.0-1
- rrdd: make safe-strings compliant

* Thu May 10 2018 Christian Lindig <christian.lindig@citrix.com> - 1.7.0-1
- CP-26583: Update error handling to use PPX-based IDL
- CP-26583: Update RRDD Server and Client references to use PPX IDL
- CP-26583: Define server-impl RPC bindings for API calls
- CP-26583: Match API call signatures to RPC bindings
- CP-26583: Update API calls in RRDD to use new signatures
- CP-26583: ocp-indent xcp-rrdd

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.6.0-1
- CA-277850 Replace xenops library with ezxenstore

* Fri Feb 02 2018 Christian Lindig <christian.lindig@citrix.com> - 1.5.0-1
- CA-277850 increase loglevel to info for memfree
- CA-277850 add more logging (temporarily)

* Mon Dec 18 2017 Christian Lindig <christian.lindig@citrix.com> - 1.4.0-1
- Port to jbuilder
- Use new xapi-stdext structure
- Reduce use of stringext to minimum and do not open it on toplevel
- Update opam and jbuild files
- Remove unnecessary coverage function
- Use Astring in place of (X)stringext
- rrdd_stats: rough port oclock -> mtime
- Makefile: move install/remove logic from spec to Makefile
- xcp-rrdd: make reindent

* Thu May 18 2017 Rob Hoes <rob.hoes@citrix.com> - 1.3.0-1
- Remove camlp4 dependency, port to ppx
- Backport xs-opam opam file and update dependencies

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 1.2.1-3
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 1.2.1-2
- CA-243676: Do not restart toolstack services on RPM upgrade

* Mon Dec 19 2016 Rob Hoes <rob.hoes@citrix.com> - 1.2.1-1
- Fix mutex-related undefined behaviour

* Thu Oct 06 2016 Christian Lindig <christian.lindig@citrix.com> - 1.2.0-1
- create group rrdmetrics at installation for plugins to use
- create /dev/shm/metrics on startup using tmpfiles.d service

* Mon Aug 22 2016 Christian Lindig <christian.lindig@citrix.com> - 1.1.0-1
- update to 1.1.0
- xcp-rrdd implements a new mechanism to discover plugins
- new build requirement: ocaml-inotify-devel

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 1.0.1-2
- Package for systemd

* Mon Jul 25 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.0.1-1
- Update to 1.0.1

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-2
- Re-run chkconfig on upgrade

* Wed Apr 27 2016 Euan Harris <euan.harris@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.7-2
- Remove xen-missing-headers dependency 

* Wed Jun 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.7-1
- Update to 0.9.7
- Create new subpackage for the devel libraries now installed

* Fri May  9 2014 David Scott <dave.scott@citrix.com> - 0.9.5-1
- Update to 0.9.5, now will start without xen

* Sat Apr 26 2014 David Scott <dave.scott@eu.citrix.com> - 0.9.4-1
- Update to 0.9.4, now depends on rrdd-transport

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.2-1
- Update to 0.9.2

* Tue Sep 10 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.1

* Tue Jun 18 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

