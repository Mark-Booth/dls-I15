'''
Created on 3 Nov 2015

@author: wnm24546
'''

from PyQt4 import QtCore, QtGui
import UIApplicationModel

class LuckyMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(LuckyMainWindow, self).__init__()
        luckyAppModel = UIApplicationModel.ApplicationModel()
        
        self.setWindowTitle('Lucky')
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        #Control buttons
        runBtn = QtGui.QPushButton('Run', self)
        runBtn.clicked.connect(self.runBtnClicked())
        
        stopBtn = QtGui.QPushButton('Stop', self)
        stopBtn.clicked.connect(self.stopBtnClicked())
        
        quitBtn = QtGui.QPushButton('Quit', self)
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        
        
        
    def runBtnClicked(self):
        sender = self.sender()
        sender.text()
    
    def stopBtnClicked(self):
        sender = self.sender()
        sender.text()