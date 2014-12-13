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
import statsmodels.api as sm

class CollisionVisualizer():
    '''
    classdocs
    '''

    '''
    Internal Methods
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
        
    def _safeSelectByDateRange(self,start_date=None,end_date=None):
        '''
        try select date by range, includes exception handling
        '''
        try:
            date_ranged_data = self._selectByDateRange(start_date, end_date)
            return date_ranged_data
        except (DateRangeError):
            print >> sys.stderr, 'Invalid Date Range!\n'
            return None
    
    '''
    Public Methods
    '''
    def VehicleTypes(self,start_date=None,end_date=None):
        '''
        returns a dataframe for all recorded vehicle types, counts and percentages within date range (start,end)
        '''
        date_ranged_data = self._safeSelectByDateRange(start_date,end_date)
        record_vehicle_types = pd.Series(date_ranged_data[['VEHICLE TYPE CODE {}'.format(x) for x in range(1,6)]].values.ravel()).dropna()
        collisions_count_by_type = record_vehicle_types.value_counts()
        others_count = collisions_count_by_type.sum()-collisions_count_by_type.head().sum()
        collisions_count_by_type = collisions_count_by_type.head(5)
        collisions_count_by_type['OTHERS'] = others_count 
        print collisions_count_by_type
        collisions_count_by_type = pd.DataFrame(collisions_count_by_type,columns=['COUNTS'])
        collisions_count_by_type['%'] = collisions_count_by_type['COUNTS']/collisions_count_by_type['COUNTS'].sum() #calculate percentage
        return collisions_count_by_type
    
    def listNearbyCollisions(self,start_date=None, end_date=None, longitude = None, latitude = None, proximity_range = None):
        '''
        returns a table listing all the collisions in the nearby area of (longitude, latitude) from start_date to end_date, the table has
        columns [DATE, TIME, DISTANCE FROM, NUMBER OF INJURIES AND DEATHS]
        '''
        #delete all entries without geographical information
        geographical_cleaner = DataCleaner(dropMissingLocations)
        data_with_location = geographical_cleaner.clean(self._safeSelectByDateRange(start_date, end_date))
        data_with_location.apply()


    def regressionPlot(self):
        '''
        generates a scatter plot of normalized raw data with a fitted regression line
        '''
        df = self._data
        Y = self._data['TOTAL FATALITIES']  # response
        X = self._data['VEHICLES INVOLVED']  # predictor
        X = sm.add_constant(X)  # Adds a constant term to the predictor
        est = sm.OLS(Y, X)
        est = est.fit()
 
        X_prime = np.linspace(X['VEHICLES INVOLVED'].min(), X['VEHICLES INVOLVED'].max(), 5)[:, np.newaxis]
        X_prime = sm.add_constant(X_prime)  # add constant as we did before
        
        plt.style.use('ggplot')
        plt.ylim([0,35])
        y_hat = est.predict(X_prime)
        plt.scatter(X['VEHICLES INVOLVED'],Y,alpha = 0.3)
        plt.xlabel('Number of Vehicles Involved')
        plt.ylabel('Total Fatalities')
        plt.title('Linear Regression Model of Fatilities vs. Vehicles Involved',fontsize=12,color='k')
        plt.plot(X_prime[:,1],y_hat,'r',alpha=0.9)
        plt.show()
    
    def howManyPerday(self,start_date=True,end_date=True):
        '''
        return a Dataframe with the Date and how many collosions happend that day
        columns [DATE, HAS collisions happen]
        then use numpy np.mean to find the mean value of has collisions happen
        '''
        
        new_df=self._data[start_date:end_date]
        date_happen=new_df.groupby()
        date_happened={'date':[],'happen':[],'killed':[],'injured':[],'kill and injured':[]}
        for date, group in date_happen:
            happen=len(group)
            inAndKill=group['TOTAL INJURIES OR KILLED'].sum()
            kill=group['TOTAL DEATHS'].sum()
            injured=group['TOTAL INJURIES'].sum()
            date_happened['date'].append(date)
            date_happened['happen'].append(happen)
            date_happened['killed'].append(kill)
            date_happened['injured'].append(injured)
            date_happened['kill and injured'].append(inAndKill)

        df_happen=pd.DataFrame.from_dict(date_happened['happen'])#, orient='columns', dtype=None)
        df_date=pd.DataFrame.from_dict(date_happened['date'])
        df_in=pd.DataFrame.from_dict(date_happened['injured'])
        df_kill=pd.DataFrame.from_dict(date_happened['killed'])
        df_in_kill=pd.DataFrame.from_dict(date_happened['kill and injured'])
        df_date.columns=['date']
        df_happen.columns=['Has collisions happen']
        
        #print df_date
        #print df_kill_d
        df_date_happen=df_date.join(df_happen)
        df_data_happen=df_date_happen.join(df_in)
        df_data_happen= df_data_happen.join(df_kill)
        df_data_happen= df_data_happen.join(df_in_kill)
        df_data_happen.columns=[['date','Has collisions happen','injured','killed','kill and injured']]
        #df_date_kill.columns=['Date','TOTAL INJURIES OR KILLED']
        df_date_happen=df_date_happen.set_index('date')
        mean_collision=np.mean(df_date_happen['Has collisions happen'])    
        mean_inj=np.mean(df_date_happen['injured']) 
        mean_kill=np.mean(df_date_happen['killed'])
        mean_kill_in=np.mean(df_date_happen['kill and injured'])
        return df_date_happen,mean_collision,mean_inj,mean_kill,mean_kill_in
    
    def boro_kill(self,start_date=True,end_date=True):
        '''
        return a table with borough and number of kill and injured
        columns=['BOROUGH','TOTAL DEATHS','TOTAL INJURIES'] 
        '''
        data=self._data[start_date:end_date]
        boro=data.groupby('BOROUGH')
    
        injured_killed={'borough':[],'injured_killed':[]}
        for borough,group in boro:
            group=group[['Date','TOTAL DEATHS','TOTAL INJURIES']]
            b_group=group.set_index('Date')
            x_sum=b_group.sum(axis=0)
            #print borough
            #print x_sum
            injured_killed['borough'].append(borough)
            injured_killed['injured_killed'].append(x_sum)
     

        df_boro=pd.DataFrame.from_dict(injured_killed['borough'])#, orient='columns', dtype=None)
        df_kill=pd.DataFrame.from_dict(injured_killed['injured_killed'])
        df_boro_kill=df_boro.join(df_kill)
        df_boro_kill.columns=['BOROUGH','TOTAL DEATHS','TOTAL INJURIES']
        df_boro_kill=df_boro_kill.set_index('BOROUGH')
        plt.style.use('ggplot')
        df_boro_kill.plot(kind='bar', stacked=True)
        #x.savefig('lol.png')
        plt.show()
        return df_boro_kill
    
    
    def time_kill(self,start_date=True,end_date=True):
        data=self._data[start_date:end_date]
        dd=data.sort('TIME',ascending=1)
        time_group=dd.groupby('TIME')
        time_injured_killed={'TIME':[],'injured_killed':[]}
        for time,t_group in time_group:
            t_group=t_group[['time','TOTAL INJURIES OR KILLED']]
            time_sum=t_group['TOTAL INJURIES OR KILLED'].sum(axis=0)
            time_injured_killed['TIME'].append(time)
            time_injured_killed['TIME'].append(time_sum)
        df_time=pd.DataFrame.from_dict(time_injured_killed['time'])#, orient='columns', dtype=None)
        df_kill_t=pd.DataFrame.from_dict(time_injured_killed['injured_killed'])
        df_time.columns=['time']
        df_kill_t.columns=['TOTAL INJURIES OR KILLED']
        #print df_date
        #print df_kill_d
        df_time_kill=df_time.join(df_kill_t)
        #df_date_kill.columns=['Date','TOTAL INJURIES OR KILLED']
        df_time_kill=df_time_kill.set_index('time')
        plt.style.use('ggplot')
        df_time_kill.plot()
        plt.title('number of injured and killed by time')
        # plt.savefig('number of injured and killed by time.png')
        # plt.show()
        return df_time_kill

#     def date_kill(self,start_date=True,end_date=True):
#         data=self._data[start_date:end_date]
#         date_g=data.groupby(data.index)
#         date_injured_killed={'Date':[],'injured_killed':[]}
#         for date,group in date_g:
#             group=group[['Date','TOTAL INJURIES OR KILLED']]
#             #date_group=group.set_index('Date')
#             date_sum=group['TOTAL INJURIES OR KILLED'].sum(axis=0)
#             date_injured_killed['Date'].append(date)
#             date_injured_killed['injured_killed'].append(date_sum)
#             #print date_injured_killed 
# 
#         df_date=pd.DataFrame.from_dict(date_injured_killed['Date'])#, orient='columns', dtype=None)
#         df_kill_d=pd.DataFrame.from_dict(date_injured_killed['injured_killed'])
#         df_date.columns=['Date']
#         df_kill_d.columns=['TOTAL INJURIES OR KILLED']
#         #print df_date
#         #print df_kill_d
#         df_date_kill=df_date.join(df_kill_d)
#         #df_date_kill.columns=['Date','TOTAL INJURIES OR KILLED']
#         df_date_kill=df_date_kill.set_index('Date')
#         plt.style.use('ggplot')
#         df_date_kill.plot()
#         plt.title('number of injured and killed by Date')
#         plt.savefig('number of injured and killed by Date.png')
#         plt.show()
#         return df_date_kill
#         #df_date_kill=date_kill(data)
# 
#         
#         plt.ylim([0, 35])
#         y_hat = est.predict(X_prime)
#         plt.scatter(X['Vehicles Involved'], Y, alpha=0.3)  # Plot the raw data
#         plt.xlabel("Number of Vehicles Invovled")
#         plt.ylabel("Total Fatalities")
#         plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #plot regession line
#         plt.savefig('regression_line')
#         
    
    def _regression(self):
        '''
        generate a summary table about the parameters from the regression analysis
        '''
        mask = np.random.rand(len(self._data)) < 0.75
        train = self._data[mask]
        test = self._data[~mask]
        ols = sm.OLS(train['TOTAL FATALITIES'], train.drop('TOTAL FATALITIES', 1))
        result = ols.fit()
        return result.summary()
            
    def getMaxFatalities(self, start_date, end_date):
        ''' 
        generate a data frame that reports the maximum number of fatalities during a time frame given as parameters
        '''
        date_ranged_data = self._safeSelectByDateRange(start_date,end_date)
        max_fatality_point = date_ranged_data[date_ranged_data['TOTAL FATALITIES']==date_ranged_data['TOTAL FATALITIES'].max()]
        max_fatality_point = max_fatality_point[['TIME','TOTAL FATALITIES','BOROUGH','ZIP CODE','LATITUDE','LONGITUDE']]
        return max_fatality_point

    def top5Factors(self,start_date,end_date):
        '''
        returns the top 5 contributing factor for accidents in the given date range and plot a pie Chart
        '''
        date_ranged_data = self._safeSelectByDateRange(start_date, end_date)
        factors_list = pd.Series(date_ranged_data[['CONTRIBUTING FACTOR VEHICLE {}'.format(x) for x in range(1,6)]].values.ravel()).dropna()
        top5_factors = factors_list.value_counts().head()   #keep only the top 5
        return top5_factors
    
        