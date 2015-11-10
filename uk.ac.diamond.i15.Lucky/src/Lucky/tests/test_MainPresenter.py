'''
Created on 5 Nov 2015

@author: wnm24546
'''
import unittest

import Lucky
from Lucky.LuckyExceptions import BadModelStateException

class MainPresenterTest(unittest.TestCase):
    def setUp(self):
        self.mp = Lucky.MainPresenter.MainPresenter()
    
    def tearDown(self):
        self.mp = None
        
class RunStopPressActiveChangesTest(MainPresenterTest):
    def runTest(self):
        #Set allDataPresent
        self.mp.dataModel.allDataPresent = True
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled by default')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled by default')
        
        #Activate run by toggling
        self.mp.toggleButtonStates()
        self.assertTrue(self.mp.dataModel.runEnabled, 'Run should be enabled with all data present')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled with all data present')
        
        #Activate stop, deactivate run
        self.mp.toggleButtonStates()
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled after starting')
        self.assertTrue(self.mp.dataModel.stopEnabled, 'Stop should be enabled after starting')
        
        with self.assertRaises(BadModelStateException):
            self.mp.dataModel.allDataPresent = False
            self.mp.toggleButtonStates()
        
        #Toggle again and unset allDataPresent
        self.mp.dataModel.allDataPresent = True
        self.mp.toggleButtonStates()
        self.mp.dataModel.allDataPresent = False
        self.mp.toggleButtonStates()
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled without data')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled without data')

class RunPressedAllUIChanges(MainPresenterTest):
    def runTest(self):
        self.mp.dataModel.allDataPresent = True
        self.mp.toggleButtonStates()
        
        #This is for offline-mode
        ####
        #Fake starting a run
        self.mp.doRun(test=True)
        self.assertFalse(self.mp.dataModel.allUIControlsEnabled, 'UI controls should be disabled after start')
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled after start')
        self.assertTrue(self.mp.dataModel.stopEnabled, 'Stop should be enabled after start')
        self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled during run')
        
        #Fake stopping a run
        self.mp.doStop(test=True)
        self.assertTrue(self.mp.dataModel.allUIControlsEnabled, 'UI controls should be enabled after stop')
        self.assertTrue(self.mp.dataModel.runEnabled, 'Run should be enabled after stop')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled after stop')
        self.assertTrue(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be enabled after stop')

        #This is for live-mode
        ####
        self.mp.setMode()#TODO This needs thought
        self.mp.doRun(test=True)
        self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled in live-mode')
        
        self.mp.doStop(test=True)
        self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled in live-mode')