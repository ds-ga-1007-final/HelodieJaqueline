'''
Created on Dec 3, 2014

@author: luchristopher
'''
import unittest
from collisionvis import *
from ioprocess import *
import time
from dtclean import *


class TestCollisionVisualizer(unittest.TestCase):


    def setUp(self):
        self.test_data_reader = DataReader()
        self.test_cleaner = DataCleaner(cleanCollisionData)
        test_raw_data = self.test_data_reader.safeReadCsvLocal('../data/NYPD_Motor_Vehicle_Collisions.csv')
        self.test_cleaner.clean(test_raw_data)
        self.test_object = CollisionVisualizer(test_raw_data)

    def tearDown(self):
        pass


#    def test_getVehicleTypes(self):
#         print self.test_object._getVehicleTypes()
        
#    def test_barGraphVehicleTypes(self):
#        print self.test_object._data
        self.test_object.barGraphVehicleTypes('8/10/2013', '2/8/2014')

    def test_regressionPlot(self):
        self.test_object.bregressionPlot()


        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
