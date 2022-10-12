Name:           xcp-rrdd
Version:        1.33.0
Release:        6%{?dist}
Summary:        Statistics gathering daemon for the xapi toolstack
License:        LGPL
URL:            https://github.com/xapi-project/xcp-rrdd

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xcp-rrdd/archive?at=v1.33.0&format=tar.gz&prefix=xcp-rrdd-1.33.0#/xcp-rrdd-1.33.0.tar.gz
Source1: SOURCES/xcp-rrdd/xcp-rrdd.service
Source2: SOURCES/xcp-rrdd/xcp-rrdd-sysconfig
Source3: SOURCES/xcp-rrdd/xcp-rrdd-conf
Source4: SOURCES/xcp-rrdd/xcp-rrdd-tmp
Patch1: SOURCES/xcp-rrdd/0001-Reformat.patch
Patch2: SOURCES/xcp-rrdd/0002-http-svr-remove-slow-path.patch
Patch3: SOURCES/xcp-rrdd/0003-Limit-concurrent-connections-with-semaphore.patch


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xcp-rrdd/archive?at=v1.33.0&format=tar.gz&prefix=xcp-rrdd-1.33.0#/xcp-rrdd-1.33.0.tar.gz) = 9a6f6ef807813d22c6635d0ebfc6433e105b7463

BuildRequires:  xs-opam-repo
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-rrd-transport-devel
BuildRequires:  xen-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  xen-libs-devel
BuildRequires:  blktap-devel
BuildRequires:  systemd-devel
#Requires:       redhat-lsb-core

Requires:       libev
Requires(pre):  shadow-utils

%{?systemd_requires}


%description
Statistics gathering daemon for the xapi toolstack.

%prep
%autosetup -p1

%build
make

%check
make test

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
* Thu Sep 08 2022 Rob Hoes <rob.hoes@citrix.com> - 1.33.0-6
- CA-368579: Mitigations against DoS attacks by unauthenticated clients

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 1.33.0-5
- Bump package for libev dependency

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 1.33.0-4
- Bump package after xs-opam update

* Mon Sep 27 2021 Pau Ruiz Safont <pau.safont@citrix.com> - 1.33.0-3
- Bump packages after ocaml-xen-api-libs-transitional update

* Tue Jul 13 2021 Edwin Török <edvin.torok@citrix.com> - 1.33.0-2
- bump packages after xs-opam update

* Fri May 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.33.0-1
- CA-335964: Do not expose temporary VM UUIDs

* Tue May 19 2020 Christian Lindig <christian.lindig@citrix.com> - 1.32.0-1
- maintenace: prepare for ocamlformat
- maintenance: format code with ocamlformat
- maintenance: format comments with ocamlformat

* Mon May 04 2020 Christian Lindig <christian.lindig@citrix.com> - 1.31.0-1
- CA-338809: Update information for running VMs, not paused ones

* Wed Apr 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.30.0-1
- CA-335964: Prepare code for hiding temporary uuids
- CA-335964: Actively mask temporary VM UUIDs from exposed metrics

* Fri Mar 27 2020 Christian Lindig <christian.lindig@citrix.com> - 1.29.0-1
- fix build -- use OASIS
- Add opam file
- rrddump: Update for stdext 2.0.0
- Move text_export from xapi-rrd-unix
- Port to jbuilder
- Ported from jbuilder to dune and updated dependencies.
- Do not use 'finally' from package xapi-stdext-pervasives.
- maintenance: rrddump pointing at incorrect repo
- Fix after rrddump merge
- maintenance: normalize opam files

* Thu Mar 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.28.0-1
- CP-33121: stop using stdext's std and monadic modules
- stats: use standard Mutex.execute
- xcp_rrdd: Do not include modules into the namespace

* Fri Mar 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.27.0-1
- rrdd_server: document add functions
- travis: use xs-opam config by default

* Tue Dec 17 2019 Christian Lindig <christian.lindig@citrix.com> - 1.26.0-1
- CA-325582 fix bug with query_possible_dss

* Fri Nov 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.25.0-1
- CA-325582: remove SR RRDs from memory after archiving
- CA-325582: always remove VM RRDs from memory even if archiving failed
- CA-325582: Report disabled sources

* Wed Sep 18 2019 Christian Lindig <christian.lindig@citrix.com> - 1.24.0-1
- CA-327028: Cleanup function for calculating per-cpu usage
- CA-327028: Work around a incorrect values of vcputime

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 1.23.0-2
- bump packages after xs-opam update

* Mon Aug 12 2019 Christian Lindig <christian.lindig@citrix.com> - 1.23.0-1
- Drop rpc dependency
- use more granular dependencies

* Mon Jul 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.22.0-1
- CA-322045: log skipped plugins outside of the lock at debug level
- CA-322045: skip /dev/shm/metrics/tap-

* Tue Jul 23 2019 Rob Hoes <rob.hoes@citrix.com> - 1.21.0-1
- CA-322045: Enable fastpath for xcp-rrdd http server

* Mon Jul 01 2019 Christian Lindig <christian.lindig@citrix.com> - 1.20.0-1
- maintenance: remove unused files from the root
- maintenance: remove INSTALL

* Tue May 14 2019 Christian Lindig <christian.lindig@citrix.com> - 1.19.0-1
- CP-30614 Eliminate xapi's dependency on libxenctrl
- CP-315465: pre-allocate enough pages for mem_vm writer

* Thu May 02 2019 Christian Lindig <christian.lindig@citrix.com> - 1.18.0-1
- Revert merge psafont/CP-30614

* Mon Apr 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.17.0-1
- XSI-283 add GC logging

* Wed Mar 20 2019 Christian Lindig <christian.lindig@citrix.com> - 1.16.0-1
- CP-30614: decouple stats generation from consolidation
- CP-30614: Do not register self-written files
- CP-30614: Incorporate RRD filewriters
- CP-30614: prefix files for easier identification
- CP-30614: Prepare for file-writing stats within the monitor loop
- CP-30614: Rename written DSS files
- CP-30614: Write files for memory stats


* Thu Mar 14 2019 Christian Lindig <christian.lindig@citrix.com> - 1.15.0-1
- Fix: Masking real dss with fake ones doesn't supress all of them
- maintenance: remove fake modules

* Wed Jan 23 2019 Christian Lindig <christian.lindig@citrix.com> - 1.14.0-1
- Prepare for Dune 1.6
- Update Travis configuration
- Add ezxenstore dependency to opam

* Fri Jan 11 2019 Christian Lindig <christian.lindig@citrix.com> - 1.13.0-1
- Use xapi-rrd; rrd is being deprecated.

* Tue Dec 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.12.0-1
- Moved from jbuilder to dune and deprecated xxp in favour of xapi-idl.

* Fri Nov 16 2018 Christian Lindig <christian.lindig@citrix.com> - 1.11.0-1
- New ocaml-rpc

* Fri Aug 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.10.0-1
- Simplify PPX processing in jbuild file

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

