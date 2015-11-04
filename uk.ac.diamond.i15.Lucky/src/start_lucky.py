'''
Created on 3 Nov 2015

@author: wnm24546
'''

import sys
from PyQt4 import QtGui

import Lucky.LuckyUIView
import Lucky.CalibrationConfigUI
import Lucky.MainUI

def main():
    app = QtGui.QApplication(sys.argv)
    lucky0 = Lucky.LuckyUIView.MainWindow()
    lucky = Lucky.MainUI.MainUI()
#    lucky0.show()
    lucky.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()