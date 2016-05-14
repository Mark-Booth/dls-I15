'''
Created on 11 Mar 2016

@author: wnm24546
'''
import unittest
import os

class Test(unittest.TestCase):


    def setUp(self):
        self.mainData = MainData()


    def tearDown(self):
        pass


    def testDefaults(self):
        self.assertEqual(os.path.expanduser("~"), self.mainData.dataDir, "Expected dataDir not found")
        
    def testGetSetUSDSByNumbers(self): 
        self.assertEqual([1, 2], self.mainData.getUSDSNumbers(), "Returned USDS numbers differ from expected.")
        
        self.mainData.setUSDSNumbers([35,36])
        self.assertEqual([35, 36], self.mainData.getUSDSNumbers(), "Returned USDS numbers differ from expected.")
        usdsFilePaths = [os.path.join(self.mainData.dataDir,"T_35.txt"), os.path.join(self.mainData.dataDir,"T_35.txt")]
        self.assertEqual(usdsFilePaths, self.mainData.usdsFiles, "Expected USDS filepath after setting filenumbers are wrong")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()