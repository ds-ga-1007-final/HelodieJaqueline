'''
Created on Dec 11, 2014

@author: luchristopher
'''
def executeAnalysis(visualizer_instance, ui, parameter):
    '''
    execute exploratory Analysis
    '''
    if parameter == 1:
        pass
    elif parameter == 2:
        start_date, end_date = ui.receiveDateRange()
        visualizer_instance.barGraphVehicleTypes(start_date,end_date)
