"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 13 Sep 2020
Info         :

"""
import collections

import pymel.core as pm
from FrMaya.vendor import path

from FrMaya import utility as util
from . import system, general


def get_skincluster_node(input_object):
    """Get skincluster node from specified PyNode object.

    :arg input_object: PyNode object that have skincluster.
    :type input_object: pm.nt.Transform
    :rtype: pm.nt.SkinCluster
    """
    history_list = input_object.listHistory(pruneDagObjects = True, interestLevel = True)
    skin_node = None
    for o in history_list:
        if o.nodeType() == 'skinCluster':
            skin_node = o

    return skin_node


def get_skincluster_info(skin_node):
    """Get joint influence and skincluster method.

    :arg skin_node: Skincluster PyNode that need to get info extracted.
    :type skin_node: pm.nt.SkinCluster
    :return: Skincluster joint influence, Skin method index.
    :rtype: (list of pm.nt.Joint, int)
    """
    joint_list = []
    skin_method = 0
    if skin_node:
        joint_list = skin_node.getInfluence()
        skin_method = skin_node.getSkinMethod()

    return joint_list, skin_method


def remove_unused_influence(skin_node):
    """Remove zero weight influences on skincluster.

    :arg skin_node: PyNode skincluster need to remove unused influence.
    :type skin_node: pm.nt.SkinCluster
    :return: List of removed influences.
    :rtype: list of pm.PyNode
    """
    influence_list = skin_node.getInfluence()
    weight_inf_list = skin_node.getWeightedInfluence()
    # Set skinCluster to HasNoEffect so it won't process after each removal
    skin_node.nodeState.set(1)
    zero_weight_inf_list = list(set(influence_list) - set(weight_inf_list))
    skin_node.removeInfluence(zero_weight_inf_list)
    skin_node.nodeState.set(0)
    return zero_weight_inf_list


def transfer_skincluster(source_object, target_objects):
    """Bind the target objects based on source object,
    then copied the skin data from source to target objects.
    If target object have skincluster,
    it will get replaced by new skincluster.

    :arg source_object: PyNode object transfer source.
    :type source_object: pm.PyNode
    :arg target_objects: PyNode objects transfer destination.
    :type target_objects: list of pm.PyNode
    :rtype: None
    """
    source_skin_node = get_skincluster_node(source_object)
    assert source_skin_node, 'Skincluster not found on source object.'
    joint_list, skin_method = get_skincluster_info(source_skin_node)
    for tgt_obj in target_objects:
        old_tgt_skin_node = get_skincluster_node(tgt_obj)
        if old_tgt_skin_node:
            old_tgt_skin_node.unbind()
        try:
            tgt_skin_node = pm.skinCluster(joint_list, tgt_obj, bindMethod = skin_method)
        except:
            tgt_skin_node = pm.skinCluster(joint_list, tgt_obj)
        pm.copySkinWeights(
            sourceSkin = source_skin_node,
            destinationSkin = tgt_skin_node,
            noMirror = True,
            surfaceAssociation = 'closestPoint',
            influenceAssociation = ['name', 'oneToOne', 'closestJoint'],
        )
        remove_unused_influence(tgt_skin_node)


def get_control_files(name = ''):
    """Collect all control files from all path in FR_CONTROLCURVE.

    :key name: If specified, only return control file of a specified name.
    :type name: str
    :rtype: list of path.Path
    """
    # get all control folder path
    control_dir_list = system.get_control_curve_path()
    # collect all control files and flatten it
    control_files = [control_dir.glob('*.json') for control_dir in control_dir_list]
    control_files = util.flatten(control_files)
    if name:
        control_files = [o for o in control_files if o.filename == name]

    return control_files


def create_control(control_file, transform = None, name = 'FrControl', suffix = 'Ctl', group = None):
    """Create control curve for FrMaya rig.

    :arg control_file: Control file absolute path or control file name.
    :type control_file: path.Path or str
    :key transform: Sets transformation of the newly-created control. Default use world transform.
    :type transform: pm.dt.Matrix
    :key name: Sets the name of the newly-created control.
    :type name: str
    :key suffix: Add suffix to the name.
    :type suffix: str
    :key group: Sets group chain on newly-created control.
    :type group: list of str
    :return: ControlTuple(control = control_curve, group_data = group_dict_data)
    :rtype: (pm.nt.Transform, dict of pm.nt.Transform)
    """
    if transform is None:
        transform = pm.dt.Matrix()
    if group is None:
        group = ['Grp']
    # if control_file is file name of control grab it from get_control_files
    control_file_path = path.Path(control_file)
    if not control_file_path.exists():
        control_file_path = get_control_files(control_file)[0]
    # add suffix to name
    name += '_' + suffix
    # read control file
    control_data = util.read_json(control_file_path)
    # build control curve
    curve_control = general.build_curve(control_data)
    # rename control
    curve_control.rename(name)
    # retransform control
    curve_control.setMatrix(transform, worldSpace = True)
    # pgroup the control
    resgrp = {}
    input_grp = curve_control
    for o in group:
        resgrp[o] = general.pgroup([input_grp], re = suffix, suffix = o)[0]
        input_grp = resgrp[o]
        suffix = o
    # create control tuple class
    ControlTuple = collections.namedtuple('ControlTuple', 'control group_data')
    # create instance of control tuple and assign the value
    result = ControlTuple(control = curve_control, group_data = resgrp)

    return result


def reset_attributes(input_object, attr_name_list = None):
    """Reset all attributes visible in channel box or supplied attributes
    to their respective attributes default value.

    :arg input_object: PyNode object which attributes need to reset.
    :type input_object: pm.PyNode
    :param attr_name_list: Attributes name need to reset.
    :type attr_name_list: list of str
    :rtype: None
    """
    if attr_name_list is None:
        attr_name_list = []
    if len(attr_name_list) > 0:
        attr_list = [input_object.attr(attr_name) for attr_name in attr_name_list]
    else:
        attr_list = general.get_channelbox_attributes(input_object)

    for attr in attr_list:
        # def_val = attr.get(default = True)
        def_val = pm.attributeQuery(attr.plugAttr(), node = attr.node(), listDefault = True)[0]
        if attr.isSettable():
            attr.set(def_val)


def set_attrs_default(input_object):
    """Set current value attributes as the default value.
    Some default value attributes cannot be set.

    :arg input_object: PyNode object which attributes need to set default value.
    :type input_object: pm.PyNode
    :rtype: None
    """
    attr_list = general.get_channelbox_attributes(input_object)
    for attr in attr_list:
        current_val = attr.get()
        if hasattr(attr, 'addAttr'):
            attr.addAttr(e = True, defaultValue = current_val)




