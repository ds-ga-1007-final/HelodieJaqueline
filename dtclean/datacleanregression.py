__author__ = 'leilu'

import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm



def dataCleanForRegression(self):
    data = self._data
    clean_data = buildBoroDummies(data)
    col_to_keep = ['Number of total People injured and killed', 'num_vehicles_involved', 'BROOKLYN',  'QUEENS', 'MANHATTAN',
                   'BRONX', 'STATEN ISLAND']
    clean_data = clean_data[col_to_keep]
    return clean_data


def buildBoroDummies(self):
    data = self._data
    dummies = pd.get_dummies(data['BOROUGH'])
    data = data.join(dummies)
    data = data.drop('BOROUGH', 1)
    return data

def normalizeData(self):
    df = self._data
    df_norm = (df - df.mean()) / (df.max() - df.min())
    return df_norm
