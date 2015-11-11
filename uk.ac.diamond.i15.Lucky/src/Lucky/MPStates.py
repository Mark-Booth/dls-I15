'''
Created on 11 Nov 2015

@author: wnm24546
'''

from enum import Enum

class State(object):
    EVENTS = Enum("EVENTS", "START LIVE OFFLINE DATAGOOD DATABAD RUN STOP")
    
    def __init__(self):
        self.name = None
        self.transitions = {State.EVENTS.START : StartState}
    
    def run(self):
        assert 0, "Run not implemented"
        return True
    
    def next(self, event):
        if event in self.transitions:
            return self.transitions[event]
        else:
            return self

class StartState(State):
    def __init__(self):
        super(StartState, self).__init__()
        self.name = "Start"
        self.transitions = {State.EVENTS.LIVE : LiveSetup}
    
    def run(self):
        print "I am in start state"

class LiveSetup(State):
    def __init__(self):
        super(LiveSetup, self).__init__()
        self.name = "LiveSetup"
        self.transitions = {State.EVENTS.DATAGOOD : LiveStartable}
    
    def run(self):
        self.next(self.EVENTS.DATAGOOD)

class LiveStartable(State):
    def __init__(self):
        super(State, self).__init__()
        self.name = "LiveStartable"
        self.transitions = {State.EVENTS.DATABAD : LiveSetup}
    
    def run(self):
        print "I am in start mode"

