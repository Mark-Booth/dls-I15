'''
Created on 10 Nov 2015

@author: wnm24546
'''

import unittest

from Lucky.DataModel import MainData
from Lucky.MPStates import (State, LiveSetup, LiveStartable, LiveStoppable,
                            OfflineSetup, OfflineStartable, OfflineStoppable)

class MPStateTest(unittest.TestCase):
    def setUp(self):
        self.dM = MainData()
        self.state = None
    
    def tearDown(self):
        self.dM = None
    
    def stateRun(self):
        self.state.run(self.dM)
    
    def compareTransitions(self, expected):
        presentTransitions = self.state.transitions.keys()
        self.assertTrue(all(pt in expected for pt in presentTransitions), "Extra transition present!")

class LiveSetupTest(MPStateTest):
    def runTest(self):
        #Force opposite settings to those used in LiveSetup
        self.dM.mode = (0, 1)
        self.dM.usdsControlsEnabled = True
        self.dM.runEnabled = True
        
        self.state = LiveSetup()
        
        #Check the correct transitions are present
        expectedTransitions = [State.EVENTS.DATAGOOD, State.EVENTS.OFFLINE]
        self.compareTransitions(expectedTransitions)
        
        #Do the state's action
        self.stateRun()
        
        self.assertEqual(self.dM.mode, (1, 0), "Live mode not set")
        self.assertEqual(self.dM.usdsControlsEnabled, False, "US/DS controls enabled")
        self.assertEqual(self.dM.runEnabled, False, "Run control enabled")
