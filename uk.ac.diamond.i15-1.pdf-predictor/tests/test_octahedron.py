'''
Created on 4 Nov 2016

@author: wnm24546
'''

#Test tools
from nose.tools import assert_equals

#What we're testing
from pdfpredictor.polyhedra import Octahedron

class TestOctahedron(object):
    
    def setUp(self):
        pass
    
    def test_number_points(self):
        test_octa = Octahedron()
        assert_equals(test_octa.n_vertices(), 6, "Octahedron should have 6 vertices")
    
    def test_vertex_positions(self):
        test_octa = Octahedron()
        
        #Points is an array of positions described in x,y,z)
        vertices = test_octa.vertices
        
        for vertex in vertices:
            assert_equals()
        