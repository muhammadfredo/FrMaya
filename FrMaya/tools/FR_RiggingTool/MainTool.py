"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 23 Feb 2016
Purpose      :
# TODO: add repeatable decorator
# TODO: createControl is for basic create control
# TODO: while createFrControl is for control with tag and can be init with control FrNode
# TODO: clean this shit
# TODO: crete joint on selection only work on vertex

"""
from functools import partial
import copy

import pymel.core as pm

import FrMaya.core.uimaya
import FrMaya.utility as util
from FrMaya.vendor import path

from FrMaya.core import FrRigging


class MainGUI(FrMaya.core.uimaya.MyQtWindow):
    """
    Main GUI for FR_RiggingTool
    """

    def __init__(self, *args):
        """
        Constructor of main GUI for FR_RiggingTool
        """

        # Convert ui path file as FrFile Object
        ui_file = path.Path(__file__).parent / 'FR_RiggingTool.ui'
        super(MainGUI, self).__init__(ui_file, title_tool = 'FR_RiggingTool', *args)

        self.connect_event_handlers()

    def connect_event_handlers(self):
        """
        Connect event handler/sender from UI to slot
        """

        ## MAIN TOOL ##
        # Display group ui list
        dispaly_grp = [self.ui.dis_over_btn, self.ui.dis_ref_btn, self.ui.dis_norm_btn, self.ui.dis_none_btn,
                       self.ui.dis_jnt_btn, self.ui.dis_axis_btn, self.ui.dis_noaxis_btn]

        # Loop through ui list and connect it to display_pressed slot 
        for o in dispaly_grp:
            o.pressed.connect(partial(self.display_pressed, o))

        # Align group ui list
        align_grp = [self.ui.align_transform_btn, self.ui.align_translate_btn, self.ui.align_rotate_btn]

        # Loop through ui list and connect it to align_pressed slot
        for o in align_grp:
            o.pressed.connect(partial(self.align_pressed, o))

        # Freeze transform group ui list
        freeze_tm_grp = [self.ui.ft_all_btn, self.ui.ft_translate_btn, self.ui.ft_rotate_btn, self.ui.ft_scale_btn]

        # Loop through ui list and connect it to freeze_tm_pressed slot
        for o in freeze_tm_grp:
            o.pressed.connect(partial(self.freeze_tm_pressed, o))

        ## SRT TAB ##
        # Reset srt ui list
        reset_srt_grp = [self.ui.r_translate_btn, self.ui.r_rotate_btn, self.ui.r_scale_btn, self.ui.r_visibility_btn,
                         self.ui.r_rotateorder_btn]

        # Loop through ui list and connect it to reset_srt_pressed slot
        for o in reset_srt_grp:
            o.pressed.connect(partial(self.reset_srt_pressed, o))

        # Lock hide checkbox ui Dictionary
        lock_hide_check_grp = {'translateX': self.ui.lh_tx_check, 'translateY': self.ui.lh_ty_check,
                               'translateZ': self.ui.lh_tz_check, 'rotateX': self.ui.lh_rx_check,
                               'rotateY': self.ui.lh_ry_check, 'rotateZ': self.ui.lh_rz_check,
                               'scaleX': self.ui.lh_sx_check, 'scaleY': self.ui.lh_sy_check,
                               'scaleZ': self.ui.lh_sz_check, 'visibility': self.ui.lh_vis_check,
                               'rotateorder': self.ui.lh_rotateorder_check}

        # Lock hide check all ui list
        lock_hide_all_grp = [self.ui.lh_tall_check, self.ui.lh_rall_check, self.ui.lh_sall_check]

        # Loop through check all ui list and connect it to lockhide_state_changed slot
        for o in lock_hide_all_grp:
            o.stateChanged.connect(partial(self.lockhide_state_changed, o, lock_hide_check_grp))

        # Lock hide button group ui list
        lock_hide_btn_grp = [self.ui.lh_k_btn, self.ui.lh_l_btn, self.ui.lh_h_btn, self.ui.lh_uk_btn, self.ui.lh_ul_btn,
                             self.ui.lh_uh_btn]

        # Loop through ui list and connect it to lockhide_pressed slot
        for o in lock_hide_btn_grp:
            o.pressed.connect(partial(self.lockhide_pressed, o, lock_hide_check_grp))

        ## Joint TAB ##
        # Joint creation button group ui list
        joint_creation_btn_grp = [self.ui.jc_create_btn, self.ui.jc_insert_btn, self.ui.jc_reroot_btn,
                                  self.ui.jc_split_btn, self.ui.jc_createonsel_btn]
        joint_creation_opt_grp = {'splitCount': self.ui.jc_splitCount_dsb, 'replace': self.ui.jc_replace_check}

        # Loop through ui list and connect it to joint_creation_pressed slot
        for o in joint_creation_btn_grp:
            o.pressed.connect(partial(self.joint_creation_pressed, o, joint_creation_opt_grp))

        # Comet joint orient button group ui list
        joint_orient_btn_grp = [self.ui.jo_worldupX_btn, self.ui.jo_worldupY_btn, self.ui.jo_worldupZ_btn,
                                self.ui.jo_orient_btn]
        joint_orient_opt_grp = {'aimX': self.ui.jo_aimX_rdbtn, 'aimY': self.ui.jo_aimY_rdbtn,
                                'aimZ': self.ui.jo_aimZ_rdbtn, 'upX': self.ui.jo_upX_rdbtn, 'upY': self.ui.jo_upY_rdbtn,
                                'upZ': self.ui.jo_upZ_rdbtn, 'wupX': self.ui.jo_worldupX_dspn,
                                'wupY': self.ui.jo_worldupY_dspn, 'wupZ': self.ui.jo_worldupZ_dspn,
                                'aimFlip': self.ui.jo_aimFlip_check, 'upFlip': self.ui.jo_upFlip_check,
                                'worldupAuto': self.ui.jo_worldupAuto_check}

        for o in joint_orient_btn_grp:
            o.pressed.connect(partial(self.joint_orient_pressed, o, joint_orient_opt_grp))

        # Mirror joint button group ui list
        mirror_joint_btn_grp = [self.ui.mj_mirror_btn, self.ui.mj_change_btn]
        mirror_joint_opt_grp = {'acrossXY': self.ui.mj_XY_rdbtn, 'acrossYZ': self.ui.mj_YZ_rdbtn,
                                'acrossXZ': self.ui.mj_XZ_rdbtn, 'fnBehave': self.ui.mj_behaviour_rdbtn,
                                'fnOrient': self.ui.mj_orientation_rdbtn, 'search': self.ui.mj_search_txt,
                                'replace': self.ui.mj_replace_txt}

        for o in mirror_joint_btn_grp:
            o.pressed.connect(partial(self.mirror_joint_pressed, o, mirror_joint_opt_grp))

        ## Control TAB ##
        # Color overide group ui list
        coloroveride_btn_grp = [self.ui.color_06_btn, self.ui.color_09_btn, self.ui.color_13_btn, self.ui.color_14_btn,
                                self.ui.color_17_btn]

        for o in coloroveride_btn_grp:
            o.pressed.connect(partial(self.coloroveride_pressed, o))

        # Control creation setting group ui list
        control_setting_grp = {'suffix': self.ui.cc_suffix_txt, 'group': self.ui.cc_group_txt,
                               'posrot': self.ui.cc_posrot_check, 'scale': self.ui.cc_scale_check,
                               'controllist': self.ui.cc_clist_cb, 'search': self.ui.cc_search_txt,
                               'replace': self.ui.cc_replace_txt}

        # Populate control list combo box
        control_files = FrRigging.getControlFiles()
        for o in control_files:
            control_setting_grp['controllist'].addItem(o.stem, o)

        self.ui.cc_create_btn.pressed.connect(
            partial(self.create_control_pressed, self.ui.cc_create_btn, control_setting_grp))

        # Pgroup group ui list
        pgroup_grp = {'world': self.ui.pgroup_world_check, 'button': self.ui.pgroup_btn,
                      'search': self.ui.pgroup_search_txt, 'replace': self.ui.pgroup_replace_txt}

        # Connect pgroup_btn to the pgroup slot
        pgroup_grp['button'].pressed.connect(partial(self.pgroup_pressed, pgroup_grp))

    @util.undoable
    def display_pressed(self, sender):
        """
        Slot for pressed signal form display grup widget

        :param sender: One of display grup widget
        """

        # Check and compare sender to Display group ui
        over_bool = sender == self.ui.dis_over_btn
        ref_bool = sender == self.ui.dis_ref_btn
        norm_bool = sender == self.ui.dis_norm_btn
        none_bool = sender == self.ui.dis_none_btn
        jnt_bool = sender == self.ui.dis_jnt_btn
        axis_bool = sender == self.ui.dis_axis_btn
        noaxis_bool = sender == self.ui.dis_noaxis_btn

        selection = pm.ls(os = True)
        # displayLocalAxis
        # Change node display type to reference or normal
        if ref_bool or norm_bool:
            if ref_bool:
                dis_draw = 2
            elif norm_bool:
                dis_draw = 0
            else:
                dis_draw = 0

            for o in selection:
                o.overrideEnabled.set(True)
                o.overrideDisplayType.set(dis_draw)

        # Turn off overrideEnabled attribute
        if over_bool:
            for o in selection:
                o.overrideEnabled.set(False)

        # Change joint draw style to None or Joint
        if none_bool or jnt_bool:
            # filtered selection joint only
            selection = pm.ls(selection, type = "joint")
            # if none selected, select all joint in scene
            if len(selection) == 0:
                selection = pm.ls(type = 'joint')

            if none_bool:
                dis_draw = 2
            elif jnt_bool:
                dis_draw = 0
            else:
                dis_draw = 0

            for o in selection:
                o.drawStyle.set(dis_draw)

        # Display local axis
        if axis_bool or noaxis_bool:
            # if none selected, select all joint in scene
            if len(selection) == 0:
                selection = pm.ls(type = 'joint')

            if axis_bool:
                dis_axis = True
            elif noaxis_bool:
                dis_axis = False
            else:
                dis_axis = False

            for o in selection:
                o.displayLocalAxis.set(dis_axis)

    @util.undoable
    def pgroup_pressed(self, sender):
        """
        Slot for pressed signal form pgroup_btn widget

        :param sender: Dictionary of pgroup widgets
        """

        # Collect selection
        selection = pm.ls(os = True)

        # Perform pgroup operation on the selection
        FrRigging.pgroup(selection, world = sender['world'].isChecked(), re = sender['search'].text(),
                         suffix = sender['replace'].text())

    @util.undoable
    def align_pressed(self, sender):
        """
        Slot for pressed signal form align grup widget

        :param sender: One of align group widget
        """

        # Collect selection
        selection = pm.ls(os = True)

        # Align transform mode on selection
        if sender == self.ui.align_transform_btn:
            FrRigging.alignMath(selection[0], selection[1], mode = 'transform')
        # Align translate mode on selection
        elif sender == self.ui.align_translate_btn:
            FrRigging.alignMath(selection[0], selection[1], mode = 'translate')
        # Align rotate mode on selection
        elif sender == self.ui.align_rotate_btn:
            FrRigging.alignMath(selection[0], selection[1], mode = 'rotate')

    @util.undoable
    def freeze_tm_pressed(self, sender):
        """
        Slot for pressed signal from freeze transform group widget

        :param sender: One of freeze transform group widget
        """

        # Collect selection
        selection = pm.ls(os = True)

        # Freeze transform on selection
        if sender == self.ui.ft_all_btn:
            FrRigging.freezeTransform(selection)
        # Freeze translate on selection
        elif sender == self.ui.ft_translate_btn:
            FrRigging.freezeTransform(selection, mode = 'translate')
        # Freeze rotation on selection
        elif sender == self.ui.ft_rotate_btn:
            FrRigging.freezeTransform(selection, mode = 'rotate')
        # Freeze scale on selection
        elif sender == self.ui.ft_scale_btn:
            FrRigging.freezeTransform(selection, mode = 'scale')

    @util.undoable
    def reset_srt_pressed(self, sender):
        """
        Slot for pressed signal from reset transform group widget

        :param sender: One of reset transform group widget
        """

        # Collect selection
        selection = pm.ls(os = True)

        # Zero out translate
        if sender == self.ui.r_translate_btn:
            FrRigging.zerooutTransform(selection, mode = 'translate')
        # Zero out rotate
        elif sender == self.ui.r_rotate_btn:
            FrRigging.zerooutTransform(selection, mode = 'rotate')
        # Zero out scale
        elif sender == self.ui.r_scale_btn:
            FrRigging.zerooutTransform(selection, mode = 'scale')
        # Normalize visibility
        elif sender == self.ui.r_visibility_btn:
            FrRigging.zerooutTransform(selection, mode = 'visibility')
        # Normalize rotate order
        elif sender == self.ui.r_rotateorder_btn:
            FrRigging.zerooutTransform(selection, mode = 'rotateorder')

    def lockhide_state_changed(self, sender, checkbox):
        """
        Slot for state changed signal from lock hide check all group widget

        :param sender: One of check all group widget
        :param checkbox: Collection of lock hide checkbox widget
        """

        # Declare variable
        srt = ''
        xyz = ['X', 'Y', 'Z']

        # Which of the check all group supplied to this slot
        if sender == self.ui.lh_tall_check:
            srt = 'translate'
        if sender == self.ui.lh_rall_check:
            srt = 'rotate'
        if sender == self.ui.lh_sall_check:
            srt = 'scale'

        # Change checkbox widget based on check all widget
        for o in xyz:
            checkbox[srt + o].setCheckState(sender.checkState())

    @util.undoable
    def lockhide_pressed(self, sender, checkbox):
        """
        Slot for pressed signal from lock hide button group widget

        :param sender: One of lock hide button group widget
        :param checkbox: Collection of lock hide checkbox widget
        """

        # Collect which attribute that will lock, hide, or make keyable
        attrubute_list = [o for o in checkbox if checkbox[o].isChecked() == True]

        # Collect selection
        selection = pm.ls(os = True)

        # Make keyable
        if sender == self.ui.lh_k_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, keyable = True)
        # Lock attribute
        if sender == self.ui.lh_l_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, lock = True)
        # Hide attribute
        if sender == self.ui.lh_h_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, hide = True)
        # Make unkeyable
        if sender == self.ui.lh_uk_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, keyable = False)
        # Unlock attribute
        if sender == self.ui.lh_ul_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, lock = False)
        # Unhide attribute
        if sender == self.ui.lh_uh_btn:
            FrRigging.keylockhideAttribute(selection, attrubute_list, hide = False)

    @util.undoable
    def joint_creation_pressed(self, sender, option):
        """
        Slot for pressed signal from joint creation button group widget

        :param option:
        :param sender: One of joint creation button group widget
        """

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
            sel = pm.ls(os = True, type = 'joint')
            if len(sel) > 0:
                FrRigging.jointSplit(sel[0], option['splitCount'].value(), option['replace'].isChecked())
        # Created joint on selected
        if sender == self.ui.jc_createonsel_btn:
            sel = pm.ls(os = True)
            # clear selection
            pm.select()
            # first loop check if there is a component
            new_selection = []
            for i, o in enumerate(sel):
                if type(o) == pm.MeshVertex:
                    if o.count > 1:
                        new_selection += [x for x in o]
                    else:
                        new_selection.append(o)
                else:
                    new_selection = copy.deepcopy(sel)
            result_jnt = []
            for o in new_selection:
                jnt = pm.createNode('joint')
                FrRigging.alignMath(jnt, o, mode = 'translate')
                result_jnt.append(jnt)

            # reselect the selection
            # pm.select(sel)
            pm.select(result_jnt)

    # TODO: below is not yet documented
    @staticmethod
    def bool_to_number(value, flip):
        flip_val = 1
        if flip:
            flip_val = -1

        if value:
            value = 1.0
        else:
            value = 0.0

        return value * flip_val

    def get_vec_orient(self, mode, option):
        output = [0, 0, 0]
        axis = ['X', 'Y', 'Z']
        aim_flip = option['aimFlip'].checkState()
        up_flip = option['upFlip'].checkState()

        if mode == 'aimAxis':
            for i, o in enumerate(axis):
                output[i] = self.bool_to_number(option['aim' + o].isChecked(), aim_flip)
        elif mode == 'upAxis':
            for i, o in enumerate(axis):
                output[i] = self.bool_to_number(option['up' + o].isChecked(), up_flip)
        elif mode == 'upDir':
            for i, o in enumerate(axis):
                output[i] = option['wup' + o].value()

        return output

    @util.undoable
    def joint_orient_pressed(self, sender, option):
        axis = ['X', 'Y', 'Z']
        axis_val = [0, 0, 0]

        # set axis_val to X
        if sender == self.ui.jo_worldupX_btn:
            axis_val = [1, 0, 0]
        # set axis_val to Y
        if sender == self.ui.jo_worldupY_btn:
            axis_val = [0, 1, 0]
        # set axis_val to Z
        if sender == self.ui.jo_worldupZ_btn:
            axis_val = [0, 0, 1]
        # set worldup ui according axis_val
        if axis_val != [0, 0, 0]:
            for i, o in enumerate(axis):
                option['wup' + o].setValue(axis_val[i])

        # CometOrient selected joint
        if sender == self.ui.jo_orient_btn:
            sel = pm.ls(os = True, type = 'joint')

            aim_axis = self.get_vec_orient('aimAxis', option)
            up_axis = self.get_vec_orient('upAxis', option)
            up_dir = self.get_vec_orient('upDir', option)

            FrRigging.cometJoint_orient(sel, aimAxis = aim_axis, upAxis = up_axis, upDir = up_dir,
                                        doAuto = option['worldupAuto'].checkState())

            pm.select(sel)

    @util.undoable
    def mirror_joint_pressed(self, sender, option):
        src = option['search'].text()
        re = option['replace'].text()

        if sender == self.ui.mj_change_btn:
            option['search'].setText(re)
            option['replace'].setText(src)

        if sender == self.ui.mj_mirror_btn:
            joint_selected = pm.ls(os = True, type = 'joint')

            pm.mirrorJoint(joint_selected, mirrorBehavior = option['fnBehave'].isChecked(),
                           mirrorXY = option['acrossXY'].isChecked(), mirrorXZ = option['acrossXZ'].isChecked(),
                           mirrorYZ = option['acrossYZ'].isChecked(), searchReplace = (src, re))

    @util.undoable
    def coloroveride_pressed(self, sender):
        sel = pm.ls(os = True)
        color_val = int(sender.objectName().split('_')[1])

        for o in sel:
            for x in o.getShapes():
                x.overrideEnabled.set(True)
                x.overrideColor.set(color_val)

    @util.undoable
    def create_control_pressed(self, sender, setting):
        controllist = setting['controllist']
        sel = pm.ls(os = True)
        searchtext = setting['search'].text()
        replacetext = setting['replace'].text()
        suffixtext = setting['suffix'].text()
        grouptext = setting['group'].text()
        posrot_cons = setting['posrot'].isChecked()
        scale_cons = setting['scale'].isChecked()

        item_data = controllist.itemData(controllist.currentIndex())
        tm_list = [(o.getMatrix(worldSpace = True), o) for o in sel]
        group_list = [o for o in grouptext.split(';') if o]

        if not tm_list:
            tm_list.append((pm.dt.Matrix(), None))

        for tm, object_node in tm_list:
            object_name = 'Control'
            if object_node:
                object_name = object_node.name()
            object_name = object_name.replace(searchtext, replacetext)
            if object_name[len(object_name) - 1] == '_':
                object_name = object_name[:-1]
            # createControl(filenode, name = '', suffix = 'Ctl', transform = None, color = None, group = ['Grp'])
            result = FrRigging.createControl(item_data, name = object_name, transform = tm, suffix = suffixtext,
                                             group = group_list)

            # parent cons
            if posrot_cons and object_node:
                pm.parentConstraint(result.control, object_node, mo = True)

            # scale cons
            if scale_cons and object_node:
                pm.scaleConstraint(result.control, object_node, mo = True)

        if sender == self.ui.cc_create_btn:
            print 'create control'



