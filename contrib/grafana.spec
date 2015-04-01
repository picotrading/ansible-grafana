%define my_version 2.0.0
%define my_release beta1
%define pkg_version %{my_version}_%{my_release}
%define tag_version %{my_version}-%{my_release}
%define tag v%{tag_version}


Name:           grafana
Summary:        Metrics dashboard and graph editor
Version:        %{pkg_version}
Release:        1%{?dist}
License:        Apache 2.0
URL:            http://grafana.org
Source:         https://github.com/%{name}/%{name}/archive/%{tag}.tar.gz
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
Source1:        grafana.service
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  git
BuildRequires:  golang
BuildRequires:  npm
BuildRequires:  nodejs-grunt-cli


%description
An open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -T -c -D


%build
export GOPATH=%{_builddir}/%{name}-%{version}/go
export NPM_CONFIG_CACHE=%{_builddir}/%{name}-%{version}/npm

if [ ! -e $GOPATH/src/github.com/%{name}/%{name}/%{name} ]; then
    go get -v -tags %{tag} github.com/%{name}/%{name} || true

    cd $GOPATH/src/github.com/%{name}/%{name}
    git checkout %{tag}

    # Build the backend
    go run build.go setup
    $GOPATH/bin/godep restore
    go build .
fi

if [ ! -e $GOPATH/src/github.com/%{name}/%{name}/dist/%{name}-%{tag_version}.%{_arch}.tar.gz ]; then
    cd $GOPATH/src/github.com/%{name}/%{name}

    # Build the frontend
    npm install
    grunt release
fi


%install
[ "%{buildroot}" != / ] && %{__rm} -rf "%{buildroot}"

cd %{_builddir}/%{name}-%{version}/go/src/github.com/%{name}/%{name}

# Move the frontend files
%{__mkdir_p} %{buildroot}%{_datarootdir}
%{__tar} -xzf dist/%{name}-%{tag_version}.%{_arch}.tar.gz -C %{buildroot}%{_datarootdir}
%{__mv} %{buildroot}%{_datarootdir}/%{name}-%{tag_version} %{buildroot}%{_datarootdir}/%{name}

# Move the init.d script
%{__mkdir_p} %{buildroot}/%{_initddir}
install -m 0755 %{buildroot}%{_datarootdir}/%{name}/scripts/init.sh %{buildroot}/%{_initddir}/%{name}
%{__rm} -fr %{buildroot}%{_datarootdir}/%{name}/scripts

# Move the main config
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__mv} %{buildroot}%{_datarootdir}/%{name}/conf/sample.ini %{buildroot}%{_sysconfdir}/%{name}/%{name}.ini

# Move doc files
%{__mv} %{buildroot}%{_datarootdir}/%{name}/{LICENSE,NOTICE,README}.md %{_builddir}/%{name}-%{version}

# Copy the executable file
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} ./%{name} %{buildroot}%{_bindir}

%if 0%{?rhel} > 6 || 0%{?fedora} > 15
# Copy the systemd script
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__cp} %{SOURCE1} %{buildroot}%{_unitdir}
%endif

# Modify the config file
%{__sed} -i 's,/opt/%{name}/data/%{name}.db,%{_sharedstatedir}/%{name}/%{name}.db,' %{buildroot}%{_sysconfdir}/%{name}/%{name}.ini

# Modify the init.d file
%{__sed} -i 's,/opt/%{name}/current/%{name},%{_bindir}/%{name},g' %{buildroot}%{_initddir}/%{name}
%{__sed} -i 's,/opt/%{name}/current,%{_datarootdir}/%{name},g' %{buildroot}%{_initddir}/%{name}

# Create the log directory
%{__mkdir_p} %{buildroot}%{_var}/log/%{name}

# Create the DB directory
%{__mkdir_p} %{buildroot}%{_sharedstatedir}/%{name}

# Create data directory
%{__mkdir_p} %{buildroot}%{_datarootdir}/%{name}/data


%post
# Create new user
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -m -s /sbin/nologin %{name}

# Change permissions on log, DB and data directory
%{__chown} %{name}:%{name} %{_var}/log/%{name} %{_sharedstatedir}/%{name} %{_datarootdir}/%{name}/data


%clean
[ "%{buildroot}" != / ] && %{__rm} -rf "%{buildroot}"


%files
%defattr(-,root,root,-)
%doc LICENSE.md NOTICE.md README.md
%{_bindir}/%{name}
%config %{_sysconfdir}/%{name}
%{_initddir}/%{name}
%{_var}/log/%{name}
%{_datarootdir}/%{name}
%{_sharedstatedir}/%{name}
%if 0%{?rhel} > 6 || 0%{?fedora} > 15
%{_unitdir}/%{name}.service
%endif


%changelog
* Wed Apr 1 2015 Jiri Tyr <jiri.tyr at gmail.com>
- Modifications necessary to build Grafana v2.0.0_beta1.

* Tue Dec 16 2014 Jiri Tyr <jiri.tyr at gmail.com>
- First build.
