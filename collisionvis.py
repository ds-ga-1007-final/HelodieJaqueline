'''
Created on Dec 2, 2014

@author: luchristopher
'''
from dtclean import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from excpshandle import *
from dtclean.dropmissinglocations import dropMissingLocations
import sys
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
from datacleanregression import *



class CollisionVisualizer():
    '''
    classdocs
    '''


    def __init__(self, init_dataframe):
        '''
        Constructor
        '''
        self._data = init_dataframe
        
    def __getData(self):
        '''
        returns self._data, for test purposes only!
        '''
        return self._data
    
    def _isValidDateRange(self,start_date,end_date):
        '''check if the date range is valid, that is
            2012-07-01 < start_date < end_date < 2014-11-29
        '''
        start_date_timestamp = pd.to_datetime(start_date)
        end_date_timestamp = pd.to_datetime(end_date)
        return (start_date_timestamp >= self._data.index[0]) & (end_date_timestamp <= self._data.index[-1]) & (start_date_timestamp < end_date_timestamp)
        
    
    def _getVehicleTypes(self):
        '''
        returns the list for all vehicle type names that has been recorded in case needed, might be deleted in the next version
        ''' 
        columns_list = ['VEHICLE TYPE CODE {}'.format(x) for x in range(1,6)]
        vehicle_type_set = set()
        for type_code in columns_list:
            vehicle_type_set.update(list(self._data[type_code].dropna().unique()))
        return list(vehicle_type_set)
    
    def _selectByDateRange(self,start_date=None,end_date=None):
        '''
        returns a dataframe containing entries from start_date to end_date
        '''
        if self._isValidDateRange(start_date,end_date):
            return self._data[start_date:end_date]
        else:
            raise DateRangeError()
    
    def barGraphVehicleTypes(self,start_date=None,end_date=None):
        '''
        generate a pie chart visualizing the ratio of different types of vehicles involved in collisions within date range (start,end)
        '''
        try:
            date_ranged_data = self._selectByDateRange(start_date, end_date)
        except (DateRangeError):
            print >> sys.stderr, 'Invalid Date Range!\n'
            return None
            #additional exception handles shall be added here
            
        record_vehicle_types = pd.Series(date_ranged_data[['VEHICLE TYPE CODE {}'.format(x) for x in range(1,6)]].values.ravel()).dropna()
        collisions_count_by_type = record_vehicle_types.value_counts()
        print collisions_count_by_type
        #plotting
        plt.style.use('ggplot')
        plt.title('Collisions By Vehicle Types, From {} to {}'.format(start_date,end_date),fontsize=12,color='k')
        plt.ylabel('Vehicle Types')
        plt.xlabel('Number of Collisions')
        collisions_count_by_type.plot(kind='barh')
        plt.tight_layout()
        plt.show()
        return collisions_count_by_type
    
    def listNearbyCollisions(self,start_date=None, end_date=None, longitude = None, latitude = None, proximity_range = None):
        '''
        returns a table listing all the collisions in the nearby area of (longitude, latitude) from start_date to end_date, the table has
        columns [DATE, TIME, DISTANCE FROM, NUMBER OF INJURIES AND DEATHS]
        '''
        #delete all entries without geographical information
        geographical_cleaner = DataCleaner(dropMissingLocations)
        data_with_location = geographical_cleaner.clean(self._selectByDateRange(start_date, end_date))
        data_with_location.apply()


    def regressionPlot(self):
        '''
        generates a scatter plot of normalized raw data with a fitted regression line
        '''
        df = self._data
        Y = df['Total Fatalities']  # response
        X = df['Vehicles Involved']  # predictor
        X = sm.add_constant(X)  # Adds a constant term to the predictor
        est = sm.OLS(Y, X)
        est = est.fit()

        X_prime = np.linspace(X['Vehicles Involved'].min(), X['Vehicles Involved'].max(), 5)[:, np.newaxis]
        X_prime = sm.add_constant(X_prime)  # add constant as we did before
        
        plt.ylim([0, 35])
        y_hat = est.predict(X_prime)
        plt.scatter(X['Vehicles Involved'], Y, alpha=0.3)  # Plot the raw data
        plt.xlabel("Number of Vehicles Invovled")
        plt.ylabel("Total Fatalities")
        plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #plot regession line
        plt.savefig('regression_line')
        
    
    def regression(self):
        '''
        generate a summary table about the parameters from the regression analysis
        '''
        df = self._data
        msk = np.random.rand(len(df)) < 0.75
        train = df[msk]
        test = df[~msk]

        ols = sm.OLS(train['Number of total People injured and killed'], train.drop('Number of total People injured and killed', 1))
        result = ols.fit()

        print result.summary()
            
    def SummaryStats(self, start_date, end_date):
        ''' 
        generate a data frame that reports the maximum number of fatalities during a time frame given as parameters
        '''
        df = _selectByDateRange(start_date, end_date)
        maximum_fatalities = df['Total Fatalities'].max()
        d = {'start_time': start_date, 'end_time': end_date,'Total Fatalities':maximum_fatalities}
        summary = pd.DataFrame(data=d, index=index)
        return summary
