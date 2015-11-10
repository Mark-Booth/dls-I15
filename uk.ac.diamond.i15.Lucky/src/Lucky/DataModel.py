'''
Created on 9 Nov 2015

@author: wnm24546
'''

class MainData(object):
    def __init__(self, mode=(0,1), calibType=(1,0,0), dataDir=None,
                 usdsPair=0, integStart=0, integEnd=0, integDelta=0):
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
        
        
        

class CalibrationConfigData(object):
    def __init__(self, calibDir=None, bulbTemp=0,
                 calibUS=None, calibDS=None, 
                 calibF1US=None, calibF1DS=None,
                 calibF2US=None, calibF2DS=None):
        self.calibDir = calibDir
        self.bulbTemp = bulbTemp
        self.calibFiles = [[calibUS, calibDS],
                           [calibF1US, calibF1DS],
                           [calibF2US, calibF2DS]]
        