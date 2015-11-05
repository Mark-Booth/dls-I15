'''
Created on 4 Nov 2015

@author: wnm24546
'''
from PyQt4.QtGui import (QDialog, QDialogButtonBox)

class CalibrationConfigUI(QDialog):
    def __init(self,parent=None):
        super(CalibrationConfigUI, self).__init__(parent)
        self.setWindowTitle("Calibration Configuration")
        
        self.setupUI()
        
        self.show()
    
    def setupUI(self):
        okCancelBtnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        okCancelBtnBox.accepted.connect(self.okClick)
        okCancelBtnBox.rejected.connect(self.cancelClick)
        #layout.addWidget(okCancelBtnBox)