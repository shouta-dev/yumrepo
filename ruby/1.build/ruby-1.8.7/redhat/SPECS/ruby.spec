Name:           ruby
Summary:        the interpreted scripting language for quick and easy object-oriented programming
Version:        1.8.7
Release:        7.rhel5
License:        GPL
Group:          Development/Languages
URL:            http://www.ruby-lang.org/
Source0:        ftp://ftp.ruby-lang.org/pub/ruby/1.8/ruby-1.8.7-p72.tar.gz
Patch0:         bignum.patch
Patch1:         nkf.patch
Patch2:         ruby-1.8.7-p72-mbari1.patch
Patch3:         ruby-1.8.7-p72-mbari2.patch
Patch4:         ruby-1.8.7-p72-mbari3.patch
Patch5:         ruby-1.8.7-p72-mbari4.patch
Patch6:         ruby-1.8.7-p72-mbari5.patch
Patch7:         ruby-1.8.7-p72-mbari6.patch
Patch8:         ruby-1.8.7-p72-mbari7.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  zlib-devel

%description
Ruby is the interpreted scripting language for quick and easy object-oriented programming.
It has many features to process text files and to do system management tasks (as in Perl).
It is simple, straight-forward, extensible, and portable.

%prep
%setup -q -n ruby-1.8.7-p72
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%ifarch x86_64 ppc64
  %define _site_libdir      /usr/lib
  %define _libdir           /usr/lib
  %define _localstatedir    /var
  %define _sysconfdir       /etc
%endif
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's/-O[1-9]/-O3/g'`
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-stack-protector"
export CXXFLAGS="$RPM_OPT_FLAGS -Wall -fno-stack-protector"
export XCFLAGS="$RPM_OPT_FLAGS -Wall -fno-stack-protector"
%configure --enable-shared --enable-pthread --disable-ucontext --enable-ssl --with-ssl --with-openssl --with-readline
cp    Makefile Makefile.spec.bk
cat   Makefile.spec.bk | sed 's/optflags = -O2/optflags = -O3/g' > Makefile
rm -f Makefile.spec.bk
make RUBY_INSTALL_NAME=ruby %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root)
%doc COPYING README
%{_bindir}/*
%{_libdir}/lib*
%{_libdir}/ruby
%{_mandir}/man1/*

%changelog
* Fri Jul 30 2010 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile with optimization level3

* Thu Sep 24 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- revert nkf from 2.0.8 to 2.0.7

* Fri Sep 18 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- re-compile for RHEL 5.4

* Fri Sep 04 2009 Yuta Kiriyama <y-kiriyama@asteriks.co.jp>
- initial release
