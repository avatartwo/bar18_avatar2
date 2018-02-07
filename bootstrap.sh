# 0) Let's move the examples to /home/vagrant
cp -r 01_harvey 02_firefox 03_panda_rr /home/vagrant


# 1) Install general dependencies
sudo apt-get update
sudo apt-get install -y cmake
sudo apt-get install -y python python-pip
sudo apt-get install -y python3 python3-pip
sudo apt-get install -y libc6-i386 gdb git pkg-config gdb-arm-none-eabi
sudo apt-get install -y libcapstone3 libcapstone-dev
sudo apt-get install -y libgtk-3.0 xorg libffi-dev

# 2) Fetch and install avatar
git clone --branch bar18_avatar2 https://github.com/avatartwo/avatar2.git
sudo pip2 install avatar2/
sudo pip3 install avatar2/

# 2.5) fixup keystone's installation path (c.f. https://github.com/keystone-engine/keystone/issues/235)
sudo cp /usr/local/lib/python2.7/dist-packages/usr/lib/python2.7/dist-packages/keystone/libkeystone.so \
        /usr/local/lib/python2.7/dist-packages/keystone
sudo cp /usr/local/lib/python3.5/dist-packages/usr/lib/python3/dist-packages/keystone/libkeystone.so \
        /usr/local/lib/python3.5/dist-packages/keystone

# 3) build the endpoints
./avatar2/targets/build_panda.sh
#./avatar2/targets/build_qemu.sh # QEMU is not needed for this examples - let's skip it here
sudo pip2 install angr
sudo apt-get install -y openocd

# 4) download and unpack, or build firefox for the second example.
#/vagrant/02_firefox/build_firefox.sh 

wget http://www.s3.eurecom.fr/~muench/data/firefox-52.0.en-US.linux-x86_64.tar.bz2 -P /vagrant/02_firefox/
tar -xvf /vagrant/02_firefox/firefox-52.0.en-US.linux-x86_64.tar.bz2 -C /home/vagrant/
ln -s  /home/vagrant/firefox/firefox-bin /vagrant/02_firefox/firefox
