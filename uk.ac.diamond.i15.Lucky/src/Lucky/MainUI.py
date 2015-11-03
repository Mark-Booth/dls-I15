'''
Created on 3 Nov 2015

@author: wnm24546
'''

from PyQt4 import QtGui

class LuckyMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(LuckyMainWindow, self).__init__()
        
        self.setWindowTitle('Lucky')
        #self.SetWindowIcon(QtGui.QIcon('SomeLocalIcon.png'))