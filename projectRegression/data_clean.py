__author__ = 'leilu'

import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm

dataset = pd.read_csv("NYPD_Motor_Vehicle_Collisions.csv", header=0, sep=',')
df = pd.DataFrame(dataset)



def dataCleanForRegression(data):
    new_data = totalFatalities(data)
    update_data = numOfVehicles(new_data)
    clean_data = buildBoroDummies(update_data)
    col_to_keep = ['Number of total People injured and killed', 'num_vehicles_involved', 'BROOKLYN',  'QUEENS', 'MANHATTAN',
                   'BRONX', 'STATEN ISLAND']
    clean_data = clean_data[col_to_keep]
    return clean_data



def buildBoroDummies(data):
    dummies = pd.get_dummies(data['BOROUGH'])
    data = data.join(dummies)
    data = data.drop('BOROUGH', 1)
    return data

def totalFatalities(data):
    data['Number of total People injured and killed'] = \
    data['NUMBER OF PERSONS INJURED'] + df['NUMBER OF PERSONS KILLED']+\
    data['NUMBER OF PEDESTRIANS INJURED']+df['NUMBER OF PEDESTRIANS KILLED']+\
    data['NUMBER OF CYCLIST INJURED']+df['NUMBER OF CYCLIST KILLED']+\
    data['NUMBER OF MOTORIST INJURED']+df['NUMBER OF MOTORIST KILLED']  # create a new column that combine all fatalities
    return data

def numOfVehicles(data):
    col = ['VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'VEHICLE TYPE CODE 3', 'VEHICLE TYPE CODE 4', 'VEHICLE TYPE CODE 5']
    data['num_vehicles_involved'] = data[col].notnull().sum(axis=1)
    return data

