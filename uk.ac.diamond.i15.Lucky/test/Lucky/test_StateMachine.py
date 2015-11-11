'''
Created on 11 Nov 2015

@author: wnm24546
'''
import unittest

from Lucky.MainPresenter import StateMachine

class FSMTest(unittest.TestCase):
    def setUp(self):
        self.fsm = StateMachine()

    def tearDown(self):
        self.fsm = None

class GetStateTest(FSMTest):
    def runTest(self):
        self.assertEqual(self.fsm.getState(), "LiveSetup")

