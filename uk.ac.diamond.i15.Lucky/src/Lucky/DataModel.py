'''
Created on 9 Nov 2015

@author: wnm24546
'''

class MainViewData(object):
    def __init__(self, mode=(1,0), calibType=(1,0,0), dataDir=None,
                 usdsPair=0, integStart=0, integEnd=0, integDelta=0):
        self.mode = mode
        self.calibType = calibType
        self.dataDir = dataDir
        self.usdsPair = usdsPair
        self.integrationConf = [integStart, integEnd, integDelta]

class CalibrationConfigViewData(object):
    def __init__(self, calibDir=None, bulbTemp=0,
                 calibUS=None, calibDS=None, 
                 calibF1US=None, calibF1DS=None,
                 calibF2US=None, calibF2DS=None):
        self.calibDir = calibDir
        self.bulbTemp = bulbTemp
        self.calibUS = calibUS
        self.calibDS = calibDS
        self.calibF1US = calibF1US
        self.calibF1DS = calibF1DS
        self.calibF2US = calibF2US
        self.calibF2DS = calibF2DS
        