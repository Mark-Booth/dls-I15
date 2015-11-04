'''
Created on 3 Nov 2015

@author: wnm24546
'''

from PyQt4 import QtCore, QtGui
from Lucky import LuckyUIModel

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        luckyAppModel = LuckyUIModel.MainWindowModel()
        
        self.setWindowTitle('Lucky')
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        #Control buttons
        runBtn = QtGui.QPushButton('Run', self)
        runBtn.clicked.connect(self.runBtnPressed)
        
        stopBtn = QtGui.QPushButton('Stop', self)
        stopBtn.clicked.connect(self.stopBtnPressed)
        
        quitBtn = QtGui.QPushButton('Quit', self)
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
    def runBtnPressed():
    	luckyAppModel.runLuckyCalcs()
    	self.updateWidgetStates()
    
    def stopBtnPressed():
    	luckyAppModel.stopLuckyCalcs()
    	self.updateWidgetStates()
    
    def updateWidgetStates():
    	runBtn.setEnabled(luckyAppModel.runEnabled)
    	stopBtn.setEnabled(luckyAppModel.stopEnabled)