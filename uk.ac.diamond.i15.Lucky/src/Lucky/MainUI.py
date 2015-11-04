'''
Created on 4 Nov 2015

@author: wnm24546
'''
from PyQt4 import QtCore
from PyQt4.QtGui import (QWidget, QGridLayout, QGroupBox, QHBoxLayout, 
                         QLabel, QLineEdit, QPushButton, QRadioButton, 
                         QVBoxLayout)


class MainUI(QWidget):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle("Lucky")
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        ####
        #Mode controls
        modeGrpBox = QGroupBox("Mode:")
        self.modeRadBtns = []
        self.modeRadBtns.append(QRadioButton("Live"))
        self.modeRadBtns.append(QRadioButton("Offline"))
        
        modeLayout = QHBoxLayout()
        self.addWidgetListToLayout(self.modeRadBtns, modeLayout)
        modeGrpBox.setLayout(modeLayout)
        
        ####
        #Calib controls
        calibGrpBox = QGroupBox("Calibration Type:")
        self.calibRadBtns = []
        self.calibRadBtns.append(QRadioButton("Calibration"))
        self.calibRadBtns.append(QRadioButton("Calibration F1"))
        self.calibRadBtns.append(QRadioButton("Calibration F2"))
        
        calibLayout = QVBoxLayout()
        self.addWidgetListToLayout(self.calibRadBtns, calibLayout)
        calibGrpBox.setLayout(calibLayout)
        
        ####
        #Filename selector
        fileGrpBox = QGroupBox("File:")
        self.prevFileBtn = QPushButton("<")
        self.nextFileBtn = QPushButton(">")
        self.currFileTextBox = QLineEdit()#Default needs to be set from the model!
        
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.prevFileBtn)
        fileLayout.addWidget(self.currFileTextBox)
        fileLayout.addWidget(self.nextFileBtn)
        fileGrpBox.setLayout(fileLayout)
        
        ####
        #Data location
        dataDirGrpBox = QGroupBox("Data directory:")
        self.workDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.browseDirBtn = QPushButton("Browse...")
        
        dataDirLayout = QHBoxLayout()
        dataDirLayout.addWidget(self.workDirTextBox)
        dataDirLayout.addWidget(self.browseDirBtn)
        dataDirGrpBox.setLayout(dataDirLayout)
        
        ####
        #Not sure what this is, probably to do with calib config
        calibConfigGrpBox = QGroupBox("Calibration configuration:")
        self.calibDirLabel = QLabel("Calibration path:")
        self.calibDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.calibConfigBtn = QPushButton("Configure...")
        
        calibConfigLayout = QGridLayout()
        calibConfigLayout.addWidget(self.calibDirLabel, 0, 0)
        calibConfigLayout.addWidget(self.calibDirTextBox, 1, 0)
        calibConfigLayout.addWidget(self.calibConfigBtn, 1, 1)
        calibConfigGrpBox.setLayout(calibConfigLayout)
        
        ###
        #Calculation results
        self.tempLabel = QLabel("Temperature:")
        self.tempValLabel = QLabel("- K")#Default needs to be set from the model!
        self.dTempLabel = QLabel(u"\u0394 T:")
        self.dTempValLabel = QLabel("- K")#Default needs to be set from the model!
        
        resultsLayout = QVBoxLayout()
        resultsLayout.addWidget(self.tempLabel)
        resultsLayout.addWidget(self.tempValLabel, alignment=QtCore.Qt.AlignCenter)
        resultsLayout.addWidget(self.dTempLabel)
        resultsLayout.addWidget(self.dTempValLabel, alignment=QtCore.Qt.AlignCenter)
        
        ####
        #Control buttons
        self.runBtn = QPushButton('Run')
        self.stopBtn = QPushButton('Stop')
        quitBtn = QPushButton('Quit')
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.runBtn)
        buttonLayout.addWidget(self.stopBtn)
        buttonLayout.addWidget(quitBtn)
        
        ####
        #Final magic to put this all together
        controlsLayout = QGridLayout()
        controlsLayout.addWidget(modeGrpBox, 0, 0)
        controlsLayout.addWidget(calibGrpBox, 1, 0)
        controlsLayout.addWidget(fileGrpBox, 2, 0)
        controlsLayout.addWidget(dataDirGrpBox, 0, 1)
        controlsLayout.addWidget(calibConfigGrpBox, 1, 1)
        controlsLayout.addLayout(resultsLayout, 2, 1)
        
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(controlsLayout)
        mainLayout.addLayout(buttonLayout)#, alignment=QtCore.Qt.AlignCenter)
        
        self.setLayout(mainLayout)
        
            
    def addWidgetListToLayout(self, widgetList, layout):
        for i in range(len(widgetList)):
            layout.addWidget(widgetList[i])