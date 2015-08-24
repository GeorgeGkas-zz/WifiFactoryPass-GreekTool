from PyQt4.QtCore import *
from PyQt4.QtGui import *
from preferences import *


class AppForm(QDialog, Ui_Preferences_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.show()
        self.setFixedSize(350, 300)

   