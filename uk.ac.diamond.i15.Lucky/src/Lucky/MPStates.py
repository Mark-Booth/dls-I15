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
    
    def run(self, dataModel):
        assert 0, "Run not implemented"
    
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
        pass

#Live state classes
####
class LiveState(State):
    def __init__(self):
        super(LiveState, self).__init__()
    
    def run(self, dataModel):
        dataModel.mode = (1, 0)
        dataModel.usdsControlsEnabled = False

class LiveSetup(LiveState):
    def __init__(self):
        super(LiveSetup, self).__init__()
        self.name = "LiveSetup"
        self.transitions = {State.EVENTS.DATAGOOD : LiveStartable,
                            State.EVENTS.OFFLINE  : OfflineSetup}
    
    def run(self, dataModel):
        super(LiveSetup, self).run(dataModel)
        dataModel.runEnabled = False
        dataModel.stopEnabled = False
        dataModel.allUIControlsEnabled = True

class LiveStartable(LiveState):
    def __init__(self):
        super(LiveStartable, self).__init__()
        self.name = "LiveStartable"
        self.transitions = {State.EVENTS.DATABAD : LiveSetup,
                            State.EVENTS.OFFLINE : OfflineSetup,
                            State.EVENTS.RUN     : LiveStoppable}
    
    def run(self, dataModel):
        super(LiveStartable, self).run(dataModel)
        dataModel.runEnabled = True
        dataModel.stopEnabled = False
        dataModel.allUIControlsEnabled = True

class LiveStoppable(LiveState):
    def __init__(self, dM):
        super(LiveStoppable, self).__init__(dM)
        self.name = "LiveStoppable"
        self.transitions = {State.EVENTS.STOP : LiveStartable}
    
    def run(self, dataModel):
        super(LiveStoppable, self).run(dataModel)
        self.dataModel.runEnabled = False
        self.dataModel.stopEnabled = True
        self.dataModel.allUIControlsEnabled = False


#Offline state classes
####
class OfflineState(State):
    def __init__(self, dM):
        super(OfflineState, self).__init__()
    
    def run(self, dataModel):
        dataModel.mode = (0, 1)
        dataModel.usdsControlsEnabled = True

class OfflineSetup(OfflineState):
    def __init__(self):
        super(OfflineSetup, self).__init__()
        self.name = "OfflineSetup"
        self.transitions = {State.EVENTS.LIVE     : LiveSetup,
                            State.EVENTS.DATAGOOD : OfflineStartable}
    
    def run(self, dataModel):
        super(OfflineSetup, self).run(dataModel)
        dataModel.runEnabled = False

class OfflineStartable(OfflineState):
    def __init__(self):
        super(OfflineStartable, self).__init__()
        self.name = "OfflineStartable"
        self.transitions = {State.EVENTS.DATABAD : OfflineSetup,
                            State.EVENTS.LIVE    : LiveStartable,
                            State.EVENTS.RUN     : OfflineStoppable}
    
    def run(self, dataModel):
        super(OfflineStartable, self).run()
        dataModel.runEnabled = True
        dataModel.stopEnabled = False
        dataModel.allUIControlsEnabled = False

class OfflineStoppable(OfflineState):
    def __init__(self):
        super(OfflineStoppable, self).__init__()
        self.name = "OfflineStoppable"
        self.transitions = {State.EVENTS.STOP : OfflineStoppable}
    
    def run(self, dataModel):
        super(OfflineStoppable, self).run(dataModel)
        dataModel.runEnabled = False
        dataModel.stopEnabled = True
        dataModel.allUIControlsEnabled = False