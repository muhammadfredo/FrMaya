'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 23 Feb 2016
Purpose      : 

'''

# TODO: add repeatable decorator
# TODO: createControl is for basic create control
# TODO: while createFrControl is for control with tag and can be init with control FrNode

from functools import partial
import os

from FrMaya.Core.FrFile import BaseFile
from FrMaya.Core.FrInterface import BaseInterface
from FrMaya.Core.FrRigging import BaseRigging
from FrMaya.Core.FrUtilities import UndoRepeat

import pymel.core as pm

reload(BaseRigging)
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
                       self.ui.dis_none_btn, self.ui.dis_jnt_btn, self.ui.dis_axis_btn,
                       self.ui.dis_noaxis_btn ]

        # Loop through ui list and connect it to display_pressed slot 
        for o in DispalyGrp:
            o.pressed.connect( partial( self.display_pressed, o ) )

        # Pgroup group ui list
        PgroupGrp = { 'all' : self.ui.pgroup_all_check, 'button' : self.ui.pgroup_btn,
                      'rename' : self.ui.pgroup_rename_txt, 'suffix' : self.ui.pgroup_suffix_txt }

        # Connect pgroup_btn to the pgroup slot
        PgroupGrp['button'].pressed.connect( partial( self.pgroup_pressed, PgroupGrp ) )

        # Align group ui list
        AlignGrp = [ self.ui.align_transform_btn, self.ui.align_translate_btn, self.ui.align_rotate_btn ]

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

        ## Joint TAB ##
        # Joint creation button group ui list
        JointCreationBtnGrp = [ self.ui.jc_create_btn, self.ui.jc_insert_btn, self.ui.jc_reroot_btn,
                                self.ui.jc_split_btn ]
        JointCreationOptGrp = { 'splitCount' : self.ui.jc_splitCount_dsb, 'replace' : self.ui.jc_replace_check }

        # Loop through ui list and connect it to jointCreation_pressed slot
        for o in JointCreationBtnGrp:
            o.pressed.connect( partial( self.jointCreation_pressed, o, JointCreationOptGrp ) )

        # Comet joint orient button group ui list
        JointOrientBtnGrp = [ self.ui.jo_worldupX_btn, self.ui.jo_worldupY_btn, self.ui.jo_worldupZ_btn,
                                self.ui.jo_orient_btn ]
        JointOrientOptGrp = { 'aimX' : self.ui.jo_aimX_rdbtn, 'aimY' : self.ui.jo_aimY_rdbtn, 'aimZ' : self.ui.jo_aimZ_rdbtn,
                              'upX': self.ui.jo_upX_rdbtn, 'upY': self.ui.jo_upY_rdbtn, 'upZ': self.ui.jo_upZ_rdbtn,
                              'wupX': self.ui.jo_worldupX_dspn, 'wupY': self.ui.jo_worldupY_dspn, 'wupZ': self.ui.jo_worldupZ_dspn,
                              'aimFlip': self.ui.jo_aimFlip_check, 'upFlip': self.ui.jo_upFlip_check, 'worldupAuto': self.ui.jo_worldupAuto_check }

        for o in JointOrientBtnGrp:
            o.pressed.connect( partial( self.jointOrient_pressed, o, JointOrientOptGrp ) )

        # Mirror joint button group ui list
        MirrorJointBtnGrp = [ self.ui.mj_mirror_btn, self.ui.mj_change_btn ]
        MirrorJointOptGrp = { 'acrossXY' : self.ui.mj_XY_rdbtn, 'acrossYZ' : self.ui.mj_YZ_rdbtn, 'acrossXZ' : self.ui.mj_XZ_rdbtn,
                              'fnBehave' : self.ui.mj_behaviour_rdbtn, 'fnOrient' : self.ui.mj_orientation_rdbtn,
                              'search' : self.ui.mj_search_txt, 'replace' : self.ui.mj_replace_txt }

        for o in MirrorJointBtnGrp:
            o.pressed.connect( partial( self.mirrorJoint_pressed, o, MirrorJointOptGrp ) )

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
        axisBool = sender == self.ui.dis_axis_btn
        noaxisBool = sender == self.ui.dis_noaxis_btn

        selection = pm.ls( os = True )
        # displayLocalAxis
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
        if overBool:
            for o in selection: o.overrideEnabled.set( False )

        # Change joint draw style to None or Joint
        if noneBool or jntBool:
            # filtered selection joint only
            selection = pm.ls( selection, type = "joint" )
            # if none selected, select all joint in scene
            if len(selection) == 0:
                selection = pm.ls( type = 'joint' )
            
            if noneBool:
                disDraw = 2
            elif jntBool:
                disDraw = 0

            for o in selection: o.drawStyle.set( disDraw )

        # Display local axis
        if axisBool or noaxisBool:
            # if none selected, select all joint in scene
            if len( selection ) == 0:
                selection = pm.ls( type = 'joint' )

            if axisBool:
                disAxis = True
            elif noaxisBool:
                disAxis =False

            for o in selection: o.displayLocalAxis.set( disAxis )
    
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
        
        # Align transform mode on selection
        if sender == self.ui.align_transform_btn:
            BaseRigging.alignMath( selection[0], selection[1], mode = 'transform' )
        # Align translate mode on selection
        elif sender == self.ui.align_translate_btn:
            BaseRigging.alignMath( selection[0], selection[1], mode = 'translate' )
        # Align rotate mode on selection
        elif sender == self.ui.align_rotate_btn:
            BaseRigging.alignMath( selection[0], selection[1], mode = 'rotate' )
    
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
    
    @UndoRepeat.Undoable
    def jointCreation_pressed(self, sender, option, *args):
        '''
        Slot for pressed signal from joint creation button group widget
        
        :param sender: One of joint creation button group widget
        '''
        
        # Active joint tool
        if sender == self.ui.jc_create_btn:
            pm.mel.JointTool()
        # Active insert joint tool
        if sender == self.ui.jc_insert_btn:
            pm.mel.InsertJointTool()
        # Active reroot joint function
        if sender == self.ui.jc_reroot_btn:
            pm.mel.RerootSkeleton()
        # Split selected joint
        if sender == self.ui.jc_split_btn:
            sel = pm.ls( os = True, type = 'joint' )
            if len(sel) > 0:
                BaseRigging.jointSplit( sel[0], option['splitCount'].value(), option['replace'].isChecked() )

    # TODO: below is not yet documented
    def boolToNumber(self, value, flip):
        flipVal = 1
        if flip:
            flipVal = -1

        if value:
            return 1.0 * flipVal
        else:
            return 0.0 * flipVal

    def getVecOptionOrient(self, mode, option ):
        output = [ 0, 0, 0 ]
        axis = [ 'X', 'Y', 'Z' ]
        aimFlip = option['aimFlip'].checkState()
        upFlip = option['upFlip'].checkState()

        if mode == 'aimAxis':
            for i, o in enumerate(axis):
                output[i] = self.boolToNumber( option['aim'+o].isChecked(), aimFlip )
        elif mode == 'upAxis':
            for i, o in enumerate(axis):
                output[i] = self.boolToNumber( option['up'+o].isChecked(), upFlip )
        elif mode == 'upDir':
            for i, o in enumerate(axis):
                output[i] = option['wup'+o].value()

        return  output

    @UndoRepeat.Undoable
    def jointOrient_pressed(self, sender, option, *args):
        axis = [ 'X', 'Y', 'Z' ]
        axisVal = [ 0, 0, 0 ]

        # set axisVal to X
        if sender == self.ui.jo_worldupX_btn:
            axisVal = [ 1, 0, 0 ]
        # set axisVal to Y
        if sender == self.ui.jo_worldupY_btn:
            axisVal = [ 0, 1, 0 ]
        # set axisVal to Z
        if sender == self.ui.jo_worldupZ_btn:
            axisVal = [ 0, 0, 1 ]
        # set worldup ui according axisVal
        if axisVal != [0,0,0]:
            for i, o in enumerate(axis):
                option['wup'+o].setValue( axisVal[i] )

        # CometOrient selected joint
        if sender == self.ui.jo_orient_btn:
            sel = pm.ls(os=True, type = 'joint')

            aimAxis = self.getVecOptionOrient( 'aimAxis', option )
            upAxis = self.getVecOptionOrient( 'upAxis', option )
            upDir = self.getVecOptionOrient( 'upDir', option )

            BaseRigging.cometJoint_orient( sel, aimAxis = aimAxis, upAxis = upAxis, upDir = upDir,
                                           doAuto = option[ 'worldupAuto' ].checkState() )

            pm.select( sel )

    @UndoRepeat.Undoable
    def mirrorJoint_pressed(self, sender, option, *args):
        src = option['search'].text()
        re = option['replace'].text()

        if sender == self.ui.mj_change_btn:
            option['search'].setText( re )
            option['replace'].setText( src )

        if sender == self.ui.mj_mirror_btn:
            jointSelected = pm.ls( os = True, type = 'joint' )

            pm.mirrorJoint( jointSelected, mirrorBehavior = option['fnBehave'].isChecked(),
                            mirrorXY = option['acrossXY'].isChecked(),
                            mirrorXZ = option['acrossXZ'].isChecked(),
                            mirrorYZ = option['acrossYZ'].isChecked(),
                            searchReplace = ( src, re ) )



