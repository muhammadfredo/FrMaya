"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jul 2017
Purpose      :

"""
import copy
import collections

import pymel.core as pm
from FrMaya.vendor import path

import FrMaya.utility as util


def pgroup(pynodes, world = False, re = "", suffix = ""):
    """
    Create pgroup on supplied pynode

    :param pynodes: List of pynode
    :param world: Position of group in world pos or object pos, True or False value
    :param re: Find and replace input pynode name
    :param suffix: Suffix to add to pynode name
    """

    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # Initiate return variable
    output = []

    # Group created on each object transformation
    if not world:
        for o in pynodes:
            # Name var
            the_name = o.name()

            # Replace object name if any
            if re != "":
                the_name = the_name.replace(re, suffix)
            else:
                the_name = the_name + suffix

            # Create group for each supplied object
            grp = pm.group(empty = True, name = the_name)

            # Snap the group to each object transformation
            alignMath(grp, o, mode = 'transform')

            # Get object parent
            parent = o.getParent()

            # If the object have parent,
            # Parent the group to object parent 
            if parent:
                grp.setParent(parent)

            # Parent the object to Group
            o.setParent(grp)
            # Collect group to output
            output.append(grp)

    else:
        # Name var
        the_name = pynodes[0].name()

        # Replace object name if any
        if re != "":
            the_name = the_name.replace(re, suffix)
        else:
            the_name = the_name + suffix

        # Create single group
        grp = pm.group(empty = True, name = the_name)

        # Collect group to output
        output.append(grp)

        # Loop through all supplied object and parent it to group
        for o in pynodes:
            o.setParent(grp)

    return output


def align(orig, target, mode = 'transform'):
    """
    Align from orig pynode to target pynode using contraint method

    :param orig: source of transform
    :param target: target gonna get transformed
    :param mode: transform, translate, rotate
    """

    # Snap position
    if mode == 'translate' or mode == 'transform':
        # Snap position of orig node to target node using constraint
        cons = pm.pointConstraint(target, orig, maintainOffset = False)
        # Delete the constraint
        pm.delete(cons)

    # Snap rotation
    if mode == 'rotate' or mode == 'transform':
        # Snap rotation of orig node to target node using constraint
        cons = pm.orientConstraint(target, orig, maintainOffset = False)
        # Delete the constraint
        pm.delete(cons)


def freezeTransform(pynodes, mode = 'transform'):
    """
    Freeze transform, translate, rotate, scale all supplied pynode
    depend on the mode

    :param pynodes: List of pynode
    :param mode: transform, translate, rotate, scale
    """

    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # Initiate variable for makeIdentity command
    t = False
    r = False
    s = False

    # Translate mode
    if mode == 'translate' or mode == 'transform':
        t = True
    # Rotate mode
    if mode == 'rotate' or mode == 'transform':
        r = True
    # Scale mode
    if mode == 'scale' or mode == 'transform':
        s = True

    # Freeze transform command
    for o in pynodes:
        pm.makeIdentity(o, apply = True, translate = t, rotate = r, scale = s)


def zerooutTransform(pynodes, mode = 'transform'):
    """
    Zero out transform, visibility, and rotate order

    :param pynodes: list of pynode
    :param mode: transform, translate, rotate, scale, visibility, rotateorder
    """

    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    for o in pynodes:
        # Translate mode
        if mode == 'translate' or mode == 'transform':
            o.translateX.set(0)
            o.translateY.set(0)
            o.translateZ.set(0)
        # Rotate mode
        if mode == 'rotate' or mode == 'transform':
            o.rotateX.set(0)
            o.rotateY.set(0)
            o.rotateZ.set(0)
        # Scale mode
        if mode == 'scale' or mode == 'transform':
            o.scaleX.set(1)
            o.scaleY.set(1)
            o.scaleZ.set(1)
        # Visibility
        if mode == 'visibility':
            o.visibility.set(1)
        # Rotate order
        if mode == 'rotateorder':
            o.rotateOrder.set(0)


def keylockhideAttribute(pynodes, attributes_string, keyable = None, lock = None, hide = None):
    """
    Make attribute keyable or not, lock or unlock, and hide or unhide

    :param pynodes: list of pynode
    :param attributes_string: List of attribute as string, ex => [ 'translateX', 'scaleZ' ]
    :param keyable: None = Ignore; True or False
    :param lock: None = Ignore; True or False
    :param hide: None = Ignore; True or False
    """

    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # TODO: change this to more 'PyNode' way
    # Loop through list of attribute string
    for o in attributes_string:
        # Loop through list of pynode
        for x in pynodes:
            # Set attribute as PyNode object 
            att_node = pm.PyNode('{0}.{1}'.format(x.nodeName(), o))

            # Keyable or non keyable operation
            if keyable is not None:
                att_node.setKeyable(keyable)

                # Make sure attribute still showed in channelbox
                if not keyable:
                    att_node.showInChannelBox(True)

            # Lock or unlock operation
            if lock is not None:
                att_node.setLocked(lock)

            # Hide or unhide operation
            if hide is not None:
                # Attribute still showed in channelbox if it still keyable
                if hide:
                    att_node.setKeyable(False)
                    att_node.showInChannelBox(False)
                # Set keyable to true will show the attribute in channelbox
                elif not hide:
                    att_node.setKeyable(True)


def alignMath(source, target, mode = 'transform'):
    """
    Align from orig pynode to target pynode using math element ( matrix, quaternion, vector, etc)

    :param source: PyNode which will get transform applied
    :param target: The destination of alignMath operation
    :param mode: transform, translate, rotate
    """

    # I got this align translate and some rotation algorithm
    # from Red9 SnapRuntime plugin

    # Align translate
    if mode == 'translate' or mode == 'transform':
        if type(target) == pm.MeshVertex:
            target_trans = target.getPosition(space = 'world')
        else:
            rot_piv_a = target.getRotatePivot(space = 'world')
            rot_piv_b = source.getRotatePivot(space = 'world')
            orig_trans = source.getTranslation(space = 'world')
            # We subtract the destinations translation from it's rotPivot, before adding it
            # to the source rotPiv. This compensates for offsets in the 2 nodes pivots
            target_trans = rot_piv_a + (orig_trans - rot_piv_b)

        # Translate align operation
        source.setTranslation(target_trans, space = 'world')

    # Align rotation
    if mode == 'rotate' or mode == 'transform':
        # Get rotation as quaternion
        rot_qt = target.getRotation(space = 'world', quaternion = True)
        source.setRotation(rot_qt, space = 'world')

        # Maybe we should use MyMatrix object in the future for the sake of math XD
        # pm.xform(orig, ro = rot_qt.toEulerian().asList(), eu = True, ws = True)


def jointSplit(pynode, split = 2, replace = True):
    """
    Split joint from given parameter

    :param pynode: A single joint PyNode
    :param split: Number, how many split the joint will be split
    :param replace: Bool value, new chain of split joint or replace the input joint
    :return: list of split joint
    """

    # TODO: naming not yet implement, wait until we build modular auto rigging
    # init output data
    output = []
    # check if there is any selection, and store it
    sel = pm.ls(os = True)
    # make sure this is joint
    if pynode.type() == 'joint' and len(pynode.getChildren()) > 0 and split > 1:
        # clear selection
        pm.select(clear = True)
        # get first child
        first_child = pynode.getChildren()[0]
        # get vector
        vec_a = pynode.getTranslation(space = 'world')
        vec_b = first_child.getTranslation(space = 'world')

        parent = pynode
        if not replace:
            jnt = pm.createNode('joint')
            alignMath(jnt, pynode)
            parent = jnt
            output.append(parent)

        factor = (vec_b - vec_a) / split
        for i in range(split - 1):
            jnt = pm.createNode('joint')
            pos = factor * (i + 1) + vec_a

            # set splited joint translate
            jnt.setTranslation(pos.asList())
            # set splited joint rotation
            alignMath(jnt, pynode, mode = 'rotate')

            # set parent splited joint
            jnt.setParent(parent)
            # clean transformation on joint
            freezeTransform([jnt])

            # append newly created split joint to output
            output.append(jnt)
            # set new variable parent
            parent = jnt

        if not replace:
            jnt = pm.createNode('joint')
            alignMath(jnt, first_child)
            jnt.setParent(parent)
            output.append(jnt)
        else:
            first_child.setParent(parent)

        # reselect selection if any
        pm.select(sel)

    return output


def cometJoint_orient(pynodes, aim_axis = [1, 0, 0], up_axis = [0, 0, 1], up_dir = [1, 0, 0], do_auto = False):
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # make sure only joint get passed through here
    pynodes = pm.ls(pynodes, type = 'joint')

    # init variable prevUp for later use
    prev_up = pm.dt.Vector()

    for i, o in enumerate(pynodes):
        parent_point = None
        # first we need to unparent everthing and then store that,
        children = o.getChildren()
        for x in children:
            x.setParent(None)

        # find parent for later in case we need it
        parent = o.getParent()

        # Now if we have a child joint... aim to that
        try:
            aim_tgt = pm.ls(children, type = 'joint')[0]
        except:
            aim_tgt = None

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
                    aim_children = aim_tgt.getChildren()
                    try:
                        aim_child = pm.ls(aim_children, type = 'joint')[0]
                    except:
                        aim_child = None

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
                # TODO: fix here
                # pm.xform( o, relative = True, objectSpace = True, rotateAxis = True )
                o.rotateX.set(o.rotateX.get() + (aim_axis[0] * 180))
                o.rotateY.set(o.rotateY.get() + (aim_axis[1] * 180))
                o.rotateZ.set(o.rotateZ.get() + (aim_axis[2] * 180))

                prev_up *= -1
        elif parent:
            # otherwise if there is no target, just dup orientation of parent...
            alignMath(o, parent, mode = 'rotate')

        # and now finish clearing out joint axis ...
        pm.joint(o, e = True, zeroScaleOrient = True)
        freezeTransform([o])

        # now that we are done ... reparent
        if len(children) > 0:
            for x in children:
                x.setParent(o)

    return True


# return list of controller, and other data to use
def getControlFiles(name = ''):
    """
    Get available control on control folder

    :return: list of all control file in PathNode object
    """

    # get FrRigging folder PathNode
    fr_rigging_folder = path.Path(__file__).parent
    # get control folder PathNode
    control_folder = fr_rigging_folder / 'control'

    control_files = control_folder.glob('*.json')
    if name:
        control_files = [o for o in control_files if o.filename == name]

    # return list of .mel file PathNode
    return control_files


def buildCurve(data):
    curve = None
    for key, value in data.iteritems():
        degree = value.get('degree')
        periodic = value.get('periodic')
        point = value.get('point')
        knot = value.get('knot')

        # convert list to tupple
        point = [(o[0], o[1], o[2]) for o in point]

        curve = pm.curve(d = degree, per = periodic, p = point, k = knot)
    return curve


# att plan for below function, type of control, name, transform, color, group count
def createControl(filenode, transform = None, name = '', suffix = 'Ctl', color = None, group = ['Grp']):
    # check function attribute, and modify it if its on default mode
    # fill fullpath variable from filenode,
    # if filenode is name of control grab it from getControl
    controlpath = path.Path(filenode)
    if not controlpath.exists():
        controlpath = getControlFiles(filenode)[0]
    # modify if name att on default
    if not name:
        name = 'FrControl'
    # add suffix to name
    name += '_' + suffix
    # modify if transform is None
    if not transform:
        transform = pm.dt.Matrix()

    control_data = util.read_json(controlpath)
    # import control
    curve_control = buildCurve(control_data)
    # grab transform of imported control
    # ctl = pm.ls(impNodes, type = 'transform')[0]

    # rename control
    curve_control.rename(name)
    # retransform control
    curve_control.setMatrix(transform, worldSpace = True)
    # pgroup the control
    resgrp = {}
    input_grp = curve_control
    for o in group:
        resgrp[o] = pgroup([input_grp], re = suffix, suffix = o)[0]
        input_grp = resgrp[o]
        suffix = o

    # create control tuple class
    ControlTuple = collections.namedtuple('ControlTuple', 'control groupDict')
    # create instance of control tuple and assign the value
    result = ControlTuple(control = curve_control, groupDict = resgrp)

    return result
