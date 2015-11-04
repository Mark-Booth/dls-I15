'''
Created on 3 Nov 2015

@author: wnm24546
'''

class MainWindowModel():

    def __init__(self):
        self.runEnabled = True
        self.stopEnabled = False
        self.isLive = True
    
    def runLuckyCalcs(self):
        self.runEnabled = False
        self.stopEnabled = True
    
    def stopLuckyCalcs(self):
        self.runEnabled = True
        self.stopEnabled = False
