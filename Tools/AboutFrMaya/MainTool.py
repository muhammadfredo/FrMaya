'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 Sep, 2017
# Last Modified Date       : 
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''

import os

from FrMaya.Core.FrFile import BaseFile
from FrMaya.Core.FrInterface import BaseInterface
reload(BaseInterface)
class MainGUI( BaseInterface.BasePsWindow ):
    '''
    Main GUI for FrMaya About
    '''
    
    def __init__(self, *args):
        '''
        Constructor of main GUI for FR_RiggingTool
        '''
        
        # Convert ui path file as FrFile Object
        UIfile = BaseFile.BasePath( os.path.join( os.path.dirname( __file__ ), 'AboutFrMaya.ui' ) )
        super( MainGUI, self ).__init__( UIfile, Title = 'About FrMaya', *args )
        
#         self.Connect_EventHandlers()