'''
Created on 5 Nov 2015

@author: wnm24546
'''

from MPStates import State
from DataModel import (CalibrationConfigData, MainData)
from LuckyExceptions import BadModelStateException

class MainPresenter(object):
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
    
    def setCalibTypeTrigger(self, uiData):
        self.dataModel.calibType = uiData
    
    def isDataValid(self):
        return None
    
    def getModeTransition(self, inputMode=None):
        if inputMode == None:
            inputMode = self.dataModel.mode
        
        if inputMode == (1, 0):
            return State.EVENTS.LIVE
        elif inputMode == (0, 1):
            return State.EVENTS.OFFLINE
        else:
            raise BadModelStateException("Invalid mode setting detected")
    
    def getSMStateName(self):
        return self.stateMach.getStateName()
    
    def getSMState(self):
        return self.stateMach.currentState
    

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
