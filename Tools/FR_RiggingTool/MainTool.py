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
from FrMaya.Core.FrRigging import BaseRigging
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
        Connect event handler/sender from UI to slot
        '''
        
        # Display group ui list
        DispalyGrp = [ self.ui.dis_over_btn, self.ui.dis_ref_btn, self.ui.dis_norm_btn,
                      self.ui.dis_none_btn, self.ui.dis_jnt_btn ]
        
        # Loop through ui list and connect it to display_pressed slot 
        for o in DispalyGrp:
            o.pressed.connect( partial( self.display_pressed, o ) )
        
        # Pgroup group ui list
        PgroupGrp = { 'all' : self.ui.pgroup_all_check, 'button' : self.ui.pgroup_btn,
                     'rename' : self.ui.pgroup_rename_txt, 'suffix' : self.ui.pgroup_suffix_txt }
        
        # Connect pgroup_btn to the pgroup slot
        PgroupGrp['button'].pressed.connect( partial( self.pgroup_pressed, PgroupGrp ) )
        
        # Align group ui list
        AlignGrp = [ self.ui.align_translate_btn, self.ui.align_rotate_btn ]
        
        # Loop through ui list and connect it to align_pressed slot
        for o in AlignGrp:
            o.pressed.connect( partial( self.align_pressed, o ) )
        
        # Freeze transform group ui list
        FreezeTMGrp = [ self.ui.ft_all_btn, self.ui.ft_translate_btn,
                       self.ui.ft_rotate_btn, self.ui.ft_scale_btn ]
        
        # Loop through ui list and connect it to freezeTM_pressed slot
        for o in FreezeTMGrp:
            o.pressed.connect( partial( self.freezeTM_pressed, o ) )
    
    @UndoRepeat.Undoable
    def display_pressed(self, sender, *args):
        '''
        Slot for pressed signal form display grup widget
        
        :param sender: One of display grup widget
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
    
    @UndoRepeat.Undoable
    def pgroup_pressed(self, sender, *args):
        '''
        Slot for pressed signal form pgroup_btn widget
        
        :param sender: Dictionary of pgroup widgets
        '''
        
        # Collect selection
        selection = pm.ls( os = True )
        
        # Perform pgroup operation on the selection
        BaseRigging.pgroup( selection, world = sender['all'].isChecked(),
                            re = sender['rename'].toPlainText(),
                            suffix = sender['suffix'].toPlainText() )
    
    @UndoRepeat.Undoable
    def align_pressed(self, sender, *args):
        '''
        Slot for pressed signal form align grup widget
         
        :param sender: One of align group widget
        '''
        
        # Collect selection
        selection = pm.ls( os = True )
        
        # Align translate mode on selection
        if sender == self.ui.align_translate_btn:
            BaseRigging.align( selection, mode = 'translate' )
        # Align rotate mode on selection
        elif sender == self.ui.align_rotate_btn:
            BaseRigging.align( selection, mode = 'rotate' )
    
    @UndoRepeat.Undoable
    def freezeTM_pressed(self, sender, *args):
        '''
        Slot for pressed signal from freeze transform group widget
        
        :param sender: One of freeze transform group widget
        '''
        
        # Collect selection
        selection = pm.ls( os = True )
        
        # Freeze transform on selection
        if sender == self.ui.ft_all_btn:
            BaseRigging.freezeTransform( selection )
        # Freeze translate on selection
        elif sender == self.ui.ft_translate_btn:
            BaseRigging.freezeTransform( selection, mode = 'translate' )
        # Freeze rotation on selection
        elif sender == self.ui.ft_rotate_btn:
            BaseRigging.freezeTransform( selection, mode = 'rotate' )
        # Freeze scale on selection
        elif sender == self.ui.ft_scale_btn:
            BaseRigging.freezeTransform( selection, mode = 'scale' )