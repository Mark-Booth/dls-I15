'''
Created on 6 Nov 2015

@author: wnm24546
'''
import sys
from PyQt4.QtGui import (QHBoxLayout, QWidget, QPushButton, QApplication, QDialog)

class Node(object):
    pass


class Foo(QWidget, Node):

    def __init__(self):
        super(Foo, self).__init__(parent=None)
        Node.__init__(self, 'Node name is Disp')
        
        btn = QPushButton("Push")
        btn.clicked.connect(self.btnClick)
        layout = QHBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)
        
    def btnClick(self):
        self.bar = Bar(self)
        self.bar.exec_()


class Bar(QDialog):

    def __init__(self, parent_widget):
        super(Bar, self).__init__(parent=parent_widget)
        btn = QPushButton("Push")
        btn.clicked.connect(self.btnClick)
        layout = QHBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)
    
    def btnClick(self):
        print "Yay!"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Foo()
    w.show()
    sys.exit(app.exec_())
