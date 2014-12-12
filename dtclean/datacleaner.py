'''
Created on Nov 23, 2014

@author: luchristopher
'''

class DataCleaner():
    '''
    This is the class definition of a general purpose data cleaner, which cleans a pandas data frame according with specified methods defined by users
    '''


    def __init__(self, clean_func):
        '''
        Constructor
        '''
        self.__F = clean_func
    
    def clean(self,input_dataframe):
        '''
        Cleans the input dataframe with self.__F
        '''
        return self.__F(input_dataframe)
        
    
    
    