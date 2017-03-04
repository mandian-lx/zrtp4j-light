%{?_javapackages_macros:%_javapackages_macros}

%define commit beb6723b2e13e27710e38ea9b64f2da8d9a395a3
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define oname zrtp4j

%define version_pom 20150723.002345

Summary:	Java implementation of ZRTP protocol 
Name:		%{oname}-light
Version:	4.1.0
Release:	0
License:	GPLv3+
Group:		Development/Java
Url:		https://github.com/jitsi/zrtp4j
Source0:	https://github.com/jitsi/zrtp4j/archive/%{commit}/%{name}-%{commit}.zip
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires:	mvn(org.jitsi:bccontrib)
BuildRequires:	mvn(org.jitsi:fmj)

%description
This package provides a library that adds ZRTP support to JMF
and FMJ. Phil Zimmermann developed ZRTP to allow ad-hoc, easy to
use key negotiation to setup Secure RTP (SRTP) sessions. GNU ZRTP4J
together with Sun's JMF or the free alternative FMJ provides a ZRTP
implementation that can be directly embedded into client and server
applications.

%files -f .mfiles
%doc README.txt
%doc legal/LICENSE-gnu.txt
%doc legal/LICENSE-ZRTP4J-exception.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
Java library for capturing images from a video source.

This package contains documentation for %{name}.

%files javadoc
%{_javadocdir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{commit}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# fix fmj artifactId according to fmj package
#%pom_change_dep :fmj:: :fmj-jitsi:: ./m2/%{name}/

# Remove jitsi-universe parent
%pom_remove_parent ./m2/%{name}

# Add groupId
%pom_xpath_inject "pom:project" "<groupId>org.jitsi</groupId>" ./m2/%{name}/

# Fix missing version
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]" "
	<version>any</version>" ./m2/%{name}/

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_add_plugin :maven-jar-plugin ./m2/%{name}/ "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Set the right name to fit the packaging guidelines
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -f m2/%{name}/pom.xml -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

