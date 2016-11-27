'''
Created on 4 Nov 2016

@author: wnm24546
'''

from collections import namedtuple

class Polyhedron(object):
    
    def __init__(self):
        Vertex = namedtuple("Vertex", ["x","y","z"])