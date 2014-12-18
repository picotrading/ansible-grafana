Name:		grafana
Summary:	Metrics dashboard and graph editor
Version:	1.9.0
Release:	1%{?dist}
License:	Apache 2.0
URL:		http://grafana.org
Source:		https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch
BuildRequires:	nodejs
BuildRequires:	nodejs-grunt-cli
BuildRequires:	npm


%description
An open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -q


%build
npm install
grunt


%install
[ "%{buildroot}" != / ] && %{__rm} -rf "%{buildroot}"
%{__mkdir_p} %{buildroot}%{_var}/www/html/%{name}
%{__cp} -r src/* %{buildroot}%{_var}/www/html/%{name}


%clean
[ "%{buildroot}" != / ] && %{__rm} -rf "%{buildroot}"


%files
%defattr(-,root,root,-)
%{_var}/www/html/%{name}


%changelog
* Tue Dec 16 2014 Jiri Tyr <jiri.tyr at gmail.com>
- First build.
