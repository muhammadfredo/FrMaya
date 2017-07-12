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

import pymel.core as pm
# import FRtools.rigging.general as riggen
# import FRtools.rigging.modules.general as rigmod
# import FRtools.ui.FR_BaseQWidget as frui
from FrMaya.Core.FrInterface import BaseInterface
from FrMaya.Core.FrFile import BaseFile
from FrMaya.Core.FrUtilities import UndoRepeat
import os, glob

from functools import partial

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
        
        # Convert ui path file as FrFile Object
        UIfile = BaseFile.BasePath( os.path.join( os.path.dirname( __file__ ), 'FR_RiggingTool.ui' ) )
        super( MainGUI, self ).__init__( UIfile, *args )
        
        self.Connect_EventHandlers()
    
    def Connect_EventHandlers(self):
        '''
        Connect event handler from UI to method
        '''
        
        # Display group ui list
        DispalyGrp = [ self.ui.dis_over_btn, self.ui.dis_ref_btn, self.ui.dis_norm_btn,
                      self.ui.dis_none_btn, self.ui.dis_jnt_btn ]
        
        # Loop through ui list and connect it to method 
        for o in DispalyGrp:
            o.pressed.connect( partial( self.display_pressed, o ) )
    
    @UndoRepeat.Undoable
    def display_pressed(self, sender, *args):
        '''
        Slot for pressed signal form display grup widget
        
        :param sender: one of display grup widget
        '''
        
        # Check and compare sender to Display group ui
        overBool = sender == self.ui.dis_over_btn
        refBool = sender == self.ui.dis_ref_btn
        normBool = sender == self.ui.dis_norm_btn
        noneBool = sender == self.ui.dis_none_btn
        jntBool = sender == self.ui.dis_jnt_btn
        
        selection = pm.ls( os = True )
        
        # Change node display type to reference or normal
        if refBool or normBool:
            if refBool:
                disDraw = 2
            elif normBool:
                disDraw = 0
            
            for o in selection:
                o.overrideEnabled.set( True )
                o.overrideDisplayType.set( disDraw )
        # Turn off overrideEnabled attribute
        elif overBool:
            for o in selection: o.overrideEnabled.set( False )
        # Change joint draw style to None or Joint
        elif noneBool or jntBool:
            selection = pm.ls( os = True, type = "joint" )
            
            if noneBool:
                disDraw = 2
            elif jntBool:
                disDraw = 0

            for o in selection: o.drawStyle.set( disDraw )