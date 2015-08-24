WifiFactoryPass-GreekTool 
================================
[![Build Status](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool.svg)](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool) ![](https://img.shields.io/badge/health-100%25-yellowgreen.svg?style=flat-square) ![](https://img.shields.io/badge/version-0.1-blue.svg?style=flat-square)  ![](https://img.shields.io/badge/python-2.7-blue.svg?style=flat-square) ![](https://img.shields.io/badge/licence-LGPL%20v3.0-green.svg?style=flat-square) 

-----------
WifiFactoryPass is an **Aircrack** based GUI tool,  created for reasons of flexibility and fun. As the name implies, the tool developed to work mainly in Greek home routers. 

#Requirements
The program uses **PyQt4**, **Reaver v1.4 -t6x-fork** and **Aircrack** suit.
To run it will need to install the above dependencies. Check the following  paragraphs to know how to install it.

##Usage

To run the program we need to have root previlages. In Backtack/Kali Linux distros we just run the bellow line, but in Ubuntu we have to add **sudo** argument before:

	python main.py

For more informations, about the GUI and how to use it, check [Wiki](https://github.com/GeorgeGkas/WifiFactoryPass-GreekTool/wiki)


##Installing Dependencies
Aircrack and Reaver suits comes installed in Backtrack/Kali Linux distros. For Ubuntu we have to install it using the following line:

	sudo apt-get -y install build-essential libpcap-dev sqlite3 libsqlite3-dev python-qt4 aircrack-ng libssl-dev


#Acknowledgements

###Author Informations
 * WifiFactoryPass-GreekTool uses aircrack to recover passwords. Airckrack suit have been developed in the last years to hold Windows machines as well, but after a lot of bugs I found and many incompatible network drives, which don't support inject and sniffing in Windows macine, I prefered to develop the app for Linux Systems.
 
 * The softare is developed mainly for own use. It contains some bugs and lucks of good UI. 

 * For Ideas, Bug Reports, or any other question, create a ''**New Issue**''

###Continuous Integration & Test
This project uses Travis CI to perform tests on linux (Ubuntu 14.04 LTS).

###License
You may use, modify, and redistribute this software under the terms of the [LGPL v3.0](http://www.gnu.org/licenses/lgpl-3.0.html) License. See LICENSE.

#Changelog

####**Version**  **0.2**

 - Remove macchanger. Now uses ifconfig
 - Add collum in network_table to check if a network is cracked (YES/NO).
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
 - Add option for user spesific mac adress, both vendor and serial support
 - Add option for choose of wireless card. If not chosed then the first one
   discovered will be used. This is practical if we use a wireless usb card


####**Version**  **0.1**

 - First Alpha Release