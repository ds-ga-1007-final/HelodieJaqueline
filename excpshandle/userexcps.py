'''
Created on Nov 6, 2014

@author: luchristopher
'''
from exceptions import *

class InvalidInputError(Exception):
    pass

class FileExtensionError(Exception):
    pass

class FileNamingError(Exception):
    pass

class DateRangeError(Exception):
    pass

class DateValueError(Exception):
    pass