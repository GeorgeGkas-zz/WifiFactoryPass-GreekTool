#!/usr/bin/python

# -*- coding: utf-8 -*-

import commands
import time
import fileinput

from system_functions import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main_window import Ui_Main_window
from client import *
from wpe_crack import *
from preferences_func import *

class Main_window_ex(QMainWindow, Ui_Main_window):
    
    def __init__(self, parent = None):
        """
        Default Constructor. It can receive a top window as parent. 
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.table_networks.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.button_attack.setEnabled(False)
        self.button_reset_process.setEnabled(False)

        self.start_procedure_is_pressed = False
        self.reset_process_is_pressed = False
        self.device_interface = str()
        self.device_mac= str()
        self.true_mac= str()
        self.scan_output=list()
        self.victim = list()
        self.essid = str()
        self.bssid = str()
        self.channel = str()
        self.assossiate_dict = dict()
        self.cracked = str()
        self.support_wps = str()
        self.run_problem = False


        with open('variables.txt', 'w+') as f:
            f.seek(0)
            f.truncate()
            f.write('random_mac_vendor|\nrandom_mac_serial|\nwicard|\n')

        direct_output(self, 'Program started-----')

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if self.start_procedure_is_pressed == True:
                exit_procedure(self)
            if self.run_problem:
                time_now = time.strftime("%H:%M:%S", time.localtime())
                date_now = time.strftime("%d-%m-%Y")
                log_name = date_now + '_' + time_now + '.txt'
                with open('Logs/' + log_name, 'w') as fl:
                    fl.write(str(self.text_output.toPlainText()))

            event.accept()
        else:
            event.ignore()

    def check_network(self):
        if not self.table_networks.selectedIndexes():
            return

        self.victim[:] = []

        for idx in self.table_networks.selectedIndexes():
            self.victim.append(idx.data().toString()) 


        self.encryption = str(self.victim[4])
        self.essid = str(self.victim[0])
        self.bssid = str(self.victim[1])
        self.channel = str(self.victim[2])
        self.client = str(self.victim[8])
        self.cracked = str(self.victim[10])
        self.support_wps = str(self.victim[9])

        if self.cracked == 'YES':
            #check keys.lst database for cracked network
            with open('keys.lst', 'r') as f:
                    for line in f:
                        network = line.split('|')
                        if network[0] == self.bssid:
                            print 'key is ' + network[1]
                            return
                        network[:] = []

        if self.support_wps == 'YES':
            reply = QtGui.QMessageBox.question(self, 'Message',
            "Network <b>MAYBE</b> support Pixie Dust Attack.\n <center>Do you want to try it?</center>\n ", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                direct_output(self, 'We are going to try Pixie Dust attack in ' + str(self.essid))
                pixie_dust_attack = "reaver -i mon0 -m " + self.true_mac +" -c " + self.channel + " -b " + self.bssid + " -vv -K 1"
                ct = Command_thread(pixie_dust_attack)
                ct.start()
                return


        if self.encryption == 'OPN':
            direct_output(self, '<b>The network is OPEN. Go connect!</b>')

        elif self.encryption == 'WPA' or self.encryption == 'WPA2' or self.encryption == 'WPA2WPA':

            self.w = Client(self.victim)
            self.w.setGeometry(QRect(100, 100, 400, 200))
            
            check_wpa_essid(self)

        elif self.encryption == 'WEP':

            self.wep = WEP_Crack(self.victim, self.device_mac)
            self.wep.setGeometry(QRect(100, 100, 400, 200))
        else:
            direct_output(self, 'Error: Can\'t find the encryption of the network')

    def scan_process(self):
        self.button_rescan_networks.setEnabled(False)
        self.button_attack.setEnabled(False)
        self.button_reset_process.setEnabled(True)
        sender = self.sender()
        self.statusBar().showMessage('Process started')
        if self.start_procedure_is_pressed == True:
            rescan(self)
        else:
            first_scan(self)


    def reset_process(self):
        exit_procedure(self)
        with open('variables.txt', 'w+') as f:
            f.seek(0)
            f.truncate()
            f.write('random_mac_vendor|\nrandom_mac_serial|\nwicard|\n')
        for i in range(self.table_networks.rowCount(), -1, -1):
            self.table_networks.removeRow(i)
            time.sleep(0.1)
            QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze
        self.button_reset_process.setEnabled(False)
        self.text_output.append('\n')
        self.reset_process_is_pressed = True
        self.button_rescan_networks.setEnabled(True)


    def open_window_preferences(self):
		Dialog = QtGui.QDialog()
		u = Ui_Preferences_Dialog()
		u.setupUi(Dialog)

		Dialog.exec_()


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
