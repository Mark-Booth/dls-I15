'''
Created on 3 Nov 2015

@author: wnm24546
'''

import sys
from PyQt4 import QtGui

import Lucky.MainUI

def main():
    app = QtGui.QApplication(sys.argv)
    lucky = Lucky.MainUI.LuckyMainWindow()
    lucky.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()