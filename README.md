WifiFactoryPass-GreekTool 
================================
[![Build Status](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool.svg)](https://travis-ci.org/GeorgeGkas/WifiFactoryPass-GreekTool) [![Code Health](https://landscape.io/github/GeorgeGkas/WifiFactoryPass-GreekTool/master/landscape.svg?style=flat-square)](https://landscape.io/github/GeorgeGkas/WifiFactoryPass-GreekTool/master) ![](https://img.shields.io/badge/version-0.1-blue.svg?style=flat-square)  ![](https://img.shields.io/badge/python-2.7-blue.svg?style=flat-square) ![](https://img.shields.io/badge/licence-LGPL%20v3.0-green.svg?style=flat-square) 



----------
WifiFactoryPass is an **Aircrack** based GUI tool,  created for reasons of flexibility and fun. As the name implies, the tool developed to work mainly in Greek home routers. 

#Usage
The program uses **Qt4** Library, **Python 2.7**, **PyQt4** and **Aircrack** suit.
To run it will need to install the above dependencies. Check the next paragraph for that!

To run the program we need to have root previlages. In Backtack/Kali Linux distros we just run the bellow line, but in Ubuntu we have to add sudo argument before:

	python main.py



###Installing Dependencies
Aircrack suit comes installed in Backtrack/Kali Linux distros. For Ubuntu we have to install it using the following line:

	sudo apt-get install aircrack-ng

To install Qt Designer 4 we have to simply go to main download page and download it from there. (It is GUI installer, no trouble with terminal commads).  [Qt Download page](http://www.qt.io/download/)

To install PyQt4 we type the following line:

	sudo apt-get install python-qt4


#Acknowledgement

 * WifiFactoryPass-GreekTool uses aircrack to recover passwords. Airckrack suit have been developed in the last years to hold Windows machines as well, but after a lot of bugs I found and many incompatible network drives, which don't support inject and sniffing in Windows macine, I prefered to develop the app for Linux Systems.
 
 * The softare is developed mainly for own use. It contains some bugs and lucks of good UI. However, the tool work well, at least on my machine. 

 * For Ideas, Bug Reports, or any other question, create a ''**New Issue**''


