'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 23 Feb, 2016
# Last Modified Date       : 18 May, 2017
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
# import maya.cmds as mc
# import FRtools.rigging.general as riggen
# import FRtools.rigging.modules.general as rigmod
# import FRtools.ui.FR_BaseQWidget as frui
from FrMaya.Core.FrInterface import BaseInterface
from FrMaya.Core.FrFile import BaseFile
import os, glob

# from functools import partial
# from FRlibs.UndoRepeat import UndoContext

# reload(riggen)
# reload(frui)

class MainGUI( BaseInterface.BasePsWindow ):
    '''
    Main GUI for FR_RiggingTool
    '''
    
    def __init__(self, *args):
        '''
        Constructor of main GUI for FR_RiggingTool
        '''
        
        UIfile = BaseFile.BasePath( os.path.join( os.path.dirname( __file__ ), 'FR_RiggingTool.ui' ) )
        super( MainGUI, self ).__init__( UIfile, *args )