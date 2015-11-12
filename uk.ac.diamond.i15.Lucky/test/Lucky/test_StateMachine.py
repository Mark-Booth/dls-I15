'''
Created on 11 Nov 2015

@author: wnm24546
'''
import unittest

from Lucky.MainPresenter import StateMachine
from Lucky.DataModel import MainData

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

class GetStateTest(FSMTest):
    def runTest(self):
        self.assertEqual(self.fsm.getState(), "LiveSetup")

class StateChangesTest(FSMTest):
    def runTest(self):
        pass

