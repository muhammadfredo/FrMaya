"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 11 Sep 2020
Info         :

"""
from typing import List, Optional, Tuple, Type, Union

import pymel.core as pm

from . import transformation


def pgroup(pynodes, world = False, re = "", suffix = ""):
    """
    Create pgroup on supplied pynode
    # TODO: fix docstring

    :arg pynodes: List of pynode
    :type pynodes: list of pm.PyNode
    :arg world: Position of group in world pos or object pos
    :type world: bool
    :arg re: Find and replace input pynode name
    :type re: str
    :arg suffix: Suffix to add to pynode name
    :type suffix: str
    :return: list of pgroup node
    :rtype: pm.nt.Transform
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

            # Create group for each supplied object
            grp = pm.group(empty = True, name = the_name)

            # Snap the group to each object transformation
            transformation.align(grp, o, mode = 'transform')

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


def joint_split(pynode, split = 2, replace = True):
    """
    Split joint from given parameter
    # TODO: fix docstring

    :arg pynode: A single joint PyNode
    :type pynode: pm.nt.Joint
    :arg split: How many split the joint will be split
    :type split: int
    :arg replace: New chain of split joint or replace the input joint
    :type replace: bool
    :return: list of split joint
    :rtype: list of pm.nt.Joint
    """
    # TODO: naming not yet implement, wait until we build modular auto rigging
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


def comet_joint_orient(pynodes, aim_axis = None, up_axis = None, up_dir = None, do_auto = False):
    """
    # TODO: fix docstring

    :arg pynodes:
    :arg aim_axis:
    :arg up_axis:
    :arg up_dir:
    :arg do_auto:
    :return:
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
                # TODO: fix here
                # pm.xform( o, relative = True, objectSpace = True, rotateAxis = True )
                o.rotateX.set(o.rotateX.get() + (aim_axis[0] * 180))
                o.rotateY.set(o.rotateY.get() + (aim_axis[1] * 180))
                o.rotateZ.set(o.rotateZ.get() + (aim_axis[2] * 180))

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





