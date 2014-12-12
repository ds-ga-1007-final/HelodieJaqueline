'''
Created on Dec 2, 2014

@author: luchristopher
'''
from ioprocess import *
from dtclean import *
from collisionvis import *
from dtclean.donothing import donothingClean
from dtclean.cleanreg import dataCleanForRegression
from userinterface.ui_unix import UnixInterface
from dtclean.cleancollisiondata import cleanCollisionData
from utilities import *


def main():
    
    #unix command line 
    terminal_ui = UnixInterface()
    terminal_ui.loading()
    #read and clean data
    dataframe_reader = DataReader()
    raw_data=dataframe_reader.safeReadCsvLocal('./data/NYPD_Motor_Vehicle_Collisions.csv')
    cleaner = DataCleaner(cleanCollisionData)
    cleaner.clean(raw_data)
    collision_vis_demo = CollisionVisualizer(raw_data)
    terminal_ui.welcome()
    executeAnalysis(collision_vis_demo,terminal_ui,terminal_ui.options())

if __name__ == '__main__':
    main()