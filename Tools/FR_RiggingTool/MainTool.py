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
from FrMaya.Core.FrInterface import BaseInterface
from FrMaya.Core.FrFile import BaseFile
from FrMaya.Core.FrUtilities import UndoRepeat
from FrMaya.Core.FrRigging import BaseRigging
import os, glob

from functools import partial

# reload(BaseRigging)
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
        
        ## MAIN TOOL ##
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
        
        ## SRT TAB ##
        # Reset srt ui list
        ResetSRTGrp = [ self.ui.r_translate_btn, self.ui.r_rotate_btn, self.ui.r_scale_btn,
                       self.ui.r_visibility_btn, self.ui.r_rotateorder_btn ]
        
        # Loop through ui list and connect it to resetSRT_pressed slot
        for o in ResetSRTGrp:
            o.pressed.connect( partial( self.resetSRT_pressed, o ) )
        
        # Lock hide checkbox ui Dictionary
        LockHideCheckGrp = { 'translateX' : self.ui.lh_tx_check, 'translateY' : self.ui.lh_ty_check, 'translateZ' : self.ui.lh_tz_check,
                            'rotateX' : self.ui.lh_rx_check, 'rotateY' : self.ui.lh_ry_check, 'rotateZ' : self.ui.lh_rz_check,
                            'scaleX' : self.ui.lh_sx_check, 'scaleY' : self.ui.lh_sy_check, 'scaleZ' : self.ui.lh_sz_check,
                            'visibility' : self.ui.lh_vis_check, 'rotateorder' : self.ui.lh_rotateorder_check }
        
        # Lock hide check all ui list
        LockHideAllGrp = [ self.ui.lh_tall_check, self.ui.lh_rall_check, self.ui.lh_sall_check ]
        
        # Loop through check all ui list and connect it to lockHide_stateChanged slot
        for o in LockHideAllGrp:
            o.stateChanged.connect( partial( self.lockHide_stateChanged, o, LockHideCheckGrp ) )
        
        # Lock hide button group ui list
        LockHideBtnGrp = [ self.ui.lh_k_btn, self.ui.lh_l_btn, self.ui.lh_h_btn,
                       self.ui.lh_uk_btn, self.ui.lh_ul_btn, self.ui.lh_uh_btn ]
        
        # Loop through ui list and connect it to lockHide_pressed slot
        for o in LockHideBtnGrp:
            o.pressed.connect( partial( self.lockHide_pressed, o, LockHideCheckGrp ) )
    
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
    
    @UndoRepeat.Undoable
    def resetSRT_pressed(self, sender, *args):
        '''
        Slot for pressed signal from reset transform group widget
        
        :param sender: One of reset transform group widget
        '''
        
        # Collect selection
        selection = pm.ls( os = True )
        
        # Zero out translate
        if sender == self.ui.r_translate_btn:
            BaseRigging.zerooutTransform( selection, mode = 'translate' )
        # Zero out rotate
        elif sender == self.ui.r_rotate_btn:
            BaseRigging.zerooutTransform( selection, mode = 'rotate' )
        # Zero out scale
        elif sender == self.ui.r_scale_btn:
            BaseRigging.zerooutTransform( selection, mode = 'scale' )
        # Normalize visibility
        elif sender == self.ui.r_visibility_btn:
            BaseRigging.zerooutTransform( selection, mode = 'visibility' )
        # Normalize rotate order
        elif sender == self.ui.r_rotateorder_btn:
            BaseRigging.zerooutTransform( selection, mode = 'rotateorder' )
    
    def lockHide_stateChanged(self, sender, checkbox, *args):
        '''
        Slot for state changed signal from lock hide check all group widget
        
        :param sender: One of check all group widget
        :param checkbox: Collection of lock hide checkbox widget
        '''
        
        # Declare variable
        srt = ''
        xyz = ['X','Y','Z']
        
        # Which of the check all group supplied to this slot
        if sender == self.ui.lh_tall_check:
            srt = 'translate'
        if sender == self.ui.lh_rall_check:
            srt = 'rotate'
        if sender == self.ui.lh_sall_check:
            srt = 'scale'
        
        # Change checkbox widget based on check all widget
        for o in xyz:
            checkbox[srt + o].setCheckState( sender.checkState() )
    
    @UndoRepeat.Undoable
    def lockHide_pressed(self, sender, checkbox, *args):
        '''
        Slot for pressed signal from lock hide button group widget
        
        :param sender: One of lock hide button group widget
        :param checkbox: Collection of lock hide checkbox widget
        '''
        
        # Collect which attribute that will lock, hide, or make keyable
        attrubuteList = [ o for o in checkbox if checkbox[o].isChecked() == True ]
        
        # Collect selection
        selection = pm.ls( os = True )
        
        # Make keyable
        if sender == self.ui.lh_k_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, keyable = True )
        # Lock attribute
        if sender == self.ui.lh_l_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, lock = True )
        # Hide attribute
        if sender == self.ui.lh_h_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, hide = True )
        # Make unkeyable
        if sender == self.ui.lh_uk_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, keyable = False )
        # Unlock attribute
        if sender == self.ui.lh_ul_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, lock = False )
        # Unhide attribute
        if sender == self.ui.lh_uh_btn:
            BaseRigging.keylockhideAttribute( selection, attrubuteList, hide = False )

