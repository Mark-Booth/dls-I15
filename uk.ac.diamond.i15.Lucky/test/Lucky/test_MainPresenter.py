'''
Created on 5 Nov 2015

@author: wnm24546
'''
import unittest

import Lucky
from Lucky.LuckyExceptions import BadModelStateException
from Lucky.DataModel import (CalibrationConfigData, MainData)
from Lucky.MainPresenter import MainPresenter
from Lucky.MPStates import State

class MainPresenterTest(unittest.TestCase):
    def setUp(self):
        self.mp = MainPresenter()
    
    def tearDown(self):
        self.mp = None

class StartupModeTest(MainPresenterTest):
    def runTest(self):
        #Reset the Main Presenter to be our own object.
        dM = MainData(mode=(0, 1))
        self.mp = MainPresenter(dM=dM)
        self.assertEqual(self.mp.getModeTransition(), State.EVENTS.OFFLINE, "Expected offline, got live transition")
        
        dM = MainData(mode=(1, 0))
        self.mp = MainPresenter(dM=dM)
        self.assertEqual(self.mp.getModeTransition(), State.EVENTS.LIVE, "Expected live, got offline transition")

class GetStateTest(MainPresenterTest):
    def runTest(self):
        self.assertEqual(self.mp.getSMStateName(), "OfflineSetup", "Expected OfflineSetup at startup")
   
class DataValidRunStopStateChangesTest(MainPresenterTest):
    def runTest(self):
        #Set allDataPresent
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled by default')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled by default')
         
        #Check all data valid: Activate run by toggling
        self.mp.dataValidTrigger()
        self.assertTrue(self.mp.dataModel.runEnabled, 'All data valid: Run should be enabled')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'All data valid: Stop should be disabled')
         
        #Press run: Activate stop, deactivate run
        self.mp.runTrigger()
        self.assertFalse(self.mp.dataModel.runEnabled, 'Run triggered: Run should be disabled')
        self.assertTrue(self.mp.dataModel.stopEnabled, 'Run triggered: Stop should be enabled')
        
        #Press stop: Activate run, deactivate stop
        self.mp.stopTrigger()
        self.assertTrue(self.mp.dataModel.runEnabled, 'Stop triggered: Run should be disabled')
        self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop triggered: Stop should be enabled')
        
        
#         with self.assertRaises(BadModelStateException):
#             self.mp.dataModel.allDataPresent = False
#             self.mp.toggleButtonStates()
#          
#         #Toggle again and unset allDataPresent
#         self.mp.dataModel.allDataPresent = True
#         self.mp.toggleButtonStates()
#         self.mp.dataModel.allDataPresent = False
#         self.mp.toggleButtonStates()
#         self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled without data')
#         self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled without data')

class RunPressedAllUIChangesTest(MainPresenterTest):
    pass
#     def runTest(self):
#         self.mp.dataModel.allDataPresent = True
#         self.mp.toggleButtonStates()
#         
#         #This is for offline-mode
#         ####
#         #Fake starting a run
#         self.mp.doRun(test=True)
#         self.assertFalse(self.mp.dataModel.allUIControlsEnabled, 'UI controls should be disabled after start')
#         self.assertFalse(self.mp.dataModel.runEnabled, 'Run should be disabled after start')
#         self.assertTrue(self.mp.dataModel.stopEnabled, 'Stop should be enabled after start')
#         self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled during run')
#         
#         #Fake stopping a run
#         self.mp.doStop(test=True)
#         self.assertTrue(self.mp.dataModel.allUIControlsEnabled, 'UI controls should be enabled after stop')
#         self.assertTrue(self.mp.dataModel.runEnabled, 'Run should be enabled after stop')
#         self.assertFalse(self.mp.dataModel.stopEnabled, 'Stop should be disabled after stop')
#         self.assertTrue(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be enabled after stop')
# 
#         #This is for live-mode
#         ####
#         self.mp.setMode()#TODO This needs thought
#         self.mp.doRun(test=True)
#         self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled in live-mode')
#         
#         self.mp.doStop(test=True)
#         self.assertFalse(self.mp.dataModel.usdsControlsEnabled, 'US/DS pair selector should be disabled in live-mode')
        
class UpdateTextFieldTest(MainPresenterTest):
    def runTest(self):
        #Needs to test getting string from text box or from browse button
        pass
    
class ModeSettingTest(MainPresenterTest):
    def runTest(self):
        self.assertEqual(self.mp.getSMStateName(), "OfflineSetup", "Expected OfflineSetup at startup")
        
        #Set to live setup
        uiData = (1, 0)
        self.mp.setModeTrigger(uiData)
        self.assertEqual(self.mp.getSMStateName(), "LiveSetup")
        
        #Set to offline setup
        uiData = (0, 1)
        self.mp.setModeTrigger(uiData)
        self.assertEqual(self.mp.getSMStateName(), "OfflineSetup")
        
        
class CalibrationTypeSettingTest(MainPresenterTest):
    def runTest(self):
        #Receive state from UI, check only one active, update model
        pass

class USDSPairSelectionTest(MainPresenterTest):
    def runTest(self):
        #Needs to test incrementing, decrement; needs to test getting string directly from text box
        pass

class CalibrationConfigUpdateTest(MainPresenterTest):
    def runTest(self):
        #Create new CCData object; pass to method; check mp values are now updated
        pass