'''
Created on Dec 9, 2014

@author: luchristopher
'''
from pandas.index import Timestamp
import pandas as pd

def cleanCollisionData(raw_data):
    '''
    do the following cleaning operations:
        1.create a column indicating the weekday info for each record
        2.reindex the data with Timestamp
    '''
    raw_data['DATETIME']=pd.to_datetime(raw_data['DATE'])
    raw_data.drop('DATE',1,inplace=True)
    raw_data.set_index('DATETIME',inplace=True)
    raw_data.sort(inplace = True)
    
        