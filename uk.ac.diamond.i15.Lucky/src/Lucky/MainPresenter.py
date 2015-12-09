'''
Created on 5 Nov 2015

@author: wnm24546
'''

import os, re

from Lucky.MPStates import State
from Lucky.DataModel import (CalibrationConfigData, MainData)
from Lucky.LuckyExceptions import BadModelStateException, IllegalArgumentException

class AllPresenter(object):
    def __init__(self, dM = None):
        super(AllPresenter, self).__init__()
        
    def isValidPath(self, uiText, dirPath=False):
        return (dirPath and os.path.isdir(uiText)) or (not dirPath and os.path.isfile(uiText))
    
    def isValidInt(self, uiNum):
        try:
            int(uiNum)
            return True
        except ValueError:
            return False
    
    def isValidFloat(self, uiNum):
        try:
            float(uiNum)
            return True
        except ValueError:
            return False

class MainPresenter(AllPresenter):
    def __init__(self, dM = None):
        #Create the data model and the state machine
        if dM == None:
            self.dataModel = MainData()
        else:
            self.dataModel = dM
        self.stateMach = StateMachine(self)
        
    def runTrigger(self):
        self.stateMach.changeState(State.EVENTS.RUN)
        #Start a new calculation thread and kick off the calcs
    
    def stopTrigger(self):
        self.stateMach.changeState(State.EVENTS.STOP)
        #Kill the calculation thread
    
    def dataValidTrigger(self, noData=False):
        if noData:
            dataValid = not self.dataModel.allDataPresent
        else:
            dataValid = self.isDataValid()
        
        if dataValid:
            event = State.EVENTS.DATAGOOD
        else:
            event = State.EVENTS.DATABAD
        self.stateMach.changeState(event)
    
    def setModeTrigger(self, uiData):
        self.stateMach.changeState(self.getModeTransition(uiData))
        #No return as this is a radio button option
        
        print str(self.stateMach.getStateName())
    
    def setCalibTypeTrigger(self, uiData):
        if sum(uiData) != 1:
            raise BadModelStateException("Only one calibration option can be selected")
        self.dataModel.calibType = uiData
        #No return as this is a radio button option
        
        print self.dataModel.calibType
    
    def changeDataDirTrigger(self, uiText):
        self.dataModel.dataDir = str(uiText)
        self.dataModel.calibConfigData.calibDir = str(uiText)
        if self.isValidPath(uiText, dirPath=True):
            self.dataModel.dataValid['dataDir'] = True
            self.dataModel.calibConfigData.calibValid['calibDir'] = True
            return True
        else:
            self.dataModel.dataValid['dataDir'] = False
            return False
    
    def changeIntegrationConfigTrigger(self, uiNumbs):
        intUINumbs = []
        for val in uiNumbs:
            if not self.isValidInt(val):
                return False
            intUINumbs.append(int(val))
        
        self.dataModel.integrationConf = intUINumbs
        if ((intUINumbs[0] < intUINumbs[1]) and (intUINumbs[2] < (intUINumbs[1] - intUINumbs[0]))):
            self.dataModel.dataValid['integrationConf'] = True
            return True
        else:
            self.dataModel.dataValid['integrationConf'] = False
            return False
    
    def calibConfigUpdateTrigger(self, calibConfig, validity):
        self.dataModel.calibConfigData = calibConfig
        self.dataModel.dataValid['calibConfig'] = validity
    
    def changeUSDSPairTrigger(self, inc=False, dec=False, dsFile=None, usFile=None):
        #Catch malformed args
        if (inc and dec) or ((inc or dec) and (dsFile != None or usFile != None)):
            raise IllegalArgumentException("Cannot inc/decrement together and/or change filenames")
        
        if dsFile != None:
            dsFile = str(dsFile)
            try:
                dsNewPath = os.path.join(self.dataModel.dataDir, dsFile)
            except:
                return False
            if self.isValidPath(dsNewPath, False):
                self.dataModel.usdsPair[0] = dsNewPath
                self.dataModel.dataValid['dsFile'] = True
                return True
            else:
                self.dataModel.dataValid['dsFile'] = False
                return False
        if usFile != None:
            usFile = str(usFile)
            try:
                usNewPath = os.path.join(self.dataModel.dataDir, usFile)
            except:
                return False
            if self.isValidPath(usNewPath, False):
                self.dataModel.usdsPair[1] = usNewPath
                self.dataModel.dataValid['usFile'] = True
                return True
            else:
                self.dataModel.dataValid['usFile'] = False
                return False
        
        if inc or dec:
            def shiftFileName(usdsIndex, shiftVal):
                #Regular expression to match file name of the format:
                #    A_#_#.txt
                rePatt = re.compile("([a-zA-Z]+)(_+)([0-9]+)(_+)([0-9]+)(\.txt$)")
                filePath = os.path.basename(self.dataModel.usdsPair[usdsIndex])
                filePathParts = list(rePatt.match(filePath).groups())
                fileNr = int(filePathParts[2])
                filePathParts[2] = str(fileNr + shiftVal)
                return ''.join(filePathParts)
            
            newUSDSPair = ['', '']
            for i in range(2):
                if dec:
                    newUSDSPair[i] = shiftFileName(i, -1)
                if inc:
                    newUSDSPair[i] = shiftFileName(i, 1)
                
                newUSDSPair[i] = os.path.join(self.dataModel.dataDir, newUSDSPair[i])
            self.dataModel.usdsPair = newUSDSPair
            
            return True #This should just be ignored...
    
    def isDataValid(self):
        if (all(val == True for val in self.dataModel.dataValid.values())):
            return True
        elif self.dataModel.calibType == (1,0,0):
            if (self.dataModel.calibConfigData.calibValid['(US)'] and self.dataModel.calibConfigData.calibValid['(DS)']):
                return True
        elif self.dataModel.calibType == (0,1,0):
            if (self.dataModel.calibConfigData.calibValid['F1 (US)'] and self.dataModel.calibConfigData.calibValid['F1 (DS)']):
                return True
        elif self.dataModel.calibType == (0,0,1):
            if (self.dataModel.calibConfigData.calibValid['F2 (US)'] and self.dataModel.calibConfigData.calibValid['F2 (DS)']):
                return True
        return False
    
    def getModeTransition(self, inputMode=None):
        if inputMode == None:
            inputMode = self.dataModel.mode
        
        if inputMode == (1, 0):
            self.dataModel.dataValid['dsFile'] = True
            self.dataModel.dataValid['usFile'] = True #We won't have this to start, must be true
            return State.EVENTS.LIVE
        elif inputMode == (0, 1):
            #Check validity of current US/DS pair
            for i in range(2):
                usdsLabel = 'dsFile' if i == 0 else 'usFile'
                if self.isValidPath(self.dataModel.usdsPair[0], False):
                    self.dataModel.dataValid[usdsLabel] = True
                else:
                    self.dataModel.dataValid[usdsLabel] = False
            return State.EVENTS.OFFLINE
        else:
            raise BadModelStateException("Invalid mode setting detected")
    
    def getSMStateName(self):
        return self.stateMach.getStateName()
    
    def getSMState(self):
        return self.stateMach.currentState

####

class CalibPresenter(AllPresenter):
    def __init__(self, cM = None):
        #Create the data model and the state machine
        if cM == None:
            self.calibModel = CalibrationConfigData()
        else:
            self.calibModel = cM
            
    def changeCalibDirTrigger(self, uiText):
        if self.isValidPath(uiText, dirPath=True):
            self.calibModel.calibDir = uiText
            self.calibModel.calibValid['calibDir'] = True
            return True
        else:
            self.calibModel.calibValid['calibDir'] = False
            return False
    
    def changeCalibFileTrigger(self, uiText, calibId):
        if self.isValidPath(uiText, dirPath=False):
            self.calibModel.calibFiles[calibId] = uiText
            self.calibModel.calibValid[calibId] = True
            return True
        else:
            self.calibModel.calibValid[calibId] = False
            return False
    
    def changeBulbTempTrigger(self, uiText):
        if (self.isValidInt(uiText) or self.isValidFloat(uiText)) and (float(uiText) >= 0):
            self.calibModel.bulbTemp = float(uiText)
            self.calibModel.calibValid['bulbTemp'] = True
            return True
        else:
            self.calibModel.calibValid['bulbTemp'] = False
            return False
    
    def isValidConfig(self):
        return all(val == True for val in self.calibModel.calibValid.values())

####

class StateMachine(object):
    def __init__(self, mp):
        self.mainPres = mp
        
        #This is a slightly convoluted way to avoid importing StartState
        self.currentState = State().next(State.EVENTS.START)()
        self.currentState.run()
        
        #Set the StateMachine based on the dataModel of the mainPres
        self.changeState(self.mainPres.getModeTransition())
        
    def changeState(self, event):
        while True:
            nextState = self.currentState.next(event)
            if nextState == type(self.currentState):
                break
            self.currentState = nextState()
            self.currentState.run(self.mainPres.dataModel)
    
    def getStateName(self):
        return self.currentState.name


