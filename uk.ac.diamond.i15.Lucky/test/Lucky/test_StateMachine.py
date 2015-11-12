'''
Created on 11 Nov 2015

@author: wnm24546
'''
import unittest

from Lucky.MainPresenter import StateMachine
from Lucky.DataModel import MainData
from Lucky.MPStates import State

class FSMTest(unittest.TestCase):
    def setUp(self):
        self.dM = MainData()
        self.mp = MockMainPresenter(self.dM)
        self.fsm = StateMachine(self.mp)

    def tearDown(self):
        self.dM = None
        self.fsm = None
        
class MockMainPresenter(object):
    def __init__(self, dM):
        self.dataModel = dM
    
    def getModeTransition(self):
        return State.EVENTS.LIVE

class GetStateTest(FSMTest):
    def runTest(self):
        self.assertEqual(self.fsm.getStateName(), "LiveSetup")

class StateChangesTest(FSMTest):
    def runTest(self):
        self.assertEqual(self.fsm.getStateName(), "LiveSetup")
        
        #Set state to LiveStartable
        self.fsm.changeState(State.EVENTS.DATAGOOD)
        self.assertEqual(self.fsm.getStateName(), "LiveStartable")
        
        #Set state to LiveStoppable
        self.fsm.changeState(State.EVENTS.RUN)
        self.assertEqual(self.fsm.getStateName(), "LiveStoppable")
        
        #Fail to set state to OfflineStoppable
        self.fsm.changeState(State.EVENTS.OFFLINE)
        self.assertEqual(self.fsm.getStateName(), "LiveStoppable")
        
        #Set state to LiveStartable
        self.fsm.changeState(State.EVENTS.STOP)
        self.assertEqual(self.fsm.getStateName(), "LiveStartable")
        
        #Set state to OfflineStartable
        self.fsm.changeState(State.EVENTS.OFFLINE)
        self.assertEqual(self.fsm.getStateName(), "OfflineStartable")
        
        #Set state to OfflineStoppable
        self.fsm.changeState(State.EVENTS.RUN)
        self.assertEqual(self.fsm.getStateName(), "OfflineStoppable")
        0
        
        #Set state to OfflineStartable
        self.fsm.changeState(State.EVENTS.STOP)
        self.assertEqual(self.fsm.getStateName(), "OfflineStartable")
        0
        
        #Set state to OfflineSetup
        self.fsm.changeState(State.EVENTS.DATABAD)
        self.assertEqual(self.fsm.getStateName(), "OfflineSetup")
        0
        
        #Fail to set state to OfflineStoppable
        self.fsm.changeState(State.EVENTS.RUN)
        self.assertEqual(self.fsm.getStateName(), "OfflineSetup")
    
