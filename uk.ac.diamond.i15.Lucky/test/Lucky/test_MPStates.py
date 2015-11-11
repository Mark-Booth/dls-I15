'''
Created on 10 Nov 2015

@author: wnm24546
'''

import unittest

from Lucky.DataModel import MainData
from Lucky.MPStates import (LiveSetup, LiveStartable, LiveStoppable,
                            OfflineSetup, OfflineStartable, OfflineStoppable)

class MPStateTest(unittest.TestCase):
    def setUp(self):
        self.dM = MainData()
        self.state = None
    
    def tearDown(self):
        self.dM = None
    
    def stateRun(self):
        self.state.run(self.dM)

class LiveSetupTest(MPStateTest):
    def runTest(self):
        #Force opposite settings to those used in LiveSetup
        self.dM.mode = (0, 1)
        self.dM.usdsControlsEnabled = True
        self.dM.runEnabled = True
        
        self.state = LiveSetup()
        self.stateRun()
        
        self.assertEqual(self.dM.mode, (1, 0), "Live mode not set")
        self.assertEqual(self.dM.usdsControlsEnabled, False, "US/DS controls enabled")
        self.assertEqual(self.dM.runEnabled, False, "Run control enabled")
