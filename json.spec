%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
%define oname JSON-java

Name:       json
Summary:    JavaScript Object Notation support in Java
URL:        http://www.json.org/java/index.html
Version:    20160810
Release:    1
License:    ASL 2.0
Group:      Development/Java
BuildArch:  noarch
Source0:    http://github.com/stleary/%{oname}/releases/%{oname}-%{version}.tar.gz
Source1:    pom.xml
BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  zip

%description
Java support for the JSON (JavaScript Object Notation) lightweight
data-interchange format.  It is based on a subset of the JavaScript
Programming Language, Standard ECMA-262 3rd Edition - December 1999.
JSON is a text format that is completely language independent but uses
conventions that are familiar to programmers of the C-family of
languages including C, C++, C#, Java, JavaScript, Perl, Python, and many
others.

%package javadoc
Summary:    Javadoc for %{name}
Group:      Development/Java
Requires:   jpackage-utils

%description javadoc
API docs for %{name}.

%prep
%setup -q -c -n %{oname}-%{version}
mv %{oname}-%{version} src
cp %SOURCE1 .
%build

%mvn_build

%install
%mvn_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -f .mfiles

%files javadoc -f .mfiles-javadoc



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 3-8
+ Revision: 734055
- rebuild
- imported package json

