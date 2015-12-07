'''
Created on 5 Nov 2015

@author: wnm24546
'''

import os

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
        if self.isValidPath(uiText, dirPath=True):
            self.dataModel.dataDir = uiText
            self.dataModel.dataValid['dataDir'] = True
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
        
        if ((intUINumbs[0] < intUINumbs[1]) and (intUINumbs[2] < (intUINumbs[1] - intUINumbs[0]))):
            self.dataModel.integrationConf = intUINumbs
            self.dataModel.dataValid['integrationConf'] = True
            return True
        else:
            self.dataModel.dataValid['integrationConf'] = False
            return False
    
    def calibConfigUpdateTrigger(self, calibConfig):
        pass
    
    def changeUSDSPairTrigger(self, inc=False, dec=False, pairNr=False):
        if pairNr is not False and not (inc or dec):
            if pairNr >= 0:
                self.dataModel.usdsPair = pairNr
                return True
            else:
                return False
        
        if inc and not (dec or pairNr is not False):
            usdsPair = self.dataModel.usdsPair + 1
            return self.changeUSDSPairTrigger(pairNr=usdsPair)
        
        if dec and not (inc or pairNr is not False):
            usdsPair = self.dataModel.usdsPair - 1
            return self.changeUSDSPairTrigger(pairNr=usdsPair)
        
        raise IllegalArgumentException("Found none of inc, dec or a pairNr value")
#         if not(inc or dec):
#             if pairNr < 0:
#                 return False
#             else:
#                 self.dataModel.usdsPair = pairNr
#         
#         if inc and not(dec and pairNr < 0):
#             
#             
#             
#             else:
#                 raise IllegalArgumentException("Found none of inc, dec or a pairNr value")
#         if 
#         
#         if pairNr >= 0:
#             
#             return True
#         if inc:
            
    
    def isDataValid(self):
        return None
    
    def getModeTransition(self, inputMode=None):
        if inputMode == None:
            inputMode = self.dataModel.mode
        
        if inputMode == (1, 0):
            self.dataModel.dataValid['usdsPair'] = True #We won't have this to start, must be true
            return State.EVENTS.LIVE
        elif inputMode == (0, 1):
            #TODO Need to check validity of current pair
            self.dataModel.dataValid['usdsPair'] = False
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
            self.dataModel = cM
    
    def changeCalibFileTrigger(self, uiText, fileId):
        if self.isValidPath(uiText, dirPath=False):
            self.calibModel.calibFiles[fileId[0]][fileId[1]] = uiText
            self.calibModel.calibValid[self.calibModel.calibFileLabels.get(fileId)] = True
            return True
        else:
            self.calibModel.calibValid[self.calibModel.calibFileLabels.get(fileId)] = False
            return False

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


