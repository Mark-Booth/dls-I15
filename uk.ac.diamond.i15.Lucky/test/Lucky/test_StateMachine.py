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
        self.fsm = StateMachine(self.dM)

    def tearDown(self):
        self.dM = None
        self.fsm = None

class GetStateTest(FSMTest):
    def runTest(self):
        self.assertEqual(self.fsm.getState(), "LiveSetup")

class StateChangesTest(FSMTest):
    def runTest(self):
        pass

