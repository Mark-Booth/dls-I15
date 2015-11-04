'''
Created on 3 Nov 2015

@author: wnm24546
'''

#from PyQt4 import QtCore

class MainWindowModel():
    runEnabled = True
    stopEnabled = False
	
	
    def __init__(self):
    	pass
	#Do nothing
    
    def runLuckyCalcs(self):
    	runEnabled = False
    	stopEnabled = True
    
    def stopLuckyCalcs(self):
    	runEnabled = True
    	stopEnabled = False
    

    