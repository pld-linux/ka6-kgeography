#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kgeography
Summary:	kgeography
Name:		ka6-%{kaname}
Version:	25.12.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	aeadb1b98ba69ec0e050b48cdcb3f339
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KGeography is a geography learning tool, which allows you to learn
about the political divisions of some countries (divisions, capitals
of those divisions and their associated flags if there are some).

%description -l pl.UTF-8
KGeography to narzędzi do nauki geografii, które pozwala uczyć się o
podziałach administracyjnych różnych krajów, ich stolicach i flagach.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kgeography

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.kgeography.desktop
%{_datadir}/config.kcfg/kgeography.kcfg
%{_iconsdir}/hicolor/*x*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/kgeography.svgz
%{_datadir}/kgeography
#%{_localedir}/fi/LC_SCRIPTS/kgeography/kgeography.js
#%{_localedir}/fi/LC_SCRIPTS/kgeography/kgeography.pmap
#%{_localedir}/fi/LC_SCRIPTS/kgeography/kgeography.pmapc
#%{_localedir}/fr/LC_SCRIPTS/kgeography/kgeography.js
#%{_localedir}/ja/LC_SCRIPTS/kgeography/kgeography.js
#%{_localedir}/pl/LC_SCRIPTS/kgeography/general.pmap
#%{_localedir}/pl/LC_SCRIPTS/kgeography/general.pmapc
#%{_localedir}/pl/LC_SCRIPTS/kgeography/kgeography.js
#%{_localedir}/uk/LC_SCRIPTS/kgeography/general.pmap
#%{_localedir}/uk/LC_SCRIPTS/kgeography/general.pmapc
#%{_localedir}/uk/LC_SCRIPTS/kgeography/kgeography.js
%{_datadir}/metainfo/org.kde.kgeography.appdata.xml
