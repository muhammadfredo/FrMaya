"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 11 Sep 2020
Info         :

"""
import pymel.core as pm

from . import transformation


def pgroup(pynodes, world = False, re = "", suffix = ""):
    """Pgroup the specified PyNodes,
    either per-PyNode or all PyNodes under the same pgroup.
    Pgroup name based on the specified PyNodes,
    then modified by 're' and 'suffix' key argument.

    :arg pynodes: Specified pynodes need to be pgrouped.
    :type pynodes: list of pm.PyNode
    :arg world: Align pgroup to world transform or align to per-PyNode transform.
    :type world: bool
    :arg re: String to search and then replace by suffix.
    :type re: str
    :arg suffix: Suffix for pgroup name.
    :type suffix: str
    :return: list of pgroup node.
    :rtype: list of pm.nt.Transform
    """
    # Initiate return variable
    output = []
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return output
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
            # Create group for each specified PyNode
            grp = pm.group(empty = True, name = the_name)
            # Align the pgroup to each PyNode transformation
            transformation.align(grp, o, mode = 'transform')
            # Get object parent
            parent = o.getParent()
            # If the object have parent,
            # Parent the group to object parent
            if parent:
                grp.setParent(parent)
            # Parent the object to pgroup
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
        # Parent all specified PyNodes to pgroup
        pm.parent(pynodes, grp)

    return output


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
    # FIXME: naming not yet implement, wait until we build modular auto rigging
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
            transformation.freeze_transform([jnt])

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


# Based on code by Michael B. Comet - comet@comet-cartoons.com
# http://www.comet-cartoons.com/
def comet_joint_orient(pynodes, aim_axis = None, up_axis = None, up_dir = None, do_auto = False):
    """Complete Joint Orient function for properly setting up joint axis.
    Translated from cometJointOrient.mel.

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
        transformation.freeze_transform([o])

        # now that we are done ... reparent
        if len(children) > 0:
            for x in children:
                x.setParent(o)

    return True


def build_curve(curve_data):
    """Build curve shape from dictionary curve data.

    :arg curve_data: Dictionary curve data.
     {'curve_shape_name': {
       'degree': int,
       'periodic': bool,
       'point': nested list,
       'knot': list of float
     } }
    :type curve_data: dict
    :return: Curve PyNode object.
    :rtype: pm.nt.Transform
    """
    result = []
    for key, value in curve_data.items():
        degree = value.get('degree')
        periodic = value.get('periodic')
        point = value.get('point')
        knot = value.get('knot')

        # convert list to tuple
        point = [tuple(o) for o in point]

        curve = pm.curve(d = degree, per = periodic, p = point, k = knot)
        result.append(curve)
    # FIXME: multi shape not supported
    return result[0]


def keylockhide_attribute(pynodes, attributes_string, keyable = None, lock = None, hide = None):
    """
    Make attribute keyable or not, lock or unlock, and hide or unhide
    # TODO: docstring here
    :param pynodes: list of pynode
    :param attributes_string: List of attribute as string, ex => [ 'translateX', 'scaleZ' ]
    :param keyable: None = Ignore; True or False
    :param lock: None = Ignore; True or False
    :param hide: None = Ignore; True or False
    """
    # TODO: can use map function, no need pynode list
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # FIXME: change this to more 'PyNode' way
    # Loop through list of attribute string
    for o in attributes_string:
        # Loop through list of pynode
        for x in pynodes:
            # Set attribute as PyNode object
            att_node = pm.PyNode('{0}.{1}'.format(x.nodeName(), o))

            # Keyable or non keyable operation
            if keyable is not None:
                att_node.setKeyable(keyable)

                # Make sure attribute still showed in channel box
                if not keyable:
                    att_node.showInChannelBox(True)

            # Lock or unlock operation
            if lock is not None:
                att_node.setLocked(lock)

            # Hide or unhide operation
            if hide is not None:
                # Attribute still showed in channel box if it still keyable
                if hide:
                    att_node.setKeyable(False)
                    att_node.showInChannelBox(False)
                # Set keyable to true will show the attribute in channel box
                elif not hide:
                    att_node.setKeyable(True)


def transfer_shape(source_object, target_objects, replace = True):
    """Copied source shape object into target object,
    Default it will replace target shape objects.

    :arg source_object: PyNode object shape transfer source.
    :type source_object: pm.nt.Transform
    :arg target_objects: PyNodes object transfer destination.
    :type target_objects: list of pm.nt.Transform
    :arg replace: Replace target shape or keep it.
    :type replace: bool
    :rtype: bool
    """
    if len(target_objects) == 0:
        return False
    shapes_list = []
    if source_object.type() == 'transform':
        shapes_list = source_object.getShapes(noIntermediate = True)
    if not shapes_list:
        return False

    for tgt in target_objects:
        if replace:
            pm.delete(tgt.getShapes(noIntermediate = True))
        for shp in shapes_list:
            new_shp = pm.duplicate(shp, addShape = True)[0]
            new_shp.setParent(tgt, relative = True, shape = True)
            new_shp.rename(tgt.nodeName(stripNamespace = True) + 'Shape')

    return True





