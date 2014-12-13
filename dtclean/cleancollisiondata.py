'''
Created on Dec 9, 2014

@author: luchristopher
'''
from pandas.index import Timestamp
import pandas as pd
import numpy as np

def cleanCollisionData(raw_data):
    '''
    do the following cleaning operations:
        1.create a column indicating the weekday info for each record
        2.reindex the data with Timestamp
    '''
    raw_data['DATETIME']=pd.to_datetime(raw_data['DATE'])
    raw_data.drop('DATE',1,inplace=True)
    raw_data.set_index('DATETIME',inplace=True)
    raw_data['TOTAL DEATHS'] = raw_data['NUMBER OF MOTORIST KILLED'] \
                             + raw_data['NUMBER OF CYCLIST KILLED'] \
                             + raw_data['NUMBER OF PEDESTRIANS KILLED'] \
                             + raw_data['NUMBER OF PERSONS KILLED']
    raw_data['TOTAL INJURIES'] = raw_data['NUMBER OF PERSONS INJURED'] \
                               + raw_data['NUMBER OF PEDESTRIANS INJURED'] \
                               + raw_data['NUMBER OF CYCLIST INJURED'] \
                               + raw_data['NUMBER OF MOTORIST INJURED'] # create a new column that combine all fatalities
    raw_data['TOTAL FATALITIES'] = raw_data['TOTAL DEATHS']+raw_data['TOTAL INJURIES']
    column_list = ['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']
    raw_data['VEHICLES INVOLVED'] = raw_data[column_list].notnull().sum(axis=1)
    raw_data.replace('Unspecified',np.nan,inplace=True)
    raw_data.sort(inplace = True)
    
        