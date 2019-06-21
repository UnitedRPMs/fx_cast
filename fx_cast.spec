# tips node thanks to 314eter

%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global __provides_exclude_from %{_libdir}/mozilla/native-messaging-hosts
%global __requires_exclude_from %{_libdir}/mozilla/native-messaging-hosts
%global __provides_exclude_from %{_libdir}/mozilla/extensions
%global __requires_exclude_from %{_libdir}/mozilla/extensions
%global __requires_exclude (npm|libnode)

# globals for node and nodewebkit (nw)
%global nodev 10.12.0

# Nvm version
%global nvm_ver 0.34.0 

#defining architectures
%ifarch x86_64
%global archnode linux-x64
%else
%global archnode linux-x86
%endif

# commit
%global _commit 0a9af094190c14d7b4625828784d1d274541ef4f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    fx_cast
Version: 0.0.3
Release: 1%{?dist}
Summary: Implementation of the Chrome Sender API Chromecast within Firefox

Group:   Applications/Multimedia
License: MIT
URL:     https://hensm.github.io/fx_cast/

Source0: https://github.com/hensm/fx_cast/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
# Sorry but we need a specific node for compatibility
Source1: https://github.com/nvm-sh/nvm/archive/v%{nvm_ver}.tar.gz
Source2: https://nodejs.org/dist/v%{nodev}/node-v%{nodev}-%{archnode}.tar.gz
Patch:	fx_cast.patch

ExclusiveArch: x86_64

BuildRequires: git 
BuildRequires: mingw32-nsis 
BuildRequires: dpkg
BuildRequires: gcc
BuildRequires:  gcc-c++

%if 0%{?fedora} >= 29
BuildRequires: python-unversioned-command
%endif


%description
Firefox extension that implements the Chrome sender API and exposes it to 
web apps to enable cast support.


%prep
%setup -q -n %name-%{_commit} -a1 -a2 
%patch -p1 

%build

# activate nvm
mv -f nvm-%{nvm_ver} ~/nvm
echo "source ~/nvm/nvm.sh" >> ~/.bashrc

source ~/.bashrc
nvm install %{nodev}
nvm use %{nodev}

export PATH=$PATH:$PWD/node-v%{nodev}-%{archnode}/bin:/usr/bin/
$PWD/node-v%{nodev}-%{archnode}/bin/npm config set python /usr/bin/python2 
$PWD/node-v%{nodev}-%{archnode}/bin/npm config set registry http://registry.npmjs.org/
$PWD/node-v%{nodev}-%{archnode}/bin/npm cache clean --force
$PWD/node-v%{nodev}-%{archnode}/bin/npm install fs-extra mustache makensis pkg@4.4.0 node-fetch dnssd
$PWD/node-v%{nodev}-%{archnode}/bin/npm install @types/mime-types @types/dnssd castv2 jasmine webpack
$PWD/node-v%{nodev}-%{archnode}/bin/npm install web-ext

$PWD/node-v%{nodev}-%{archnode}/bin/npm install 
$PWD/node-v%{nodev}-%{archnode}/bin/npm run build:app
$PWD/node-v%{nodev}-%{archnode}/bin/npm run package:ext

# Fix path
sed -i 's#"path": ".*"#"path": "/usr/bin/fx_cast_bridge"#' dist/app/fx_cast_bridge.json


%install

install -Dm755 dist/app/bridge "%{buildroot}/%{_bindir}/fx_cast_bridge"
install -Dm644 dist/app/fx_cast_bridge.json -t "%{buildroot}/%{_libdir}/mozilla/native-messaging-hosts/"
install -Dm644 "dist/ext/%{name}-%{version}.xpi" "%{buildroot}/%{_libdir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/fx_cast@matt.tf.xpi"


%files
%defattr(755, root, root)
%{_bindir}/fx_cast_bridge
%{_libdir}/mozilla/native-messaging-hosts/fx_cast_bridge.json
%{_libdir}/mozilla/extensions/*/fx_cast@matt.tf.xpi

%changelog

* Thu Jun 20 2019 David Va <davidva AT tuta DOT io> 0.0.3-1
- Initial package
