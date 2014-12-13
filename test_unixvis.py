'''
Created on Dec 13, 2014

@author: luchristopher
'''
import unittest
from unixvis import *
from dtclean import *



class Test_UnixVisualizer(unittest.TestCase):


    def setUp(self):
        begin = time.time()
        self.test_data_reader = DataReader()
        self.test_cleaner = DataCleaner(cleanCollisionData)
        test_raw_data = self.test_data_reader.safeReadCsvLocal('data/NYPD_Motor_Vehicle_Collisions.csv')
        self.test_cleaner.clean(test_raw_data)
        self.test_object = UnixVisualizer(test_raw_data)
        end = time.time()
        print end-begin


    def tearDown(self):
        self.test_data_reader = None
        self.test_object = None
        self.test_cleaner = None


    def test_unixvis_vehicleTypes(self):
        self.test_object.unixvis_vehicleTypes('ggplot')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()