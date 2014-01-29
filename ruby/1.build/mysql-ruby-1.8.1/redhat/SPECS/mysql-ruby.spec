Name:           mysql-ruby
Summary:        A Ruby interface to MySQL
Version:        2.8.1
Release:        5.rhel5
License:        Ruby
Group:          Development/Libraries
URL:            http://rubyforge.org/projects/mysql-ruby/
Source0:        http://rubyforge.org/frs/download.php/51087/mysql-ruby-2.8.1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  mysql-devel
BuildRequires:  ruby        >= 1.8.7
Requires:       ruby        >= 1.8.7

%description
This is the MySQL API module for Ruby. It provides the same functions for
Ruby programs that the MySQL C API provides for C programs.

%prep
%setup -q

%build
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-O[1-9]/-O3/g'`
ruby extconf.rb --with-mysql-config
make %{?_smp_mflags}

%install
%ifarch x86_64 ppc64
  %define _libdir           /usr/lib
  %define _localstatedir    /var
  %define _sysconfdir       /etc
%endif
rm -rf %{buildroot}
env DESTDIR=%{buildroot} make install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING COPYING.ja 
%{_libdir}/ruby/site_ruby/1.8/*/mysql.so

%changelog
* Fri Jul 30 2010 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile with optimization level3

* Fri Sep 18 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile for RHEL 5.4

* Fri Sep 04 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- initial release
