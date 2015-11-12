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
        
    
    def getModeTransition(self):
        if self.dataModel.mode == (1, 0):
            return State.EVENTS.LIVE
        elif self.dataModel.mode == (0, 1):
            return State.EVENTS.OFFLINE
        else:
            raise BadModelStateException("Invalid mode setting detected")

class StateMachine(object):
    def __init__(self, mp):
        self.mainPres = mp
        
        #This is a slightly convoluted way to avoid importing StartState
        self.currentState = State().next(State.EVENTS.START)()
        self.currentState.run()
        self.changeState(State.EVENTS.LIVE)
        
    def changeState(self, event):
        while True:
            nextState = self.currentState.next(event)
            if nextState == self.currentState:
                break
            self.currentState = nextState()
            self.currentState.run(self.mainPres.dataModel)
    
    def getState(self):
        return self.currentState.name
