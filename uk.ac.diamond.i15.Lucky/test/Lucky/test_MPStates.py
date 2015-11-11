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
        self.dM.stopEnabled = True
        self.dM.allUIControlsEnabled = False
        
        self.state = LiveSetup()
        
        #Check the correct transitions are present
        expectedTransitions = [State.EVENTS.DATAGOOD, State.EVENTS.OFFLINE]
        self.compareTransitions(expectedTransitions)
        
        #Do the state's action
        self.stateRun()
        
        self.assertEqual(self.dM.mode, (1, 0), "LiveSetup: Live mode not set")
        self.assertFalse(self.dM.usdsControlsEnabled, "LiveSetup: US/DS controls enabled")
        self.assertFalse(self.dM.runEnabled, "LiveSetup: Run control enabled")
        self.assertFalse(self.dM.stopEnabled, "LiveSetup: Stop control enabled")
        self.assertTrue(self.dM.allUIControlsEnabled, "LiveSetup: UI controls disabled")


class LiveStartableTest(MPStateTest):
    def runTest(self):
        #Force opposite settings to those used in LiveSetup
        self.dM.mode = (0, 1)
        self.dM.usdsControlsEnabled = True
        self.dM.runEnabled = False
        self.dM.stopEnabled = True
        self.dM.allUIControlsEnabled = False
        
        self.state = LiveStartable()
        
        #Check the correct transitions are present
        expectedTransitions = [State.EVENTS.DATABAD, State.EVENTS.OFFLINE, State.EVENTS.RUN]
        self.compareTransitions(expectedTransitions)
        
        self.stateRun()
        
        self.assertEqual(self.dM.mode, (1, 0), "LiveStartable: Live mode not set")
        self.assertFalse(self.dM.usdsControlsEnabled, "LiveStartable: US/DS controls enabled")
        self.assertTrue(self.dM.runEnabled, "LiveStartable: Run control disabled")
        self.assertFalse(self.dM.stopEnabled, "LiveStartable: Stop control enabled")
        self.assertTrue(self.dM.allUIControlsEnabled, "LiveStartable: UI controls disabled")

class LiveStoppableTest(MPStateTest):
    def runTest(self):
        #Force opposite settings to those used in LiveSetup
        self.dM.mode = (0, 1)
        self.dM.usdsControlsEnabled = True
        self.dM.runEnabled = True
        self.dM.stopEnabled = False
        self.dM.allUIControlsEnabled = True
        
        self.state = LiveStoppable()
        
        #Check the correct transitions are present
        expectedTransitions = [State.EVENTS.STOP]
        self.compareTransitions(expectedTransitions)
        
        self.stateRun()
        
        self.assertEqual(self.dM.mode, (1, 0), "LiveStoppable: Live mode not set")
        self.assertFalse(self.dM.usdsControlsEnabled, "LiveStoppable: US/DS controls enabled")
        self.assertFalse(self.dM.runEnabled, "LiveStoppable: Run control disabled")
        self.assertTrue(self.dM.stopEnabled, "LiveStoppable: Stop control enabled")
        self.assertFalse(self.dM.allUIControlsEnabled, "LiveStoppable: UI controls disabled")