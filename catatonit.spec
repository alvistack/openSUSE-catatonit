# Copyright 2025 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

Name: catatonit
Epoch: 100
Version: 0.2.1
Release: 1%{?dist}
Summary: A signal-forwarding process manager for containers
License: GPL-2.0-or-later
URL: https://github.com/openSUSE/catatonit/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: glibc-static
BuildRequires: libtool

%description
Catatonit is a /sbin/init program for use within containers. It forwards
(almost) all signals to the spawned child, tears down the container when
the spawned child exits, and otherwise cleans up other exited processes
(zombies).

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/catatonit

%changelog
