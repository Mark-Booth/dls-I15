'''
Created on 9 Nov 2015

@author: wnm24546
'''

import os

class MainData(object):
    def __init__(self, mode=(0,1), calibType=(1,0,0), dataDir=os.path.expanduser("~"),
                 usdsPair=0, integStart=500, integEnd=900, integDelta=200):
        #These relate to the calculations
        self.mode = mode
        self.calibType = calibType
        self.dataDir = dataDir
        self.usdsPair = usdsPair
        self.integrationConf = [integStart, integEnd, integDelta]
        self.calibConfigData = CalibrationConfigData()
        self.usdsPairTable = []
        
        #These are specific UI variables
        self.runEnabled = False
        self.stopEnabled = False
        self.allDataPresent = False
        self.usdsControlsEnabled = True
        self.allUIControlsEnabled = True
        
        self.dataValid = {'mode':True,
                          'calibType':True,
                          'dataDir':False,
                          'usdsPair':False,
                          'integrationConf':True,
                          'calibConfig':False}
        

class CalibrationConfigData(object):
    def __init__(self, calibDir=os.path.expanduser("~"), bulbTemp=0,
                 calibUS=None, calibDS=None, 
                 calibF1US=None, calibF1DS=None,
                 calibF2US=None, calibF2DS=None):
        self.calibDir = calibDir
        self.bulbTemp = bulbTemp
        self.calibFiles = [[calibUS, calibDS],
                           [calibF1US, calibF1DS],
                           [calibF2US, calibF2DS]]
        
        self.calibFileLabels = {[0,0]:'calibUS',
                                [0,1]:'calibDS',
                                [1,0]:'calibF1US',
                                [1,1]:'calibF1DS',
                                [2,0]:'calibF2US',
                                [2,1]:'calibF2DS',
                                }
        self.calibValid = {'bulbTemp':False,
                           'calibDir':True,
                           'calibUS':False,
                           'calibDS':False,
                           'calibF1US':False,
                           'calibF1DS':False,
                           'calibF2US':False,
                           'calibF2DS':False}
        