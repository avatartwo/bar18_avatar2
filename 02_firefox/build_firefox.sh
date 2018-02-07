#!/bin/bash

path=$(dirname "$(readlink -f "$0")")

sudo apt-get install -y  python-dev npm \
     libcurl4-openssl-dev libffi-dev liblzma-dev \
     libsasl2-dev libldap2-dev libssl-dev mercurial \
     libasound2-dev libcurl4-openssl-dev libdbus-1-dev \
     libdbus-glib-1-dev libgconf2-dev libgtk-3-dev \
     libgtk2.0-dev libiw-dev libnotify-dev libpulse-dev \
     libx11-xcb-dev libxt-dev mesa-common-dev python-dbus \
     xvfb yasm unzip zip autoconf2.13

mkdir ~/mozilla-unified
cd ~/mozilla-unified

## Clone the repository. This takes very long
hg clone https://hg.mozilla.org/mozilla-unified -r 383453 .

## Apply the buggy patch
hg import $path/firefox-patch.diff --no-commit

## Hopefully this builds Firefox - if not, please run ./mach bootstrap maunally
echo -e '1\n1\n1\n\n' | ./mach bootstrap
touch ~/mozzila-unified/.mozconfig
echo 'ac_add_options --enable-debug-symbols' > ~/mozzila-unified/.mozconfig
echo 'ac_add_options --disable-install-strip' >> ~/mozilla-unified/.mozconfig

./mach build
./mach package

## Replace the firefox binary with a simlink to the freshly built one 
ln -s ~/mozilla-unified/obj-x86_64-pc-linux-gnu/dist/bin/firefox-bin $path/firefox
