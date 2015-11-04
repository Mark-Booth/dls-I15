'''
Created on 3 Nov 2015

@author: wnm24546
'''

from PyQt4 import QtCore, QtGui
from Lucky import LuckyUIModel

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.luckyAppModel = LuckyUIModel.MainWindowModel()
        
        self.setWindowTitle('Lucky')
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        ####
        #Control buttons
        self.runBtn = QtGui.QPushButton('Run')
        self.runBtn.clicked.connect(self.runBtnPressed)
        
        self.stopBtn = QtGui.QPushButton('Stop')
        self.stopBtn.clicked.connect(self.stopBtnPressed)
        
        quitBtn = QtGui.QPushButton('Quit')
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.runBtn)
        buttonLayout.addWidget(self.stopBtn)
        buttonLayout.addWidget(quitBtn)
        ####
        
        ####
        #Final layout on which everything sits
        masterLayout = QtGui.QVBoxLayout()
        masterLayout.addLayout(buttonLayout)
        self.setLayout(masterLayout)
        
        #Set initial states of the widgets as defined by model
        self.updateWidgetStates()
        
        
    def runBtnPressed(self):
    	self.luckyAppModel.runLuckyCalcs()
    	self.updateWidgetStates()
    
    def stopBtnPressed(self):
    	self.luckyAppModel.stopLuckyCalcs()
    	self.updateWidgetStates()
    
    def updateWidgetStates(self):
    	self.runBtn.setEnabled(self.luckyAppModel.runEnabled)
    	self.stopBtn.setEnabled(self.luckyAppModel.stopEnabled)