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
import pymel.core as pm
# import FRtools.rigging.general as riggen
# import FRtools.rigging.modules.general as rigmod
# import FRtools.ui.FR_BaseQWidget as frui
from FrMaya.Core.FrInterface import BaseInterface
from FrMaya.Core.FrFile import BaseFile
from FrMaya.Core.FrUtilities import UndoRepeat
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
        
        self.Connect_EventHandlers()
    
    def Connect_EventHandlers(self):
        '''
        Connect event handler from UI to method
        '''
        
        # Display
        self.ui.dis_ref_btn.pressed.connect( self.display_pressed )
        self.ui.dis_norm_btn.pressed.connect( self.display_pressed )
        self.ui.dis_none_btn.pressed.connect( self.display_pressed )
        self.ui.dis_jnt_btn.pressed.connect( self.display_pressed )
    
    @UndoRepeat.Undoable
    def display_pressed(self, *args):
        print 'yohooo'
        sender = self.sender()
        print sender
        refBool = sender == self.ui.dis_ref_btn
        normBool = sender == self.ui.dis_norm_btn
        noneBool = sender == self.ui.dis_none_btn
        jntBool = sender == self.ui.dis_jnt_btn
        
        # referance or normal display type
        if refBool or normBool:
            selection = pm.ls( os = True )
            
            attrType = ".overrideDisplayType"
            
            if refBool:
                disDraw = 2
            elif normBool:
                disDraw = 0
        # none or joint draw style
        elif noneBool or jntBool:
            selection = pm.ls( os = True, type = "joint" )
            
            attrType = ".drawStyle"
            
            if noneBool:
                disDraw = 2
            elif jntBool:
                disDraw = 0
        
        for o in selection:
            if refBool or normBool:
                pm.setAttr( o + ".overrideEnabled", 1 )
            pm.setAttr( o + attrType, disDraw )