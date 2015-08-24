 #!/bin/bash 

user ="$(whoami)"

echo "Welcome to installation of WifiFactoryPass-GreekTool"
echo "Current version is 0.2"
echo "This script will install all the packages for you"
echo "First we are going to install the dependancies"
sudo apt-get -y install build-essential libpcap-dev sqlite3 libsqlite3-dev libssl-dev

echo "Now we are going to install aircrack-ng"
sudo apt-get -y install aircrack-ng

cd /tmp

echo "We are going to install pixiewps"
wget https://github.com/wiire/pixiewps/archive/master.zip && unzip master.zip

cd pixiewps-master
cd src
make
sudo make install

cd ../
cd ../
rm master.zip 
echo "Successfully installed pixiewps"

echo "We are going to install reaver 1.4 with pixiewps support"
wget https://github.com/t6x/reaver-wps-fork-t6x/archive/master.zip && unzip master.zip

cd reaver-wps-fork-t6x-master
cd src
./configure
make
sudo make install

cd ../
cd ../
cd ../
rm master.zip
echo "Successfully installed reaver 1.4 with pixiewps support"

echo "We are going to install WifiFactoryPass-GreekTool now! "
cd ~
cd Downloads
cd WifiFactoryPass-GreekTool

sudo cp -r  wifitools ../../.wifitools
chmod 777 wifitools.sh
sudo cp wifitools.sh /usr/bin/

cd ../
rm master.zip
echo "Successfully installed WifiFactoryPass-GreekTool! YEAHHHHHHHHH"


echo "Finished installation"
echo "To run the program run wifitools.sh with root privelages"


