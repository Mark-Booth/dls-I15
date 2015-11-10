'''
Created on 9 Nov 2015

@author: wnm24546
'''

from enum import Enum

from Lucky.LuckyExceptions import BadModelStateException

class PresenterState(object):
    def __init__(self, dataModel):
        self.dataModel = dataModel
        self.ACTIONS = Enum('ACTIONS', 
            'LIVE OFFLINE DATAGOOD DATABAD START STOP')
    
    def changeState(self, action):
        if self.transitions.has_key(action):
            return self.transitions[action]
        else:
            raise BadModelStateException("Invalid state change")

class LiveState(PresenterState):
    def __init__(self, dataModel):
        super(LiveState, self).__init__(dataModel)
        self.dataModel.mode = (1, 0)
        self.dataModel.usdsControlsEnabled = False

class OfflineState(PresenterState):
    def __init__(self, dataModel):
        super(OfflineState, self).__init__(dataModel)
        self.dataModel.mode = (0, 1)
        self.dataModel.usdsControlsEnabled = True
    
class LiveSetup(LiveState):
    def __init__(self, dataModel):
        super(LiveSetup, self).__init__(dataModel)
        self.dataModel.runEnabled = False
        
        self.transitions = {self.ACTIONS.OFFLINE : OfflineSetup(self.dataModel),
                            self.ACTIONS.DATAGOOD: LiveStartable(self.dataModel)}
    
class LiveStartable(LiveState):
    def __init__(self, dataModel):
        super(LiveStartable, self).__init__(dataModel)
        self.dataModel.runEnabled = True
        self.dataModel.stopEnabled = False
        self.allUIControlsEnabled = False
        
        self.transitions = {self.ACTIONS.OFFLINE : OfflineStartable(self.dataModel),
                            self.ACTIONS.DATABAD : LiveStartable(self.dataModel),
                            self.ACTIONS.START : LiveStoppable(self.dataModel)}
    
class LiveStoppable(LiveState):
    def __init__(self, dataModel):
        super(LiveStoppable, self).__init__(dataModel)
        self.dataModel.runEnabled = False
        self.dataModel.stopEnabled = True
        self.dataModel.allUIControlsEnabled = False
        
        self.transitions = {self.ACTIONS.STOP : LiveStartable(self.dataModel)}
        
        print "Running calculations live"

class OfflineSetup(OfflineState):
    def __init__(self, dataModel):
        super(OfflineSetup, self).__init__(dataModel)
        self.dataModel.runEnabled = False
        
        self.transitions = {self.ACTIONS.LIVE : LiveSetup(self.dataModel),
                            self.ACTIONS.DATAGOOD: OfflineStartable(self.dataModel)}
    

class OfflineStartable(OfflineState):
    def __init__(self, dataModel):
        super(OfflineStartable, self).__init__(dataModel)
        self.dataModel.runEnabled = True
        self.dataModel.stopEnabled = False
        self.allUIControlsEnabled = False
        
        self.transitions = {self.ACTIONS.LIVE : LiveStartable(self.dataModel),
                            self.ACTIONS.DATABAD : OfflineSetup(self.dataModel),
                            self.ACTIONS.START : OfflineStoppable(self.dataModel)}
    
class OfflineStoppable(OfflineState):
    def __init__(self, dataModel):
        super(OfflineStoppable, self).__init__(dataModel)
        self.dataModel.runEnabled = False
        self.dataModel.stopEnabled = True
        self.dataModel.allUIControlsEnabled = False
        
        self.transitions = {self.ACTIONS.STOP : self.dataModel.offlineStart}
        
        print "Running calculations offline"
    
