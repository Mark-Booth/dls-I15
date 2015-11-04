'''
Created on 4 Nov 2015

@author: wnm24546
'''
from PyQt4 import QtGui, QtCore


class MainUI(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle("Lucky")
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        ####
        #Mode controls
        modeGrpBox = QtGui.QGroupBox("Mode:")
        self.modeRadBtns = []
        self.modeRadBtns.append(QtGui.QRadioButton("Live"))
        self.modeRadBtns.append(QtGui.QRadioButton("Offline"))
        
        modeLayout = QtGui.QHBoxLayout()
        self.addWidgetListToLayout(self.modeRadBtns, modeLayout)
        modeGrpBox.setLayout(modeLayout)
        
        ####
        #Calib controls
        calibGrpBox = QtGui.QGroupBox("Calibration Type:")
        self.calibRadBtns = []
        self.calibRadBtns.append(QtGui.QRadioButton("Calibration F1"))
        self.calibRadBtns.append(QtGui.QRadioButton("Calibration F2"))
        self.calibRadBtns.append(QtGui.QRadioButton("Calibration"))
        
        calibLayout = QtGui.QVBoxLayout()
        self.addWidgetListToLayout(self.calibRadBtns, calibLayout)
        calibGrpBox.setLayout(calibLayout)
        
        ####
        #Filename selector
        fileGrpBox = QtGui.QGroupBox("File:")
        self.prevFileBtn = QtGui.QPushButton("<")
        self.nextFileBtn = QtGui.QPushButton(">")
        self.currFileTextBox = QtGui.QLineEdit()#Default needs to be set from the model!
        
        fileLayout = QtGui.QHBoxLayout()
        fileLayout.addWidget(self.prevFileBtn)
        fileLayout.addWidget(self.currFileTextBox)
        fileLayout.addWidget(self.nextFileBtn)
        fileGrpBox.setLayout(fileLayout)
        
        ####
        #Data location
        dataDirGrpBox = QtGui.QGroupBox("Data directory:")
        self.workDirTextBox = QtGui.QLineEdit()#Default needs to be set from the model!
        self.browseDirBtn = QtGui.QPushButton("Browse...")
        
        dataDirLayout = QtGui.QHBoxLayout()
        dataDirLayout.addWidget(self.workDirTextBox)
        dataDirLayout.addWidget(self.browseDirBtn)
        dataDirGrpBox.setLayout(dataDirLayout)
        
        ####
        #Not sure what this is, probably to do with calib config
        calibConfigGrpBox = QtGui.QGroupBox("Calibration configuration:")
        self.calibDirLabel = QtGui.QLabel("Calibration path:")
        self.calibDirTextBox = QtGui.QLineEdit()#Default needs to be set from the model!
        self.calibConfigBtn = QtGui.QPushButton("Configure...")
        
        calibConfigLayout = QtGui.QGridLayout()
        calibConfigLayout.addWidget(self.calibDirLabel, 0, 0)
        calibConfigLayout.addWidget(self.calibDirTextBox, 1, 0)
        calibConfigLayout.addWidget(self.calibConfigBtn, 1, 1)
        calibConfigGrpBox.setLayout(calibConfigLayout)
        
        ###
        #Calculation results
        self.tempLabel = QtGui.QLabel("Temperature:")
        self.tempValLabel = QtGui.QLabel("- K")#Default needs to be set from the model!
        self.dTempLabel = QtGui.QLabel(u"\u0394 T:")
        self.dTempValLabel = QtGui.QLabel("- K")#Default needs to be set from the model!
        
        resultsLayout = QtGui.QVBoxLayout()
        resultsLayout.addWidget(self.tempLabel)
        resultsLayout.addWidget(self.tempValLabel, alignment=QtCore.Qt.AlignCenter)
        resultsLayout.addWidget(self.dTempLabel)
        resultsLayout.addWidget(self.dTempValLabel, alignment=QtCore.Qt.AlignCenter)
        
        ####
        #Control buttons
        self.runBtn = QtGui.QPushButton('Run')
        self.stopBtn = QtGui.QPushButton('Stop')
        quitBtn = QtGui.QPushButton('Quit')
        quitBtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addWidget(self.runBtn)
        buttonLayout.addWidget(self.stopBtn)
        buttonLayout.addWidget(quitBtn)
        
        ####
        #Final magic to put this all together
        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(modeGrpBox, 0, 0)
        controlsLayout.addWidget(calibGrpBox, 0, 1)
        controlsLayout.addWidget(fileGrpBox, 0, 2)
        controlsLayout.addWidget(dataDirGrpBox, 1, 0)
        controlsLayout.addWidget(calibConfigGrpBox, 1, 1)
        controlsLayout.addLayout(resultsLayout, 1, 2)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(controlsLayout)
        mainLayout.addLayout(buttonLayout, alignment=QtCore.Qt.AlignCenter)
        
            
    def addWidgetListToLayout(self, widgetList, layout):
        for i in range(len(widgetList)):
            layout.addWidget(widgetList[i])