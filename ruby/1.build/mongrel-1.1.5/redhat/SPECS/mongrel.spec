Name:           mongrel
Summary:        A small fast HTTP server written in (mostly) Ruby.
Version:        1.1.5
Release:        5.rhel5
License:        Ruby's
Group:          Development/Libraries
URL:            http://mongrel.rubyforge.org/
Source0:        http://rubyforge.org/frs/download.php/37321/mongrel-1.1.5.gem
Source1:        mongrel.init
Source2:        mongrel.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ruby                    >= 1.8.7
BuildRequires:  rubygems                >= 1.3.1
Requires:       ruby                    >= 1.8.7
Requires:       rubygems                >= 1.3.1
Requires:       rake                    >= 0.8.3
Requires:       gem_plugin              >= 0.2.3
Requires:       daemons                 >= 1.0.10
Requires:       fastthread              >= 1.0.1
Requires:       cgi_multipart_eof_fix   >= 2.5.0
Requires:       mongrel_cluster         >= 1.0.5

%description
A small fast HTTP server written in (mostly) Ruby that can be used to host web frameworks directly
with HTTP rather than FastCGI or SCGI.

%prep
cp $RPM_SOURCE_DIR/%{name}-%{version}.gem $RPM_BUILD_DIR/

%install
%ifarch x86_64 ppc64
  %define _libdir           /usr/lib
  %define _localstatedir    /var
  %define _sysconfdir       /etc
%endif
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/ruby/gems/1.8
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-O[1-9]/-O3/g'`
gem install --local --force --install-dir %{buildroot}/usr %{name}
mv %{buildroot}/usr/{cache,doc,gems,specifications} %{buildroot}%{_libdir}/ruby/gems/1.8/
mkdir -p %{buildroot}%{_sysconfdir}/mongrel
chmod 700 %{buildroot}%{_sysconfdir}/mongrel
install -m600 $RPM_SOURCE_DIR/mongrel.conf %{buildroot}%{_sysconfdir}/mongrel/
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m700 $RPM_SOURCE_DIR/mongrel.init %{buildroot}%{_sysconfdir}/rc.d/init.d/mongrel_rubricks

%clean
rm -rf %{buildroot}

%pre
# pre first installation
if [ $1 -eq 1 ] ; then
  mkdir %{_localstatedir}/mongrel 2>/dev/null
  groupadd -g 82 mongrel
  useradd -u 82 -g 82 -s /sbin/nologin -d %{_localstatedir}/mongrel -m -k /dev/null mongrel 2>/dev/null
  chown mongrel.mongrel %{_localstatedir}/mongrel
  chmod 700 %{_localstatedir}/mongrel
fi

%post
# post first installation
if [ $1 -eq 1 ] ; then
  chkconfig --add mongrel_rubricks
  mkdir -p /var/log/mongrel 2>/dev/null
  chown mongrel.mongrel /var/log/mongrel
  chmod 700 /var/log/mongrel
fi

%preun
# pre uninstallation
if [ $1 -eq 0 ] ; then
  if [ -x %{_sysconfdir}/rc.d/init.d/mongrel_rubricks ]; then
    %{_sysconfdir}/rc.d/init.d/mongrel_rubricks stop > /dev/null 2>&1
    chkconfig --del mongrel_rubricks 2>/dev/null
  fi
fi

%postun
# post uninstallation
if [ $1 -eq 0 ] ; then
  chown root.root /var/log/mongrel 2>/dev/null
  rm -rf %{_localstatedir}/mongrel/*
  userdel -r mongrel 2>/dev/null
  rm -rf /var/log/mongrel
fi

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/ruby/gems/1.8/cache/*
%{_libdir}/ruby/gems/1.8/doc/*
%{_libdir}/ruby/gems/1.8/gems/*
%{_libdir}/ruby/gems/1.8/specifications/*
%{_sysconfdir}/rc.d/init.d/mongrel_rubricks
%dir %{_sysconfdir}/mongrel
%config(noreplace) %{_sysconfdir}/mongrel/mongrel.conf

%changelog
* Fri Jul 30 2010 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile with optimization level3

* Fri Sep 18 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile for RHEL 5.4

* Fri Sep 04 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- initial release
