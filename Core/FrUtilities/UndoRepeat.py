'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 23 May, 2017
# Last Modified Date       : 
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
import pymel.core as pm

def Undoable(function):
    '''
    from "Kriss Andrews" on http://blog.3dkris.com/
    A decorator that will make commands undoable in maya
    :param function:
    '''

    def decoratorCode(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        functionReturn = None
        try: 
            functionReturn = function(*args, **kwargs)

        finally:
            pm.undoInfo(closeChunk=True)
            return functionReturn
            
    return decoratorCode