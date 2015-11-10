'''
Created on 10 Nov 2015

@author: wnm24546
'''

import unittest

from Lucky.DataModel import MainData
from Lucky.MPStates import (LiveSetup, OfflineSetup)

class MPStateTest(unittest.TestCase):
    def setUp(self):
        self.dM = MainData()
        self.mpState = OfflineSetup(self.dM)
    
    def tearDown(self):
        self.dM = None
        self.mpState = None

class LiveTransitionsTest(MPStateTest):
    def runTest(self):
        self.assertEqual(self.mpState.__class__, OfflineSetup.__class__, 'Unexpected initial state')
        #self.mpState.changeState(self.mpState.ACTIONS.DATAGOOD)
