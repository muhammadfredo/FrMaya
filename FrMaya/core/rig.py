"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 13 Sep 2020
Info         :

"""
import collections

import pymel.core as pm
from FrMaya.vendor import path

from FrMaya import utility as util
from . import system, general, transformation


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

    Result key :
      - joint_list,
      - skin_method,
      - use_max_inf,
      - max_inf_count

    :arg skin_node: Skincluster PyNode that need to get info extracted.
    :type skin_node: pm.nt.SkinCluster
    :return: Skincluster joint influence, Skin method index, Use max influence, Max influence count.
    :rtype: dict
    """
    output = {
        'joint_list': [],
        'skin_method': 0,
        'use_max_inf': False,
        'max_inf_count': 4,
    }

    if skin_node:
        output['joint_list'] = skin_node.getInfluence()
        output['skin_method'] = skin_node.getSkinMethod()
        output['use_max_inf'] = skin_node.getObeyMaxInfluences()
        output['max_inf_count'] = skin_node.getMaximumInfluences()

    return output


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


def prune_skincluster(skin_node, prune_value = 0.01):
    """Prune small weight influences on skincluster.

    :arg skin_node: PyNode skincluster need to prune.
    :type skin_node: pm.nt.SkinCluster
    :key prune_value: Determine small weight value to prune.
    :type prune_value: float
    :rtype: None
    """
    pm.skinPercent(skin_node, pruneWeights = prune_value)


def transfer_skincluster(source_object, target_objects, prune_after = False):
    """Bind the target objects based on source object,
    then copied the skin data from source to target objects.
    If target object have skincluster,
    it will get replaced by new skincluster.

    :arg source_object: PyNode object transfer source.
    :type source_object: pm.PyNode
    :arg target_objects: PyNode objects transfer destination.
    :type target_objects: list of pm.PyNode
    :key prune_after: Do prune operation after transfer skincluster or not.
    :type prune_after: bool
    :rtype: None
    """
    source_skin_node = get_skincluster_node(source_object)
    assert source_skin_node, 'Skincluster not found in source object.'
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

        if prune_after:
            prune_skincluster(tgt_skin_node)


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
        control_files = [o for o in control_files if o.stem == name]

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
        group = []
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
    :key attr_name_list: Attributes name need to reset.
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


def set_attrs_default(input_object, attr_name_list = None):
    """Set current value attributes as the default value.
    Some default value attributes cannot be set.

    :arg input_object: PyNode object which attributes need to set default value.
    :type input_object: pm.PyNode
    :key attr_name_list: Attributes name need to be set default.
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
        current_val = attr.get()
        if hasattr(attr, 'addAttr'):
            attr.addAttr(e = True, defaultValue = current_val)


def split_joint(pynode, split = 2, replace = True):
    """Split joint into pieces as per split key argument.

    :arg pynode: A single joint PyNode.
    :type pynode: pm.nt.Joint
    :arg split: How many pieces the joint will be split.
    :type split: int
    :arg replace: Remove old joint (specified joint) or keep it.
    :type replace: bool
    :return: All new joint pieces.
    :rtype: list of pm.nt.Joint
    """
    output = []
    # make sure this is joint
    if not isinstance(pynode, pm.nt.Joint):
        return output
    if len(pynode.getChildren(type = 'joint')) > 0 and split > 1:
        # get first child
        children = pynode.getChildren(type = 'joint')
        if children:
            children = children[0]
        # get vector
        vec_a = pynode.getTranslation(space = 'world')
        vec_b = children.getTranslation(space = 'world')

        parent = pynode
        if not replace:
            parent = pm.createNode('joint')
            transformation.align(parent, pynode)
            output.append(parent)

        factor = (vec_b - vec_a) / split
        for i in range(1, split):
            jnt = pm.createNode('joint')
            pos = factor * i + vec_a

            # set split joint translate
            jnt.setTranslation(pos, space = 'world')
            # set split joint rotation
            transformation.align(jnt, pynode, mode = 'rotate')

            # set parent split joint
            jnt.setParent(parent)
            # clean transformation on joint
            transformation.freeze_transform(jnt)

            # append newly created split joint to output
            output.append(jnt)
            # set new variable parent
            parent = jnt

        if replace:
            children.setParent(parent)
        else:
            jnt = pm.createNode('joint')
            transformation.align(jnt, children)
            jnt.setParent(parent)
            output.append(jnt)

    return output


def comet_joint_orient(pynodes, aim_axis = None, up_axis = None, up_dir = None, do_auto = False):
    """Complete Joint Orient function for properly setting up joint axis.
    Translated from cometJointOrient.mel.

    Based on code by Michael B. Comet - comet@comet-cartoons.com

    http://www.comet-cartoons.com

    :arg pynodes: Pynodes joint need to orient.
    :type pynodes: list of pm.PyNode
    :key aim_axis: Joint aim axis in xyz list or Vector. Default aim to x axis > pm.dt.Vector(1, 0, 0).
    :type aim_axis: list or pm.dt.Vector
    :key up_axis: Joint up axis in xyz list or Vector. Default up to z axis > pm.dt.Vector(0, 0, 1).
    :type up_axis: list or pm.dt.Vector
    :key up_dir: Joint up direction in xyz list or Vector. Default up direction to x > pm.dt.Vector(1, 0, 0).
    :type up_dir: list or pm.dt.Vector
    :key do_auto: If possible will try to guess the up axis otherwise
     it will use prev joint up axis or else world up dir.
    :type do_auto: bool
    :rtype: bool
    """
    if aim_axis is None:
        aim_axis = [1, 0, 0]
    if up_axis is None:
        up_axis = [0, 0, 1]
    if up_dir is None:
        up_dir = [1, 0, 0]
    # convert to Vector
    aim_axis = pm.dt.Vector(aim_axis)
    up_axis = pm.dt.Vector(up_axis)
    up_dir = pm.dt.Vector(up_dir)
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # make sure only joint get passed through here
    pynodes = pm.ls(pynodes, type = 'joint')

    # init variable prevUp for later use
    prev_up = pm.dt.Vector()

    for i, o in enumerate(pynodes):
        parent_point = None
        # first we need to unparent everything and then store that,
        children = o.getChildren()
        for x in children:
            x.setParent(None)

        # find parent for later in case we need it
        parent = o.getParent()

        # Now if we have a child joint... aim to that
        aim_tgt = None
        for child in children:
            if child.nodeType() == 'joint':
                aim_tgt = child
                break

        if aim_tgt:
            # init variable upVec using upDir variable
            up_vec = pm.dt.Vector(up_dir)

            # first off... if doAuto is on, we need to guess the cross axis dir
            if do_auto:
                # now since the first joint we want to match the second orientation
                # we kind of hack the things passed in if it is the first joint
                # ie: if the joint doesnt have a parent... or if the parent it has
                # has the 'same' position as itself... then we use the 'next' joints
                # as the up cross calculations
                jnt_point = o.getRotatePivot(space = 'world')
                if parent:
                    parent_point.setValue(parent.getRotatePivot(space = 'world'))
                else:
                    parent_point = jnt_point.copy()
                aim_tgt_point = aim_tgt.getRotatePivot(space = 'world')

                # how close to we consider 'same'?
                tol = 0.0001

                point_cond = jnt_point - parent_point
                pos_cond = [abs(x) for x in point_cond.tolist()]
                if not parent or pos_cond[0] <= tol and pos_cond[1] <= tol and pos_cond[2] <= tol:
                    # get aimChild
                    aim_child = None
                    aim_children = aim_tgt.getChildren(type = 'joint')
                    if aim_children:
                        aim_child = aim_children[0]

                    # get aimChild vector
                    if aim_child:
                        aim_child_point = aim_child.getRotatePivot(space = 'world')
                    else:
                        aim_child_point = pm.dt.Vector()

                    # find the up vector using child vector of aim target
                    up_vec = (jnt_point - aim_tgt_point).cross(aim_child_point - aim_tgt_point)
                else:
                    # find the up vector using the parent vector
                    up_vec = (parent_point - jnt_point).cross(aim_tgt_point - jnt_point)

            # reorient the current joint
            a_cons = pm.aimConstraint(
                aim_tgt, o, aimVector = aim_axis, upVector = up_axis, worldUpVector = up_vec.tolist(),
                worldUpType = 'vector', weight = 1
            )
            pm.delete(a_cons)

            # now compare the up we used to the prev one
            current_up = up_vec.normal()
            # dot product for angle between... store for later
            dot = current_up.dot(prev_up)
            prev_up = up_vec

            if i > 0 >= dot:
                # adjust the rotation axis 180 if it looks like we have flopped the wrong way!
                # FIXME: some shit need to fix here
                # pm.xform( o, relative = True, objectSpace = True, rotateAxis = True )
                o.rotateX.set(o.rotateX.get() + (aim_axis.x * 180))
                o.rotateY.set(o.rotateY.get() + (aim_axis.y * 180))
                o.rotateZ.set(o.rotateZ.get() + (aim_axis.z * 180))

                prev_up *= -1
        elif parent:
            # otherwise if there is no target, just dup orientation of parent...
            transformation.align(o, parent, mode = 'rotate')

        # and now finish clearing out joint axis ...
        pm.joint(o, e = True, zeroScaleOrient = True)
        transformation.freeze_transform(o)

        # now that we are done ... reparent
        if len(children) > 0:
            for x in children:
                x.setParent(o)

    return True


def _create_follicle(source_object, vector_position = None, uv_position = None):
    """Create follicle based on closest vector position or uv position,
    if both empty then use default uv position which is [0.5, 0.5].

    :arg source_object: PyNode object that follicle will be attach to.
    :type source_object: pm.PyNode
    :key vector_position: Vector position (nearest) follicle will be pinned.
    :type vector_position: pm.dt.Vector
    :key uv_position: UV position [U, V] follicle will be pinned.
    :type uv_position: list of float
    :return: Follicle transform node.
    :rtype: pm.PyNode
    """
    shape_deform = source_object.getShape()
    if not shape_deform:
        return None
    node_type = shape_deform.nodeType()
    source_type_dict = {
        'mesh': {
            'closest_point': 'closestPointOnMesh',
            'output_deform': 'outMesh',
            'output_matrix': 'worldMatrix',
            'input_closest': 'inMesh',
            'input_follicle': 'inputMesh'
        },
        'nurbsSurface': {
            'closest_point': 'closestPointOnSurface',
            'output_deform': 'worldSpace',
            'output_matrix': 'matrix',
            'input_closest': 'inputSurface',
            'input_follicle': 'inputSurface'
        }
    }
    source_dict = source_type_dict[node_type]

    if vector_position is None and uv_position is None:
        uv_position = [0.5, 0.5]
    elif vector_position:
        cls_point_node = pm.createNode(source_dict['closest_point'])

        out_deform_attr = shape_deform.attr(source_dict['output_deform'])
        in_closest_attr = cls_point_node.attr(source_dict['input_closest'])
        out_deform_attr.connect(in_closest_attr)

        cls_point_node.inPositionX.set(vector_position.x)
        cls_point_node.inPositionY.set(vector_position.y)
        cls_point_node.inPositionZ.set(vector_position.z)

        u_value = cls_point_node.result.parameterU.get()
        v_value = cls_point_node.result.parameterV.get()
        uv_position = [u_value, v_value]

        pm.delete(cls_point_node)

    follicle_shp = pm.createNode('follicle')
    follicle_tm = follicle_shp.getParent()
    follicle_shp.outRotate.connect(follicle_tm.rotate)
    follicle_shp.outTranslate.connect(follicle_tm.translate)

    shape_deform.attr(source_dict['output_matrix']).connect(follicle_shp.inputWorldMatrix)
    shape_deform.attr(source_dict['output_deform']).connect(follicle_shp.attr(source_dict['input_follicle']))

    follicle_shp.simulationMethod.set(0)
    follicle_shp.parameterU.set(uv_position[0])
    follicle_shp.parameterV.set(uv_position[1])

    return follicle_tm


def create_follicle_object_position(source_object, target_objects):
    """Create follicle using object position to determine its location.

    :arg source_object: PyNode object that follicle will be attach to.
    :type source_object: pm.PyNode
    :param target_objects: PyNode object that will determine follicle location.
    :type target_objects: list of pm.PyNode
    :return: Follicles transform node.
    :rtype: list of pm.PyNode
    """
    results = []
    for each_target in target_objects:
        vec_pos = each_target.getTranslation(space = 'world')
        follicle_tm = _create_follicle(source_object, vector_position = vec_pos)
        if follicle_tm:
            results.append(follicle_tm)
    return results


def create_follicle_uv(source_object, u_pos, v_pos):
    """Create follicle using uv coordinates to determine its location.

    :arg source_object: PyNode object that follicle will be attach to.
    :type source_object: pm.PyNode
    :arg u_pos: U coordinate in UV space.
    :type u_pos: float
    :arg v_pos: V coordinate in UV space.
    :type v_pos: float
    :return: Follicle transform node.
    :rtype: pm.PyNode
    """
    result = _create_follicle(source_object, uv_position = [u_pos, v_pos])
    return result


def create_soft_cluster():
    """Create cluster from current soft selection.
    Code based on https://gist.github.com/jhoolmans/9195634, modify to use pymel and new Maya api."""
    # node, index_component, inf_val = general.get_soft_selection()
    soft_element_data = general.get_soft_selection()
    selection = [vtx_component for vtx_component, inf_val in soft_element_data]

    pm.select(selection, r=True)
    cluster = pm.cluster(relative=True)

    # for i in range(len(soft_element_data)):
    for vtx_component, inf_val in soft_element_data:
        pm.percent(cluster[0], vtx_component, v=inf_val)
    pm.select(cluster[1], r=True)

