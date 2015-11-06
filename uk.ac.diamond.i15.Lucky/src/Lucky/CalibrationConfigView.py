'''
Created on 4 Nov 2015

@author: wnm24546
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import (QDialog, QDialogButtonBox, QVBoxLayout,
                         QLabel, QHBoxLayout, QWidget, QLineEdit, QPushButton)

from PyQt4.QtCore import Qt


class CalibrationConfigView(QDialog):
    def __init(self,parent=None):
#         super(CalibrationConfigView, self).__init__(self, parent) #This doesn't work.
        QDialog.__init__(self, parent)
        self.setWindowTitle("Calibration Configuration")
        
        self.setupUI()
     
    def setupUI(self):
        baseLayout = QVBoxLayout()
         
        okCancelBtnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        okCancelBtnBox.accepted.connect(self.okClick)
        okCancelBtnBox.rejected.connect(self.cancelClick)
        baseLayout.addWidget(okCancelBtnBox)
         
        self.addLayout(baseLayout)
     
    def okClick(self):
        print "OK!"
         
     
    def cancelClick(self):
        print "Cancel"
