'''
Created on Dec 11, 2014

@author: luchristopher
'''
def dropMissingLocations(input_dataframe):
    '''
    returns a new dataframe with all entries without location info dropped
    '''
    return input_dataframe[(input_dataframe['LATITUDE'].notnull() & input_dataframe['LONGITUDE'].notnull())]