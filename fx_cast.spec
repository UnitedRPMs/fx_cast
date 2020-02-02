#
# spec file for package fx_cast
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

# tips node thanks to 314eter

# workaround debug-id conflicts (with vdhcoapp)
%global _build_id_links none

#{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global __provides_exclude_from %{_libdir}/mozilla/native-messaging-hosts
%global __requires_exclude_from %{_libdir}/mozilla/native-messaging-hosts
%global __provides_exclude_from %{_libdir}/mozilla/extensions
%global __requires_exclude_from %{_libdir}/mozilla/extensions
%global __requires_exclude (npm|libnode)

# globals for node and nodewebkit (nw)
%global nodev 13.7.0

# Nvm version
%global nvm_ver 0.35.2 

#defining architectures
%ifarch x86_64
%global archnode linux-x64
%else
%global archnode linux-x86
%endif

# commit
%global _commit 5e4c8d20f476637abd8eb4e33495062d8023fb74
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    fx_cast
Version: 0.0.5
Release: 2%{?dist}
Summary: Implementation of the Chrome Sender API Chromecast within Firefox

Group:   Applications/Multimedia
License: MIT
URL:     https://hensm.github.io/fx_cast/

Source0: https://github.com/hensm/fx_cast/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
# Sorry but we need a specific node for compatibility
Source1: https://github.com/nvm-sh/nvm/archive/v%{nvm_ver}.tar.gz
Source2: https://nodejs.org/dist/v%{nodev}/node-v%{nodev}-%{archnode}.tar.gz
Source3: %{name}.desktop
#Patch:	fx_cast.patch

ExclusiveArch: x86_64

BuildRequires: git 
BuildRequires: mingw32-nsis 
BuildRequires: dpkg
BuildRequires: gcc
BuildRequires: gcc-c++

%if 0%{?fedora} >= 29
BuildRequires: python-unversioned-command
%endif


%description
Firefox extension that implements the Chrome sender API and exposes it to 
web apps to enable cast support.


%prep
%setup -q -n %name-%{_commit} -a1 -a2 
#patch -p1 

%build

# activate nvm
mv -f nvm-%{nvm_ver} ~/nvm
echo "source ~/nvm/nvm.sh" >> ~/.bashrc

source ~/.bashrc
nvm install %{nodev}
nvm use %{nodev}

export PATH=$PATH:$PWD/node-v%{nodev}-%{archnode}/bin:/usr/bin/
#$PWD/node-v%{nodev}-%{archnode}/bin/npm config set python /usr/bin/python2.7
env -i PYTHON=/usr/bin/python2.7



$PWD/node-v%{nodev}-%{archnode}/bin/npm config set registry http://registry.npmjs.org/ 
$PWD/node-v%{nodev}-%{archnode}/bin/npm install jasmine --save-dev 
$PWD/node-v%{nodev}-%{archnode}/bin/npm install bufferutil@^4.0.1 --save-dev
$PWD/node-v%{nodev}-%{archnode}/bin/npm install utf-8-validate@^5.0.2 --save-dev
$PWD/node-v%{nodev}-%{archnode}/bin/npm install mustache --save-dev
$PWD/node-v%{nodev}-%{archnode}/bin/npm install jasmine-console-reporter --save-dev
$PWD/node-v%{nodev}-%{archnode}/bin/npm install makensis --save-dev
#$PWD/node-v%{nodev}-%{archnode}/bin/npm install pkg --save-dev
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev git+https://github.com/zeit/pkg.git
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev @types/node-fetch
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev dnssd
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev @types/dnssd
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev @types/mime-types
$PWD/node-v%{nodev}-%{archnode}/bin/npm install --save-dev castv2
$PWD/node-v%{nodev}-%{archnode}/bin/npm audit fix
$PWD/node-v%{nodev}-%{archnode}/bin/npm install 
$PWD/node-v%{nodev}-%{archnode}/bin/npm run build:app
#$PWD/node-v%{nodev}-%{archnode}/bin/npm run package:ext

# Fix path
sed -i 's#"path": ".*"#"path": "/opt/fx_cast/fx_cast_bridge"#' dist/app/fx_cast_bridge.json


%install

install -Dm755 dist/app/fx_cast_bridge "%{buildroot}/opt/fx_cast/fx_cast_bridge"
install -Dm644 dist/app/fx_cast_bridge.json -t "%{buildroot}/%{_libdir}/mozilla/native-messaging-hosts/"
#install -Dm644 "dist/ext/%{name}-%{version}.xpi" "%{buildroot}/%{_libdir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/fx_cast@matt.tf.xpi"

install -Dm644 %{S:3} -t %{buildroot}/etc/xdg/autostart/%{name}.desktop

%files
#defattr(755, root, root)
/opt/fx_cast/fx_cast_bridge
%{_libdir}/mozilla/native-messaging-hosts/fx_cast_bridge.json
#{_libdir}/mozilla/extensions/*/fx_cast@matt.tf.xpi
/etc/xdg/autostart/%{name}.desktop

%changelog

* Fri Jan 31 2020 David Va <davidva AT tuta DOT io> 0.0.5-2
- Updated to 0.0.5

* Thu Aug 29 2019 David Va <davidva AT tuta DOT io> 0.0.4-2
- Updated to 0.0.4

* Sat Jun 22 2019 David Va <davidva AT tuta DOT io> 0.0.3-2
- Updated to current commit

* Thu Jun 20 2019 David Va <davidva AT tuta DOT io> 0.0.3-1
- Initial package
