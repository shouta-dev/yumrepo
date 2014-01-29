Name:           rubygems
Summary:        the Ruby standard for publishing and managing third party libraries
Version:        1.3.1
Release:        5.rhel5
License:        Ruby
Group:          Development/Libraries
URL:            http://rubyforge.org/projects/rubygems/
Source0:        http://rubyforge.org/frs/download.php/45905/rubygems-1.3.1.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ruby        >= 1.8.7
Requires:       ruby        >= 1.8.7

%description
RubyGems is the Ruby standard for publishing and managing third party libraries.

%prep
%setup -q

%install
%ifarch x86_64 ppc64
  %define _libdir           /usr/lib
  %define _localstatedir    /var
  %define _sysconfdir       /etc
%endif
rm -rf %{buildroot}
export GEM_HOME=%{buildroot}%{_libdir}/ruby/gems/1.8
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-O[1-9]/-O3/g'`
ruby setup.rb config --destdir=%{buildroot}/usr
ruby setup.rb setup
ruby setup.rb install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_libdir}/ruby/site_ruby/1.8/rbconfig
%{_libdir}/ruby/site_ruby/1.8/rubygems
%{_libdir}/ruby/site_ruby/1.8/*.rb
%dir %{_libdir}/ruby/gems
%dir %{_libdir}/ruby/gems/1.8
%dir %{_libdir}/ruby/gems/1.8/cache
%dir %{_libdir}/ruby/gems/1.8/doc
%dir %{_libdir}/ruby/gems/1.8/gems
%dir %{_libdir}/ruby/gems/1.8/specifications
%{_libdir}/ruby/gems/1.8/doc/*

%changelog
* Fri Jul 30 2010 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile with optimization level3

* Fri Sep 04 2009 uta <uta.2009@gmail.com>
- initial release
