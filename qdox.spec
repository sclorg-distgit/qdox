%global pkg_name qdox
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

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

Summary:        Extract class/interface/method definitions from sources
Name:           %{?scl_prefix}%{pkg_name}
Version:        1.12.1
Release:        9.7%{?dist}
Epoch:          0
License:        ASL 2.0
URL:            http://qdox.codehaus.org/
Source0:        http://repo2.maven.org/maven2/com/thoughtworks/qdox/qdox/%{version}/%{pkg_name}-%{version}-project.tar.bz2
Source1:        qdox-MANIFEST.MF

BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant >= 0:1.6
BuildRequires:  %{?scl_prefix}ant-junit >= 0:1.6
BuildRequires:  %{?scl_prefix}junit >= 0:3.8.1
BuildRequires:  byaccj
BuildRequires:  %{?scl_prefix}jflex
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}maven-changes-plugin
BuildRequires:  %{?scl_prefix}maven-clean-plugin
BuildRequires:  %{?scl_prefix}maven-dependency-plugin
BuildRequires:  %{?scl_prefix}maven-deploy-plugin
BuildRequires:  %{?scl_prefix}maven-install-plugin
BuildRequires:  %{?scl_prefix}maven-site-plugin
BuildRequires:  %{?scl_prefix}maven-surefire-plugin
BuildRequires:  %{?scl_prefix}maven-surefire-provider-junit
BuildRequires:  %{?scl_prefix}maven-release-plugin
BuildRequires:  zip

BuildArch:      noarch


%description
QDox is a high speed, small footprint parser
for extracting class/interface/method definitions
from source files complete with JavaDoc @tags.
It is designed to be used by active code
generators or documentation tools.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API docs for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
find -name *.jar -delete
rm -rf bootstrap

# Ant changed groupId
%pom_remove_dep ant:ant
%pom_add_dep org.apache.ant:ant

# We don't need these plugins
%pom_remove_plugin :maven-antrun-plugin
%pom_remove_plugin :maven-jflex-plugin
%pom_remove_plugin :maven-resources-plugin
%pom_remove_plugin :xsite-maven-plugin
%pom_xpath_remove pom:build/pom:extensions

%mvn_file : %{pkg_name}
%mvn_alias : "qdox:qdox"

# %%mvn_install macro can't install apidocs from custom directory, use default one
%pom_xpath_remove pom:reporting/pom:outputDirectory
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Generate scanner (upstream does this with maven-jflex-plugin)
java -cp `build-classpath jflex java_cup` JFlex.Main \
      -d src/java \
      --skel src/grammar/skeleton.inner \
      src/grammar/lexer.flex

# Generate parser (upstream does this with maven-antrun-plugin)
dir=src/java/com/thoughtworks/qdox/parser/impl
mkdir -p $dir
(cd ./$dir
byaccj \
       -v \
       -Jnorun \
       -Jnoconstruct \
       -Jclass=Parser \
       -Jsemantic=Value \
       -Jpackage=com.thoughtworks.qdox.parser.impl \
       ../../../../../../grammar/parser.y)

# Build artifact
%mvn_build -f

# Inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u target/%{pkg_name}-%{version}.jar META-INF/MANIFEST.MF
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt README.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:1.12.1-9.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-9.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.12.1-9
- Mass rebuild 2013-12-27

* Tue Aug 27 2013 Michal Srb <msrb@redhat.com> - 0:1.12.1-8
- Install javadoc

* Tue Aug 27 2013 Michal Srb <msrb@redhat.com> - 0:1.12.1-7
- Migrate away from mvn-rpmbuild (Resolves: #997469)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Sat Feb 23 2013 Alexander Kurtakov <akurtako@redhat.com> 0:1.12.1-5
- Remove wagon-webdav extension.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:1.12.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.12.1-2
- Run jflex manually before Maven build is started
- Resolves: rhbz#879653

* Tue Dec 11 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.12.1-1
- Update to latest upstream release.

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.12-7
- Add license to javadoc subpackage

* Wed Aug 1 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-6
- Inject osgi metadata from eclipse orbit.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-3
- Build with maven 3.x.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 5 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.12-1
- Update to new version.

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-3
- Make sure to remove all yacc executables.

* Mon Jun 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-2
- Symlink byaccj to both yacc.linux and yacc.linux.x86_64 to keep it building as noarch.

* Mon Mar 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.11-1
- Update to 1.11.

* Mon Feb 15 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.10.1-2
- Rebuild for rhbz#565013.

* Thu Jan 14 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.10.1-1
- Update to upstream 1.10.1.

* Sat Sep 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.2-2
- Remove not needed sources.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.9.2-1
- Update to 1.9.2.

* Fri Apr 03 2009 Ralph Apel <r.apel at r-apel.de> 0:1.8-1.jpp5
- 1.8 as qdox18 because of qdox frozen at 1.6.1 in JPP-5

* Tue Jul 01 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-5.jpp5
- Restore to devel
- Drop mockobjects BR

* Fri Jun 13 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-4.jpp5
- Add com.thoughtworks.qdox groupId to depmap frag

* Tue Feb 26 2008 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-3jpp
- Add settings file
- Fix pom marking jmock dependency as of scope test
- Fix -jpp-depmap.xml for asm2-parent

* Mon Nov 26 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-2jpp
- Fix maven macro value

* Thu Nov 22 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.3-1jpp
- Upgrade to 1.6.3

* Wed May 30 2007 Ralph Apel <r.apel at r-apel.de> 0:1.6.2-1jpp
- Upgrade to 1.6.2
- Activate tests while building with ant
- Make Vendor, Distribution based on macro
- Install depmap frags, poms

* Thu Mar 22 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.6.1-1jpp.ep1.4
- Rebuild with fixed component-info.xml

* Fri Feb 23 2007 Ralph Apel <r.apel at r-apel.de> 0:1.5-3jpp
- Add option to build without maven
- Omit tests when building without maven
- Add gcj_support option

* Mon Feb 20 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5-2jpp
- Rebuild for JPP-1.7, adapting to maven-1.1

* Wed Nov 16 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.5-1jpp
- Upgrade to 1.5
- Build is now done with maven and requires jflex and byaccj

* Wed Aug 25 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.4-3jpp
- Rebuild with Ant 1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-2jpp
- Upgrade to ant-1.6.X

* Mon Jun 07 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.4-1jpp
- Upgrade to 1.4
- Drop Requires: mockobjects (Build/Test only)

* Tue Feb 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.3-1jpp
- First JPackage release
