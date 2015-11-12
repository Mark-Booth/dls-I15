'''
Created on 10 Nov 2015

@author: wnm24546
'''

class BadModelStateException(Exception):
    def __init__(self, message):
        super(BadModelStateException, self).__init__(message)

class InvalidPathException(Exception):
    def __init__(self, message):
        super(InvalidPathException, self).__init__(message)