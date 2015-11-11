'''
Created on 5 Nov 2015

@author: wnm24546
'''

from MPStates import State

class MainPresenter(object):
    def __init__(self):
        pass

class StateMachine(object):
    def __init__(self):
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
            self.currentState.run()
    
    def getState(self):
        return self.currentState.name
