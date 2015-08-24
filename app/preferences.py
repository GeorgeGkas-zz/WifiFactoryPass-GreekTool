# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Fri Aug 21 20:53:15 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!
import commands
import fileinput

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from time import sleep

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Preferences_Dialog(object):
    def setupUi(self, Preferences_Dialog):
        Preferences_Dialog.setObjectName(_fromUtf8("Preferences_Dialog"))
        Preferences_Dialog.resize(581, 400)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preferences_Dialog.sizePolicy().hasHeightForWidth())
        Preferences_Dialog.setSizePolicy(sizePolicy)
        Preferences_Dialog.setMinimumSize(QtCore.QSize(581, 400))
        Preferences_Dialog.setMaximumSize(QtCore.QSize(581, 400))
        self.label = QtGui.QLabel(Preferences_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.use_random_mac = QtGui.QCheckBox(Preferences_Dialog)
        self.use_random_mac.setEnabled(True)
        self.use_random_mac.setGeometry(QtCore.QRect(200, 10, 97, 22))
        self.use_random_mac.setChecked(True)
        self.use_random_mac.setObjectName(_fromUtf8("use_random_mac"))
        self.save_preferences = QtGui.QPushButton(Preferences_Dialog)
        self.save_preferences.setGeometry(QtCore.QRect(470, 360, 96, 26))
        self.save_preferences.setObjectName(_fromUtf8("save_preferences"))
        self.discard_preferences = QtGui.QPushButton(Preferences_Dialog)
        self.discard_preferences.setGeometry(QtCore.QRect(370, 360, 96, 26))
        self.discard_preferences.setObjectName(_fromUtf8("discard_preferences"))
        self.use_random_vendor = QtGui.QCheckBox(Preferences_Dialog)
        self.use_random_vendor.setGeometry(QtCore.QRect(200, 30, 171, 22))
        self.use_random_vendor.setObjectName(_fromUtf8("use_random_vendor"))
        self.use_random_serial = QtGui.QCheckBox(Preferences_Dialog)
        self.use_random_serial.setGeometry(QtCore.QRect(390, 30, 161, 22))
        self.use_random_serial.setObjectName(_fromUtf8("use_random_serial"))
        self.line_vendor = QtGui.QLineEdit(Preferences_Dialog)
        self.line_vendor.setGeometry(QtCore.QRect(200, 50, 171, 27))
        self.line_vendor.setObjectName(_fromUtf8("line_vendor"))
        self.line_serial = QtGui.QLineEdit(Preferences_Dialog)
        self.line_serial.setGeometry(QtCore.QRect(390, 50, 171, 27))
        self.line_serial.setObjectName(_fromUtf8("line_serial"))
        self.label_3 = QtGui.QLabel(Preferences_Dialog)
        self.label_3.setGeometry(QtCore.QRect(290, 10, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_3.setScaledContents(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Preferences_Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 151, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Preferences_Dialog)
        self.label_5.setGeometry(QtCore.QRect(170, 100, 341, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.wicard_scan = QtGui.QPushButton(Preferences_Dialog)
        self.wicard_scan.setGeometry(QtCore.QRect(10, 130, 96, 26))
        self.wicard_scan.setObjectName(_fromUtf8("wicard_scan"))
        self.wicard_choose = QtGui.QComboBox(Preferences_Dialog)
        self.wicard_choose.setGeometry(QtCore.QRect(120, 130, 101, 27))
        self.wicard_choose.setObjectName(_fromUtf8("wicard_choose"))
        self.wicard_set = QtGui.QPushButton(Preferences_Dialog)
        self.wicard_set.setGeometry(QtCore.QRect(230, 130, 71, 26))
        self.wicard_set.setObjectName(_fromUtf8("wicard_set"))

        # Default state of random_mac is hiden
        self.use_random_vendor.hide()
        self.use_random_serial.hide()
        self.line_vendor.hide()
        self.line_serial.hide()

        #the above state is changed when the use_random_mac isn't checked
        self.use_random_mac.stateChanged.connect(self.set_mac_state) 
        self.use_random_vendor.stateChanged.connect(self.proceed_vendor_warning) 


        # Buttons
        self.save_preferences.clicked.connect(self.save)
        self.wicard_scan.clicked.connect(self.get_wireless_card)
        self.wicard_set.clicked.connect(self.set_wicard)

        self.retranslateUi(Preferences_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Preferences_Dialog)

    def retranslateUi(self, Preferences_Dialog):
        Preferences_Dialog.setWindowTitle(_translate("Preferences_Dialog", "Dialog", None))
        self.label.setText(_translate("Preferences_Dialog", "Mac Adress Options", None))
        self.use_random_mac.setText(_translate("Preferences_Dialog", "Random", None))
        self.save_preferences.setText(_translate("Preferences_Dialog", "Save", None))
        self.discard_preferences.setText(_translate("Preferences_Dialog", "Discard", None))
        self.use_random_vendor.setText(_translate("Preferences_Dialog", "Spesify your Vendor", None))
        self.use_random_serial.setText(_translate("Preferences_Dialog", "Spesify your Serial", None))
        self.label_3.setText(_translate("Preferences_Dialog", "* with real vendors", None))
        self.label_4.setText(_translate("Preferences_Dialog", "Choose Wireless Card", None))
        self.label_5.setText(_translate("Preferences_Dialog", "If don\'t spessidy, the first one scanned will be used", None))
        self.wicard_scan.setText(_translate("Preferences_Dialog", "Scan", None))
        self.wicard_set.setText(_translate("Preferences_Dialog", "Set", None))


    def proceed_vendor_warning(self):
        if self.use_random_vendor.isChecked():
            widget = QWidget()
            QtGui.QMessageBox.warning(widget, "Warning", "<center>Using your own mac vendor might not work.<center>Please read a reference in mac adresses.Not all combinations work.</center><center>If you don't know what you are doing please UNCHECK that box</center>")
            return


    def set_mac_state(self):
        if self.use_random_mac.isChecked():
            self.use_random_vendor.hide()
            self.use_random_serial.hide()
            self.line_vendor.hide()
            self.line_serial.hide()
        else:

            self.use_random_vendor.show()
            self.use_random_serial.show()
            self.line_vendor.show()
            self.line_serial.show()


    def save(self):
        if self.use_random_mac.isChecked():
            return

        if self.use_random_vendor.isChecked() or self.use_random_serial.isChecked():
            pass
        else:
            widget = QWidget()
            QtGui.QMessageBox.warning(widget, "Warning", "Please spessify at least one option")
            return
   
        
        if self.use_random_vendor.isChecked():
            if not self.line_vendor.text():
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Please set mac vendor")
                return
            macv = self.line_vendor.text()
            macv_num = macv.count()
            if macv_num != 6:
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Please set mac vendor as XXXXXX")
                return
            if any(i in macv for i in '[~!@#$%^&*()_+{}";:\']+$ghijklmnopqrstuvwxyz'):
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Only allowed characters 0-9 A-F")
                return
            first_octect = int(macv[0:2])
            random_mac_vendor = macv
            with open('variables.txt', 'r+') as f:
                variables = f.readlines()
                print variables
                variables[0] = 'random_mac_vendor|' + str(random_mac_vendor) + '\n'
                f.seek(0)
                for info in variables:
                    f.write(info)

        if self.use_random_serial.isChecked():
            if not self.line_serial.text():
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Please set mac Serial")
                return
            macs = self.line_serial.text()
            macs_num = macs.count()
            if macs_num != 6:
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Please set mac serial as XXXXXX")
                return
            if any(i in macs for i in '[~!@#$%^&*()_+{}";:\']+$ghijklmnopqrstuvwxyz'):
                widget = QWidget()
                QtGui.QMessageBox.warning(widget, "Warning", "Only allowed characters 0-9 A-F")
                return

            first_octect = int(macs[0:2])

            random_mac_serial = macs
            with open('variables.txt', 'r+') as f:
                variables = f.readlines()
                print variables
                variables[1] = 'random_mac_serial|' + str(random_mac_serial) + '\n'
                f.seek(0)
                for info in variables:
                    f.write(info)






    def get_wireless_card(self):
        airmon = commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'")

        airmon = airmon.split('\n')
        device_interface = list()
        for interface in airmon:
            if interface == "" or interface[0:3] == 'mon':
                continue
            else:
                device_interface = interface.split('\t')
                self.wicard_choose.addItem(device_interface[0])
                device_interface[:] = []
                sleep(0.1)
                QtGui.QApplication.processEvents() # to make the programm run smoothly and not freeze


    def set_wicard(self):
        if self.wicard_choose.currentText():
            wicard = self.wicard_choose.currentText()
            with open('variables.txt', 'r+') as f:
                variables = f.readlines()
                print variables
                variables[2] = 'wicard|' + str(wicard) + '\n'
                f.seek(0)
                for info in variables:
                    f.write(info)
                
        else:
            widget = QWidget()
            QtGui.QMessageBox.warning(widget, "Warning", "Please make a scan first")
        

