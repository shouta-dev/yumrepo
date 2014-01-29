Name:           fastthread
Summary:        Ruby library which provides a faster C implementation of thread.rb.
Version:        1.0.1
Release:        5.rhel5
License:        Ruby's
Group:          Development/Libraries
URL:            http://rubyforge.org/projects/mongrel/
Source:         http://rubyforge.org/frs/download.php/27042/fastthread-1.0.1.gem
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ruby        >= 1.8.7
BuildRequires:  rubygems    >= 1.3.1
Requires:       ruby        >= 1.8.7
Requires:       rubygems    >= 1.3.1

%description
fastthread is a Ruby library which provides a faster (and non-memory-leaking)
C implementation of the concurrency primitives from stdlib's thread.rb.

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/ruby/gems/1.8/cache/*
%{_libdir}/ruby/gems/1.8/doc/*
%{_libdir}/ruby/gems/1.8/gems/*
%{_libdir}/ruby/gems/1.8/specifications/*

%changelog
* Fri Jul 30 2010 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile with optimization level3

* Fri Sep 18 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile for RHEL 5.4

* Fri Sep 04 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- initial release