'''
Created on 4 Nov 2015

@author: wnm24546
'''

from PyQt4.QtGui import (QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QRadioButton, QVBoxLayout, QWidget)
from PyQt4 import QtCore

import os

#from Lucky import CalibrationConfigView
from Lucky.MainPresenter import MainPresenter

class MainView(QWidget):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setWindowTitle("Lucky")
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        self.presenter = MainPresenter()
        
        self.setupUI()
        self.updateWidgetStates(self.presenter.dataModel)
        
    def setupUI(self):
        ####
        #Creation of supporting layouts
        baseLayout = QVBoxLayout()
        controlsLayout = QGridLayout() #This is everything except the buttons
        
        ####
        #Mode controls
        modeGrpBox = QGroupBox("Mode:")
        self.modeRadBtns = [QRadioButton("Live"),
                            QRadioButton("Offline")]
        for radBtn in self.modeRadBtns:
            radBtn.clicked.connect(self.modeRadBtnClick)
        modeLayout = QHBoxLayout()
        self.addWidgetListToLayout(self.modeRadBtns, modeLayout)
        modeGrpBox.setLayout(modeLayout)
        controlsLayout.addWidget(modeGrpBox, 0, 0)
        
        ####
        #Calib controls
        calibLayout = QVBoxLayout()
        calibGrpBox = QGroupBox("Calibration Type:")
        self.calibRadBtns = [QRadioButton("Calibration"),
                             QRadioButton("Calibration F1"),
                             QRadioButton("Calibration F2")]
        for radBtn in self.calibRadBtns:
            radBtn.clicked.connect(self.calibRadBtnClick)
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
        self.dataDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.dataDirTextBox.textChanged.connect(self.dataDirChanged)
        self.browseDataDirBtn = QPushButton("Browse...")
        self.browseDataDirBtn.clicked.connect(self.dataDirBrowseBtnClick)
        
        dataDirLayout = QHBoxLayout()
        dataDirLayout.addWidget(self.dataDirTextBox)
        dataDirLayout.addWidget(self.browseDataDirBtn)
        dataDirGrpBox.setLayout(dataDirLayout)
        controlsLayout.addWidget(dataDirGrpBox, 0, 1, 1, 2)
        
        ####
        #US/DS selector
        fileGrpBox = QGroupBox("Measurement Number (US/DS pair):")
        self.prevUSDSPairBtn = QPushButton("<")
        self.nextUSDSPairBtn = QPushButton(">")
        self.currUSDSPairTextBox = QLineEdit()#Default needs to be set from the model!
        
        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.prevUSDSPairBtn)
        fileLayout.addWidget(self.currUSDSPairTextBox)
        fileLayout.addWidget(self.nextUSDSPairBtn)
        fileGrpBox.setLayout(fileLayout)
        controlsLayout.addWidget(fileGrpBox, 1, 1, 1, 2)
        
        ###
        #Integration range
        integrationTextInputWidth = 40
        startLabel = QLabel("Beginning:")
        self.integStartTextBox = QLineEdit()#Default needs to be set from the model!
        self.integStartTextBox.setFixedWidth(integrationTextInputWidth)
        self.integStartTextBox.textChanged.connect(self.integConfigChanged)
        stopLabel = QLabel("End:")
        self.integStopTextBox = QLineEdit()#Default needs to be set from the model!
        self.integStopTextBox.setFixedWidth(integrationTextInputWidth)
        self.integStopTextBox.textChanged.connect(self.integConfigChanged)
        deltaLabel = QLabel("Window Size:")
        self.integDeltaTextBox = QLineEdit()#Default needs to be set from the model!
        self.integDeltaTextBox.setFixedWidth(integrationTextInputWidth)
        self.integDeltaTextBox.textChanged.connect(self.integConfigChanged)
        nmLabel1, nmLabel2, nmLabel3 = QLabel("nm"), QLabel("nm"), QLabel("nm")
        
        integRangeGrpBox = QGroupBox("Integration Range:")
        integRangeLayout = QGridLayout()
        integRangeLayout.addWidget(startLabel, 0, 0)
        integRangeLayout.addWidget(self.integStartTextBox, 0, 1)
        integRangeLayout.addWidget(nmLabel1, 0, 2)
        integRangeLayout.addWidget(stopLabel, 0, 3)
        integRangeLayout.addWidget(self.integStopTextBox, 0, 4)
        integRangeLayout.addWidget(nmLabel2, 0, 5)
        integRangeLayout.addWidget(deltaLabel, 1, 0)
        integRangeLayout.addWidget(self.integDeltaTextBox, 1, 1)
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
        #Add the 1st tier layouts & set the base layout
        baseLayout.addLayout(controlsLayout)
        baseLayout.addLayout(buttonLayout)
        self.setLayout(baseLayout)

###        
    def addWidgetListToLayout(self, widgetList, layout):
        for i in range(len(widgetList)):
            layout.addWidget(widgetList[i])
            
    def getRadBtnStates(self, btnList):
        return tuple([int(radBtn.isChecked()) for radBtn in btnList])
            
    def modeRadBtnClick(self):
        self.presenter.setModeTrigger(self.getRadBtnStates(self.modeRadBtns))
        self.updateWidgetStates()
              
    def calibRadBtnClick(self):
        self.presenter.setCalibTypeTrigger(self.getRadBtnStates(self.calibRadBtns))
        self.updateWidgetStates()
        
    def calibConfClick(self):
        self.calibConfInput = CalibrationConfigView(self)
        self.calibConfInput.exec_()
    
    def dataDirChanged(self):
        textBox = self.sender()
        if self.presenter.changeDataDirTrigger(textBox.text()):
            textBox.setStyleSheet("color: rgb(0, 0, 0);")
        else:
            textBox.setStyleSheet("color: rgb(255, 0, 0);")
    
    def dataDirBrowseBtnClick(self):
        currDir = self.presenter.dataModel.dataDir
        newDir = str(self.showDirBrowserDialog(initDir=currDir, caption="Select a new data directory"))
        self.dataDirTextBox.setText(newDir)
        0
        #self.dataDirChanged()
    
    def integConfigChanged(self):
        textBox = self.sender()
        if self.presenter.isValidInt(textBox.text()):
            integConfig = [self.integStartTextBox.text(),
                           self.integStopTextBox.text(),
                           self.integDeltaTextBox.text()] 
            if self.presenter.changeIntegrationConfigTrigger(integConfig):
                self.integStartTextBox.setStyleSheet("color: rgb(0, 0, 0);")
                self.integStopTextBox.setStyleSheet("color: rgb(0, 0, 0);")
                self.integDeltaTextBox.setStyleSheet("color: rgb(0, 0, 0);")
            else:
                self.integStartTextBox.setStyleSheet("color: rgb(255, 0, 0);")
                self.integStopTextBox.setStyleSheet("color: rgb(255, 0, 0);")
                self.integDeltaTextBox.setStyleSheet("color: rgb(255, 0, 0);")
        else:
            textBox.setStyleSheet("color: rgb(255, 0, 0);")
###
    def updateWidgetStates(self, extraData=None):
        mainData = self.presenter.dataModel if (extraData == None) else extraData
        
        #Mode radio buttons
        for i in range(len(self.modeRadBtns)):
            self.modeRadBtns[i].setEnabled(mainData.allUIControlsEnabled)
            self.modeRadBtns[i].setChecked(mainData.mode[i])
        
        #Calibration type radio buttons
        for i in range(len(self.calibRadBtns)):
            self.calibRadBtns[i].setEnabled(mainData.allUIControlsEnabled)
            self.calibRadBtns[i].setChecked(mainData.calibType[i])
        
        #Datadir
        
        
        #US/DS pair
        self.prevUSDSPairBtn.setEnabled((mainData.allUIControlsEnabled) and (mainData.usdsControlsEnabled))
        self.nextUSDSPairBtn.setEnabled((mainData.allUIControlsEnabled) and (mainData.usdsControlsEnabled))
        self.currUSDSPairTextBox.setEnabled((mainData.allUIControlsEnabled) and (mainData.usdsControlsEnabled))
        
        #Integration controls
        self.integStartTextBox.setEnabled(mainData.allUIControlsEnabled)
        self.integStartTextBox.setText(str(mainData.integrationConf[0]))
        self.integStopTextBox.setEnabled(mainData.allUIControlsEnabled)
        self.integStopTextBox.setText(str(mainData.integrationConf[1]))
        self.integDeltaTextBox.setEnabled(mainData.allUIControlsEnabled)
        self.integDeltaTextBox.setText(str(mainData.integrationConf[2]))
        
        ###
        #Buttons
        self.runBtn.setEnabled(mainData.runEnabled)
        self.stopBtn.setEnabled(mainData.stopEnabled)
    
    ###
    
    def showDirBrowserDialog(self, initDir=None, caption="Choose a directory"):
        if (initDir == None):
            initDir = os.path.expanduser("~")
        return QFileDialog.getExistingDirectory(self, directory=initDir, caption=caption)
    


#####################################


class CalibrationConfigView(QDialog):

    def __init__(self, parent_widget):
        super(CalibrationConfigView, self).__init__(parent=parent_widget)
        self.setWindowTitle("Configure Calibration")
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))
        
        self.setupUI()
    
    def setupUI(self):
        ####
        #Creation of supporting layouts
        baseLayout = QVBoxLayout()
        
        ####
        #Select the base directory to look for calibration files
        calibDirGrpBox = QGroupBox("Calibration Directory:")
        self.calibDirTextBox = QLineEdit()#Default needs to be set from the model!
        self.browseCalibDirBtn = QPushButton("Browse...")
        calibDirLayout = QHBoxLayout()
        calibDirLayout.addWidget(self.calibDirTextBox)
        calibDirLayout.addWidget(self.browseCalibDirBtn)
        calibDirGrpBox.setLayout(calibDirLayout)
        baseLayout.addWidget(calibDirGrpBox)
        
        ####
        #Select specific calibration file names to use
        calibFileGrpBox = QGroupBox("Calibration Files:")
        calibFileLabels = [[QLabel("Calibration (US):"), QLabel("Calibration (DS):")],
                           [QLabel("Calibration F1 (US):"), QLabel("Calibration F1 (DS):")],
                           [QLabel("Calibration F2 (US):"), QLabel("Calibration F2 (DS):")]]
        self.calibFileTextBoxes = [[QLineEdit(), QLineEdit()], 
                                   [QLineEdit(), QLineEdit()],
                                   [QLineEdit(), QLineEdit()]]#These will be relative names, populated from model
        self.calibFileBrowseBtns = [[QPushButton("Browse..."), QPushButton("Browse...")],
                                    [QPushButton("Browse..."), QPushButton("Browse...")],
                                    [QPushButton("Browse..."), QPushButton("Browse...")]]
        calibFileLayout = QGridLayout()
        for i in range(len(calibFileLabels)):
            for j in range(len(calibFileLabels[i])):
                calibFileLayout.addWidget(calibFileLabels[i][j], (2 * i), (2 * j), 1, 2)
                calibFileLayout.addWidget(self.calibFileTextBoxes[i][j], ((2 * i) + 1), (2 * j))
                calibFileLayout.addWidget(self.calibFileBrowseBtns[i][j], ((2 * i) + 1), ((2 * j) + 1))            
        calibFileGrpBox.setLayout(calibFileLayout)
        baseLayout.addWidget(calibFileGrpBox)
        
        ####
        #Define temperature of bulb used for calibration
        bulbTLabel = QLabel("Bulb Temperature:")
        self.calibTempTextBox = QLineEdit()#Populate from model
        self.calibTempTextBox.setFixedWidth(40)#Same as integrationTextInputWidth in MainView
        kTempLabel = QLabel("K")
        calibTempLayout = QHBoxLayout()
        calibTempLayout.addWidget(bulbTLabel)
        calibTempLayout.addWidget(self.calibTempTextBox)
        calibTempLayout.addWidget(kTempLabel)
        calibTempLayout.addStretch(1)
        baseLayout.addLayout(calibTempLayout)
        
        ####
        #Buttons to accept/reject dialog
        okCancelBtnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        okCancelBtnBox.accepted.connect(self.okClick)
        okCancelBtnBox.rejected.connect(self.cancelClick)
        baseLayout.addWidget(okCancelBtnBox)
        
        ####
        #Set the base layout
        self.setLayout(baseLayout)
        
    def okClick(self):
        print "OK!"
        self.accept()
         
     
    def cancelClick(self):
        print "Cancel"
        self.reject()
