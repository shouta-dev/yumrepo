Name:           repcached
Summary:        the memcached which implemented multi master asynchronous replication feature
Version:        2.2
Release:        1.rhel5
License:        BSD License
Group:          Applications/Services
URL:            http://sourceforge.net/projects/repcached/
Source0:        http://downloads.sourceforge.net/repcached/memcached-1.2.6-repcached-2.2.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires:       libevent
BuildRequires:  libevent-devel

%description
repcached is memcached which implemented multi master asynchronous replication feature.

%prep
%setup -q -n memcached-1.2.6-repcached-2.2

%build
%configure --enable-shared --enable-replication
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m644 $RPM_SOURCE_DIR/memcached.conf %{buildroot}%{_sysconfdir}/memcached.conf
install -m700 $RPM_SOURCE_DIR/memcached.init %{buildroot}%{_sysconfdir}/rc.d/init.d/memcached

%clean
rm -rf %{buildroot}

%pre
# pre first installation
if [ $1 -eq 1 ] ; then
  groupadd -g 84 memcached
  useradd -u 84 -g 84 -s /sbin/nologin -d / -m -k /dev/null memcached 2>/dev/null
fi

%post
# post first installation
if [ $1 -eq 1 ] ; then
  chkconfig --add memcached
fi

%preun
# pre uninstallation
if [ $1 -eq 0 ] ; then
  if [ -x %{_sysconfdir}/rc.d/init.d/memcached ]; then
    %{_sysconfdir}/rc.d/init.d/memcached stop > /dev/null 2>&1
    chkconfig --del memcached 2>/dev/null
  fi
fi

%postun
# post uninstallation
if [ $1 -eq 0 ] ; then
  userdel memcached 2>/dev/null
fi

%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/*
%{_mandir}/man1/*
%{_sysconfdir}/rc.d/init.d/memcached
%config(noreplace) %{_sysconfdir}/memcached.conf

%changelog
* Fri Sep 04 2009 uta <uta.2009@gmail.com>
- initial release
