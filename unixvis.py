'''
Created on Dec 13, 2014

@author: luchristopher
'''
from collisionvis import CollisionVisualizer
import matplotlib.pyplot as plt
import matplotlib.animation as mam
import pandas as pd
import numpy as np
from userinterface import *
from ioprocess import *
from excpshandle import *

class UnixVisualizer(CollisionVisualizer,UnixInterface):
    '''
    Class definition for plotting data with matplotlib and listing dataframes on the screen
    '''


    def __init__(self,init_dataframe):
        '''
        Constructor
        '''
        CollisionVisualizer.__init__(self, init_dataframe)  #initializing base class
        
    def _isStyleAvailable(self,style):
        '''
        check if plot style is available in current matplotlib version
        '''
        if style in plt.style.available:
            return True
        else:
            return False
        
    def unixvis_top5Factors(self):
        '''
        provide solutions for visualizing top5Factor() data, includes displaying text in terminal and plotting with matplotlib
        '''
        self.loading()
        print 'The Top 5 Contributers to The Collisions:\n'
        
    def unixvis_vehicleTypes(self,plot_style):
        '''
        provide solutions for visualizing top5Factor() data, lists all recorded vehicle types and their counts, plot the top 5
        '''
        start_date, end_date = self.receiveDateRange()
        self.loading()
        received = self.VehicleTypes(start_date, end_date)
        self.done()
        #displaying dataframe
        print 'The Recorded Vehicle Types and Their Stats Are Shown Below:\n'
        print received
        #plotting and saving
        if self._isStyleAvailable(plot_style):
            plt.style.use(plot_style)
        plt.title('Collisions By Vehicle Types, From {} to {}'.format(start_date,end_date),fontsize=12,color='k')
        received['COUNTS'].plot(kind='pie',legend=False,autopct='%1.1f%%')
        plt.ylabel('')
        plt.tight_layout()
        fig = plt.gcf()
        plt.show()          
        #saving figures
        ifSaveFigure(fig, 'piechart_vehicletypes_{}-{}'.format(start_date,end_date), 'png')
        
        
        
        