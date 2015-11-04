'''
Created on 3 Nov 2015

@author: wnm24546
'''

from PyQt4 import QtCore, QtGui
from Lucky import LuckyUIModel

class MainWindow(QtGui.QWidget):    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        luckyAppModel = LuckyUIModel.MainWindowModel()
        
        self.setWindowTitle('Lucky')
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        #Control buttons
        runBtn = QtGui.QPushButton('Run')
        runBtn.clicked.connect(self.runBtnPressed)
        
        stopBtn = QtGui.QPushButton('Stop')
        stopBtn.clicked.connect(self.stopBtnPressed)
        
        quitBtn = QtGui.QPushButton('Quit')
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        #Layout
        hBoxLayout = QtGui.QHBoxLayout()
        hBoxLayout.addWidget(runBtn)
        hBoxLayout.addWidget(stopBtn)
        hBoxLayout.addWidget(quitBtn)
        
        self.updateWidgetStates()
        self.setLayout(hBoxLayout)
        
    def runBtnPressed(self):
    	luckyAppModel.runLuckyCalcs()
    	self.updateWidgetStates()
    
    def stopBtnPressed(self):
    	luckyAppModel.stopLuckyCalcs()
    	self.updateWidgetStates()
    
    def updateWidgetStates(self):
    	runBtn.setEnabled(luckyAppModel.runEnabled)
    	stopBtn.setEnabled(luckyAppModel.stopEnabled)