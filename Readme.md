WifiFactoryPass-GreekTool 
================================
[![Build Status](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool.svg)](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool) ![](https://img.shields.io/badge/health-100%25-yellowgreen.svg?style=flat-square) ![](https://img.shields.io/badge/version-0.2-blue.svg?style=flat-square)  ![](https://img.shields.io/badge/python-2.7-blue.svg?style=flat-square) ![](https://img.shields.io/badge/licence-LGPL%20v3.0-green.svg?style=flat-square) 

-----------
WifiFactoryPass is an **Aircrack** based GUI tool,  created for reasons of flexibility and fun. As the name implies, it was developed to work mainly in Greek home routers.  

#Requirements
**PyQt4**, **Reaver v1.4 -t6x-fork**, **PixieWps** and **Aircrack** suit required.
Developed and tested on Ubuntu 14.04. Above versions of the distro will work as well, but no other Linux was tested.  
**It is recommend to run the program on Ubuntu 14.04+**
To run you'll need to install the above dependencies. Check the following  paragraphs to know how to install it.

##Installing Dependencies - Usage
To install the required dependencies, as described above, you need first to run the installation script that comes with the zip version. Navigate to your folder and run,

    bash install.sh

providing the password when you asked. 
The installation might take some time, but when it finished you can run the program from the terminal using the below command:

    ./wifitools.sh

For more informations, about the GUI and how to use it, check the [project website](http://georgegkas.github.io/WifiFactoryPass-GreekTool)

#Acknowledgements

###Author Informations
 * WifiFactoryPass-GreekTool uses aircrack to recover passwords. Airckrack in the last years hold Windows machines as well, but after a lot of bugs I found and many incompatible network drives, which don't support inject and sniffing in Windows machine, I preferred to develop the app for Ubuntu Linux Systems.
 
 * The software is developed mainly for my own use. It contains some bugs and lucks of good UI. 

 * For Ideas, Bug Reports, or any other question, create a ''**New Issue**''

###Continuous Integration & Test
This project uses Travis CI to perform tests on Linux (Ubuntu 14.04 LTS).

###License
You may use, modify, and redistribute this software under the terms of the [LGPL v3.0](http://www.gnu.org/licenses/lgpl-3.0.html) License. See LICENSE.

#Changelog

####**Version**  **0.2**

 - Remove macchanger. Now uses ifconfig 
 - Add column in network_table to check if a network is cracked (YES/NO).
   If it is and when the user press the "Attack" button a message will pop up with the key
 - Log system is now in use. Log files are generated when program fails in any commands
 - Fixes some crash issues -Not all of them-
 - Read cap file of airodump attack window for handshake.If found kill the airodump
 - Check for WPS support of an network reading the cap file of airodump
 - PixieDust Attack added in WPS supported networks
 - Update the UI elements and how their behave
 - Added better mac support using real vendors
 - Preferences Window created
 - Reset Process button added to help us uncover from bugs in runtime (If Any)
 - Add option for user specific mac address, both vendor and serial support
 - Add option for choose of wireless card. If not chosed then the first one
   discovered will be used. This is practical if we use a wireless usb card
 - Added Thomson support from routers in year range 2004 - 2010


####**Version**  **0.1**

 - First Alpha Release

