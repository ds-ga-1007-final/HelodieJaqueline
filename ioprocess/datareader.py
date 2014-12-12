'''
Created on Dec 2, 2014

@author: luchristopher
'''
import pandas as pd
import os
import sys

class DataReader():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def safeReadCsvLocal(self,source_file):
        '''
        returns a secured dataframe from a given csv file
        '''
        #validate the filename
        try:
            secured_dataframe = pd.read_csv(source_file,low_memory=False)
        except:
            print >> sys.stderr, 'FAILURE: Data cannot be retrieved at this moment!\n'
            sys.exit()
        return secured_dataframe
        
    def safeReadJson(self,source_file):
        pass