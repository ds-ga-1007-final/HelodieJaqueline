'''
Created on Dec 11, 2014

@author: luchristopher
'''
import pandas as pd
import numpy as np
import sys
import os
from ioprocess import *
from ioprocess.parsers import parseOptions, parseDates
import time

class UnixInterface():
    '''
    class definition of unix command line based UI
    '''
    def __init__(self):
        pass
    
    def loading(self):
        '''
        print a progress bar when operating on data
        '''
        os.system('clear')
        print 'Loading...'
            
    def welcome(self):
        '''
        print welcome message
        '''
        os.system('clear')
        try:
            f = open('./dat/welcome_unix_text.txt','r')
        except:
            print >> sys.stderr, 'Internal File Missing, Program Terminated!\n'
        try:
            welcome_page = f.readlines()
        except (EOFError,KeyboardInterrupt):
            print >> sys.stderr, 'File Reading Error\n'
        for line in welcome_page:
            print line
        
    def options(self):
        '''
        receive an integer as the option input
        '''
        option = safeInput('Your Input (Type exit or quit to terminate the program): ', ['exit','quit'],parseOptions)
        return option
    
    def receiveDateRange(self):
        '''
        receives input for a date range
        '''
        start_date = safeInput('Please Input The Start Date (MM-DD-YYYY): ', ['exit','quit'], parseDates)
        end_date = safeInput('Please Input The End Date (MM-DD-YYYY): ', ['exit','quit'], parseDates)
        return start_date, end_date