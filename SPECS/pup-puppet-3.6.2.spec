%define _prefix /opt/puppet
%define _rubybin /opt/puppet/bin/ruby
%define _defaultdocdir %{_prefix}/doc
%define tarballname puppet

%{!?ruby_sitelibdir: %global ruby_sitelibdir %(%{_rubybin} -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')}
%global confdir conf/redhat


Name:           pup-puppet
Version:        3.6.2
Release:        2
Summary:        A network tool for managing many disparate systems
License:        ASL 2.0
URL:            http://puppetlabs.com
Source0:        %{tarballname}/%{tarballname}-3.6.2.tar.gz
Group:          System Environment/Base
BuildRoot:      %{_tmppath}/%{tarballname}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       pup-ruby-local >= 2.0.0
Requires:       pup-facter-local >= 1.7.2
Provides:       pup-puppet-local
Patch0:         pup-puppet-3.2.4-aix-init.patch
Patch1:         pup-puppet-3.6.2-no-hiera.patch


%description
Puppet lets you centrally manage every important aspect of your system using a
cross-platform specification language that manages all the separate elements
normally aggregated in different files, like users, cron jobs, and hosts,
along with obviously discrete elements like packages, services, and files.

%prep
# %setup -q -n %{tarballname}-3.6.2
umask 022
cd /opt/freeware/src/packages/BUILD
rm -rf puppet-3.6.2
/bin/gzip -dc /opt/freeware/src/packages/SOURCES/%{tarballname}-3.6.2.tar.gz | gtar -xf -
cd /opt/freeware/src/packages/BUILD/puppet-3.6.2
/bin/chown -Rhf root .
/bin/chgrp -Rhf system .
/bin/chmod -Rf a+rX,g-w,o-w .

%patch0
%patch1

%build

%install
rm -rf %{buildroot}
cd /opt/freeware/src/packages/BUILD/puppet-3.6.2
%{_rubybin} install.rb --destdir=%{buildroot} --quick

mkdir -p %{buildroot}/etc/puppet
cat<<"EOF" > %{buildroot}/etc/puppet/puppet.conf
[main]
    logdir = /var/log/puppet
    rundir = /var/run/puppet
    ssldir = $vardir/ssl
    splay  = true

[agent]
    classfile = $vardir/classes.txt
    localconfig = $vardir/localconfig
    server = puppet.eb.lan.at
    report = true
EOF

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
mkdir -p /var/lib/puppet
mkdir -p /var/log/puppet

%files
%defattr(-, root, root, 0755)
%config(noreplace) /etc/puppet/puppet.conf
%config(noreplace) /etc/puppet/auth.conf
/opt/puppet


%changelog
* Wed Jul 16 2014 Toni Schmidbauer <toni@stderr.at> - 3.6.2-2
- Removed release postfix, otherwise package is not upgradable
- fixed overwriting of config files
* Wed Jul 16 2014 Toni Schmidbauer <toni@stderr.at> - 3.6.2-1.local
- Added Klausis AIX init patch
* Wed Mar 12 2014 Toni Schmidbauer <toni@stderr.at> - 3.2.4-2.local
- Added Klausis AIX init patch
* Tue Aug 28 2013 Toni Schmidbauer <toni@stderr.at> - 3.2.4-1.local
- Puppet version 3.2.4
* Tue Mar 13 2013 Toni Schmidbauer <toni@stderr.at> - 3.1.1-1.local
- Puppet version 3.1.1 + patches
* Tue Mar 11 2013 Toni Schmidbauer <toni@stderr.at> - 3.1.0-1.local
- Puppet version 3.1.0 + patches
* Tue Jan 15 2013 Toni Schmidbauer <toni@stderr.at> - 3.0.2-1.local
- Puppet version 3.0.2
* Mon Dec 19 2011 Nick Bausch <nick.bausch@gmail.com> - 2.7.6-1.local
- First puppet-local build for AIX
