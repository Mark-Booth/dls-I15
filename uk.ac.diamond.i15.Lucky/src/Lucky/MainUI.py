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
        
        self.setupUI()
        
    def setupUI(self):
        ####
        #Creation of supporting layouts
        baseLayout = QVBoxLayout()
        controlsLayout = QGridLayout() #This is everything except the buttons
        
        ####
        #Mode controls
        modeGrpBox = QGroupBox("Mode:")
        self.modeRadBtns = []
        self.modeRadBtns.append(QRadioButton("Live"))
        self.modeRadBtns.append(QRadioButton("Offline"))
        
        modeLayout = QHBoxLayout()
        self.addWidgetListToLayout(self.modeRadBtns, modeLayout)
        modeGrpBox.setLayout(modeLayout)
        controlsLayout.addWidget(modeGrpBox, 0, 0)
        
        ####
        #Calib controls
        calibLayout = QVBoxLayout()
        calibGrpBox = QGroupBox("Calibration Type:")
        self.calibRadBtns = []
        self.calibRadBtns.append(QRadioButton("Calibration"))
        self.calibRadBtns.append(QRadioButton("Calibration F1"))
        self.calibRadBtns.append(QRadioButton("Calibration F2"))
        
        calibGrpLayout = QVBoxLayout()
        self.addWidgetListToLayout(self.calibRadBtns, calibGrpLayout)
        calibGrpBox.setLayout(calibGrpLayout)
        calibLayout.addWidget(calibGrpBox)
        
        calibConfBtn = QPushButton("Configure calibration...")
        calibConfBtn.clicked.connect(self.calibConfClick)
        calibLayout.addWidget(calibConfBtn)
        
        controlsLayout.addLayout(calibLayout, 1, 0, 3, 0)
        
        ####
        #Data location
        dataDirGrpBox = QGroupBox("Data directory:")
        self.workDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.browseDirBtn = QPushButton("Browse...")
        
        dataDirLayout = QHBoxLayout()
        dataDirLayout.addWidget(self.workDirTextBox)
        dataDirLayout.addWidget(self.browseDirBtn)
        dataDirGrpBox.setLayout(dataDirLayout)
        controlsLayout.addWidget(dataDirGrpBox, 0, 1)
        
        ####
        #US/DS selector
        fileGrpBox = QGroupBox("Measurement number (US/DS pair):")
        self.prevFileBtn = QPushButton("<")
        self.nextFileBtn = QPushButton(">")
        self.currFileTextBox = QLineEdit()#Default needs to be set from the model!
        
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.prevFileBtn)
        fileLayout.addWidget(self.currFileTextBox)
        fileLayout.addWidget(self.nextFileBtn)
        fileGrpBox.setLayout(fileLayout)
        controlsLayout.addWidget(fileGrpBox, 1, 1)
        
        ###
        #Integration range
        startLabel = QLabel("Beginning:")
        startTextBox = QLineEdit()#Default needs to be set from the model!
        stopLabel = QLabel("End:")
        stopTextBox = QLineEdit()#Default needs to be set from the model!
        
        integRangeGrpBox = QGroupBox("Integration Range:")
        integRangeLayout = QGridLayout()
        integRangeLayout.addWidget(startLabel, 0, 0)
        integRangeLayout.addWidget(startTextBox, 0, 1)
        integRangeLayout.addWidget(stopLabel, 1, 0)
        integRangeLayout.addWidget(stopTextBox, 1, 1)
        integRangeGrpBox.setLayout(integRangeLayout)
        controlsLayout.addWidget(integRangeGrpBox, 2, 1, 2, 1)
        
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
        controlsLayout.addLayout(resultsLayout, 4, 1)
        
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
        #Add the 1st tier layouts to the base layout
        baseLayout.addLayout(controlsLayout)
        baseLayout.addLayout(buttonLayout)
        
        self.setLayout(baseLayout)
        
            
    def addWidgetListToLayout(self, widgetList, layout):
        for i in range(len(widgetList)):
            layout.addWidget(widgetList[i])
    
    def calibConfClick(self):
        pass