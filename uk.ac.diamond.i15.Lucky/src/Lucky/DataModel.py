'''
Created on 9 Nov 2015

@author: wnm24546
'''

import os
from collections import OrderedDict

class MainData(object):
    def __init__(self, mode=(0,1), calibType=(1,0,0), dataDir=os.path.expanduser("~"),
                 usdsPair=['',''], integStart=500, integEnd=900, integDelta=200):
        #These relate to the calculations
        self.mode = mode
        self.calibType = calibType
        self.dataDir = dataDir
        self.usdsPair = usdsPair
        self.integrationConf = [integStart, integEnd, integDelta]
        self.calibConfigData = CalibrationConfigData()
        
        #These are specific UI variables
        self.runEnabled = False
        self.stopEnabled = False
        self.allDataPresent = False
        self.usdsControlsEnabled = True
        self.allUIControlsEnabled = True
        
        self.dataValid = {'mode':True,
                          'calibType':True,
                          'dataDir':False,
                          'usFile':False,
                          'dsFile':False,
                          'integrationConf':True,
                          'calibConfig':False}
        self.usdsPairGTE = False
        

class CalibrationConfigData(object):
    def __init__(self, calibDir=os.path.expanduser("~"), bulbTemp=0,
                 calibUS='', calibDS='', 
                 calibF1US='', calibF1DS='',
                 calibF2US='', calibF2DS=''):
        self.calibDir = calibDir
        self.bulbTemp = bulbTemp
        self.calibFiles = OrderedDict([('(DS)',calibDS),
                                       ('(US)',calibUS),
                                       ('F1 (DS)',calibF1DS),
                                       ('F1 (US)',calibF1US),
                                       ('F2 (DS)',calibF2DS),
                                       ('F2 (US)',calibF2US)])
        self.calibValid = {'bulbTemp':False,
                           '(DS)':False,
                           '(US)':False,
                           'F1 (DS)':False,
                           'F1 (US)':False,
                           'F2 (DS)':False,
                           'F2 (US)':False}
