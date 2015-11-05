'''
Created on 4 Nov 2015

@author: wnm24546
'''
from PyQt4 import QtCore
from PyQt4.QtGui import (QWidget, QGridLayout, QGroupBox, QHBoxLayout, 
                         QLabel, QLineEdit, QPushButton, QRadioButton, 
                         QVBoxLayout)


class MainView(QWidget):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
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
        
        calibConfBtn = QPushButton("Configure Calibration...")
        calibConfBtn.clicked.connect(self.calibConfClick)
        calibLayout.addWidget(calibConfBtn)
        
        controlsLayout.addLayout(calibLayout, 1, 0, 3, 1)
        
        ####
        #Data location
        dataDirGrpBox = QGroupBox("Data directory:")
        self.workDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.browseDirBtn = QPushButton("Browse...")
        
        dataDirLayout = QHBoxLayout()
        dataDirLayout.addWidget(self.workDirTextBox)
        dataDirLayout.addWidget(self.browseDirBtn)
        dataDirGrpBox.setLayout(dataDirLayout)
        controlsLayout.addWidget(dataDirGrpBox, 0, 1, 1, 2)
        
        ####
        #US/DS selector
        fileGrpBox = QGroupBox("Measurement Number (US/DS pair):")
        self.prevFileBtn = QPushButton("<")
        self.nextFileBtn = QPushButton(">")
        self.currFileTextBox = QLineEdit()#Default needs to be set from the model!
        
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.prevFileBtn)
        fileLayout.addWidget(self.currFileTextBox)
        fileLayout.addWidget(self.nextFileBtn)
        fileGrpBox.setLayout(fileLayout)
        controlsLayout.addWidget(fileGrpBox, 1, 1, 1, 2)
        
        ###
        #Integration range
        integrationTextInputWidth = 40
        startLabel = QLabel("Beginning:")
        self.startTextBox = QLineEdit()#Default needs to be set from the model!
        self.startTextBox.setFixedWidth(integrationTextInputWidth)
        stopLabel = QLabel("End:")
        self.stopTextBox = QLineEdit()#Default needs to be set from the model!
        self.stopTextBox.setFixedWidth(integrationTextInputWidth)
        deltaLabel = QLabel("Window Size:")
        self.deltaTextBox = QLineEdit()#Default needs to be set from the model!
        self.deltaTextBox.setFixedWidth(integrationTextInputWidth)
        nmLabel1, nmLabel2, nmLabel3 = QLabel("nm"), QLabel("nm"), QLabel("nm")
        
        integRangeGrpBox = QGroupBox("Integration Range:")
        integRangeLayout = QGridLayout()
        integRangeLayout.addWidget(startLabel, 0, 0)
        integRangeLayout.addWidget(self.startTextBox, 0, 1)
        integRangeLayout.addWidget(nmLabel1, 0, 2)
        integRangeLayout.addWidget(stopLabel, 0, 3)
        integRangeLayout.addWidget(self.stopTextBox, 0, 4)
        integRangeLayout.addWidget(nmLabel2, 0, 5)
        integRangeLayout.addWidget(deltaLabel, 1, 0)
        integRangeLayout.addWidget(self.deltaTextBox, 1, 1)
        integRangeLayout.addWidget(nmLabel3, 1, 2)
        integRangeGrpBox.setLayout(integRangeLayout)
        controlsLayout.addWidget(integRangeGrpBox, 2, 1, 2, 2)
        
        ###
        #Calculation results
        planckTempLabel = QLabel("Planck Temperature:")
        self.planckTempValLabel = QLabel("- K")#Default needs to be set from the model!
        dPlancKTempLabel = QLabel(u"\u0394 T(Planck):")
        self.dPlanckTempValLabel = QLabel("- K")#Default needs to be set from the model!
        wienTempLabel = QLabel("Wien Temperature:")
        self.wienTempValLabel = QLabel("- K")#Default needs to be set from the model!
        dWienTempLabel = QLabel(u"\u0394 T(Wien):")
        self.dWienTempValLabel = QLabel("- K")#Default needs to be set from the model!
        
        resultsLayout = QGridLayout()
        resultsLayout.addWidget(planckTempLabel, 0, 0)
        resultsLayout.addWidget(self.planckTempValLabel, 0, 1, alignment=QtCore.Qt.AlignRight)
        resultsLayout.addWidget(dPlancKTempLabel, 1, 0)
        resultsLayout.addWidget(self.dPlanckTempValLabel, 1, 1, alignment=QtCore.Qt.AlignRight)
        resultsLayout.addWidget(QWidget(), 0, 2) #This is in effect a spacer
        resultsLayout.addWidget(wienTempLabel, 0, 3)
        resultsLayout.addWidget(self.wienTempValLabel, 0, 4, alignment=QtCore.Qt.AlignRight)
        resultsLayout.addWidget(dWienTempLabel, 1, 3)
        resultsLayout.addWidget(self.dWienTempValLabel, 1, 4, alignment=QtCore.Qt.AlignRight)
        controlsLayout.addLayout(resultsLayout, 4, 0, 1, 3)
        
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