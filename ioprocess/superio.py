'''
Created on Nov 7, 2014

@author: luchristopher
'''
import sys
from excpshandle import *
from matplotlib.pyplot import *
import re
import os.path


def safeInput(prompt,termination_command,str_parser):
    '''
        Provide general input string checking and additional validations with user defined functions,
        if illegal input string is received, it will flush the input and request a new valid input
    '''
    while True:
        try:
            input_string = raw_input(prompt)
        except (KeyboardInterrupt, EOFError):
            print >> sys.stderr, 'Program terminated by unexpected operations\n'
            sys.exit()
        
        if input_string in termination_command:
            print 'Program terminated by user\n'
            sys.exit()
            
        try:
            secured_input = str_parser(input_string)
            break
        except (InvalidInputError,DateValueError):
            continue
    return secured_input


def ifSaveFigure(fig,filename,format,os_filename_validator=None):
    '''
        Create a prompt to ask the user if a figure needs to be exported to an external file, create
        'filename.format' in 'Figures' when receive 'yes' or 'y', inputs are not case Sensitive, the
        function also provides format checking to ensure the filename is legal within unix based file 
        system naming rules
    '''
    figure_pointer = fig
    savefig_prompt = raw_input('Do you want to save the picture to an external file?\nEnter \'yes\' to export:')
    if savefig_prompt.upper() == 'YES' or 'Y':
        if re.match(re.compile(r"^[^\.\+\?\*\$]+$"),filename) and len(filename) < 255:
            if re.match(re.compile(r'^png$|^bmp$|^pdf$|^jpeg$|^jpg$|^tif$'),format):
                try:
                    figure_pointer.savefig('{}.{}'.format(filename,format))
                except:
                    print >> sys.stderr, 'Cannot create file {}.{}\n'.format(filename,format)
            else:
                raise FileExtensionError()
        else:
            raise FileNamingError()
        
