# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'as.ui'
#
# Created: Thu Aug  6 13:18:22 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Main_window(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(792, 376)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.widget = QtGui.QWidget(MainWindow)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.table_networks = QtGui.QTableWidget(self.widget)
        self.table_networks.setObjectName(_fromUtf8("table_networks"))
        self.table_networks.setColumnCount(8)
        self.table_networks.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.table_networks.setHorizontalHeaderItem(7, item)
        self.verticalLayout.addWidget(self.table_networks)
        self.button_rescan_networks = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_rescan_networks.sizePolicy().hasHeightForWidth())
        self.button_rescan_networks.setSizePolicy(sizePolicy)
        self.button_rescan_networks.setObjectName(_fromUtf8("button_rescan_networks"))
        self.verticalLayout.addWidget(self.button_rescan_networks)
        self.button_attack = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_attack.sizePolicy().hasHeightForWidth())
        self.button_attack.setSizePolicy(sizePolicy)
        self.button_attack.setObjectName(_fromUtf8("button_attack"))
        QtCore.QObject.connect(self.button_rescan_networks, QtCore.SIGNAL(_fromUtf8("clicked()")), self.scan_process)
        QtCore.QObject.connect(self.button_attack, QtCore.SIGNAL(_fromUtf8("clicked()")), self.check_network)
        self.verticalLayout.addWidget(self.button_attack)
        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        item = self.table_networks.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Essid", None))
        item = self.table_networks.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Bssid", None))
        item = self.table_networks.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Channel", None))
        item = self.table_networks.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Signal", None))
        item = self.table_networks.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Enc", None))
        item = self.table_networks.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Cypher", None))
        item = self.table_networks.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Auth", None))
        item = self.table_networks.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Mb", None))
        self.button_rescan_networks.setText(_translate("MainWindow", "Scan networks", None))
        self.button_attack.setText(_translate("MainWindow", "Attack Current Network", None))

