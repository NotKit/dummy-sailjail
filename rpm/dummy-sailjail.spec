Name:       dummy-sailjail

Summary:    Dummy sailjail wrapper
Version:    1.1.23.1
Release:    1
Group:      Qt/Qt
License:    LICENSE
URL:        https://github.com/elros34/dummy-sailjail
Source0:    %{name}-%{version}.tar.bz2
Provides:   sailjail == %{version}
Conflicts:  sailjail
Obsoletes:  sailjail <= 1.1.23
Requires:   mapplauncherd-booster-browser
Provides:   sailjail-launch-approval
Obsoletes:  sailjail-homescreen-plugin <= 1.1.0

%description
Dummy sailjail wrapper


%prep
%setup -q -n %{name}-%{version}

%transfiletriggerin -- /usr/share/applications/
/usr/bin/disable_sailjail_in_desktop.sh $(cat)

%triggerin -- jolla-camera
sed -i 's|silica-qt5 -A |silica-qt5 |' /usr/share/applications/jolla-camera*.desktop

%triggerin -- jolla-camera-lockscreen
sed -i 's|silica-qt5 -A |silica-qt5 |' /usr/share/applications/jolla-camera-lockscreen.desktop

%post
/usr/bin/disable_sailjail_in_desktop.sh $(ls /usr/share/applications/*.desktop)


%install
rm -rf %{buildroot}
install -D -m 0755 sailjail %{buildroot}/usr/bin/sailjail
install -D -m 0755 disable_sailjail_in_desktop.sh %{buildroot}/usr/bin/disable_sailjail_in_desktop.sh
mkdir -p %{buildroot}/etc
cp -r data/systemd/ %{buildroot}/etc/
mkdir -p %{buildroot}/usr/share
cp -r data/mapplauncherd/ %{buildroot}/usr/share/
mkdir -p %{buildroot}/usr/local/share/
cp -r data/dbus-1 %{buildroot}/usr/local/share/
mkdir -p %{buildroot}/etc/sailjail/config/
cp data/51-disable-default-profile.conf %{buildroot}/etc/sailjail/config/
# sandboxed boosters
ln -s /dev/null %{buildroot}/etc/systemd/user/booster-generic@.service
ln -s /dev/null %{buildroot}/etc/systemd/user/booster-qt5@.service
ln -s /dev/null %{buildroot}/etc/systemd/user/booster-browser@.service
ln -s /dev/null %{buildroot}/etc/systemd/user/booster-silica-qt5@.service
ln -s /dev/null %{buildroot}/etc/systemd/user/booster-silica-media@.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
/etc/sailjail/config/*
/etc/systemd/user/
/usr/share/mapplauncherd/
/usr/local/share/dbus-1/
