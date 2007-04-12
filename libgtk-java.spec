Name:           libgtk-java
Version:        2.10.2
Release:        %mkrel 2
Epoch:          0
Summary:        Java bindings for GTK+
License:        LGPL
Group:          Development/Java
URL:            http://java-gnome.sourceforge.net/
Source0:        http://fr2.rpmfind.net/linux/gnome.org/sources/libgtk-java/2.10/libgtk-java-%{version}.tar.bz2
Source1:        libgtk-java-2.10.2.md5sum
Source2:        libgtk-java-2.10.2.news
Source3:        java-gnome-macros.tar.bz2
BuildRequires:  cairo-java >= 0:1.0.6
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       gtk2
Requires:       glib-java
Requires:       cairo-java
Requires:       libgtk+2.0-devel
BuildRequires:  cairo-java >= 0:1.0.8
BuildRequires:  docbook-utils
BuildRequires:  docbook-dtd31-sgml
BuildRequires:  gcc-java >= 0:4.0.1
BuildRequires:  glib-java >= 0:0.4.2
BuildRequires:  java-devel >= 0:1.4.2
BuildRequires:  jpackage-utils
BuildRequires:  libgtk+2.0-devel

%description
libgtk-java is a language binding that allows developers to write GTK
applications in Java.  It is part of Java-GNOME.

%package        devel
Summary:        Compressed Java source files for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description    devel
Compressed Java source for %{name}. This is useful if you are developing
applications with IDEs like Eclipse.

%prep
%setup -q
%setup -q -T -D -a 3
%{__aclocal} -I macros --force
%{__autoconf} --force
%{__automake} --copy --force-missing
%{__libtoolize} --copy --force

%build
export CLASSPATH=
export JAVA=%{java}
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
%{configure2_5x} --with-jardir=%{_javadir}
%{make}

# pack up the java source
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
zipfile=$PWD/$jarname$jarversion-src-%{version}.zip
pushd src/java
%{_bindir}/zip -9 -r $zipfile $(find -name \*.java)
popd

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

%{__mkdir_p} %{buildroot}%{_datadir}/%{name}/macros
%{__mv} %{buildroot}/%{name}/macros/*.m4 %{buildroot}%{_datadir}/%{name}/macros
%{__rm} -rf %{buildroot}/%{name}
%{__rm} -rf %{buildroot}/%{name}-%{version}

# install the src.zip and make a sym link
jarversion=$(echo -n %{version} | cut -d . -f -2)
jarname=$(echo -n %{name} | cut -d - -f 1 | sed "s/lib//")
%{__install} -m 644 $jarname$jarversion-src-%{version}.zip $RPM_BUILD_ROOT%{_javadir}/
pushd %{buildroot}%{_javadir}
%{__ln_s} $jarname$jarversion-src-%{version}.zip $jarname$jarversion-src.zip
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/api AUTHORS COPYING doc/examples doc/FAQ.html NEWS README THANKS
%{_libdir}/*so*
%{_libdir}/*la
%{_libdir}/pkgconfig/*
%dir %{_includedir}/libgtk-java
%{_includedir}/libgtk-java/*
%{_javadir}/*.jar
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/macros
%{_datadir}/%{name}/macros/*.m4

%files devel
%defattr(-,root,root)
%{_javadir}/*.zip


