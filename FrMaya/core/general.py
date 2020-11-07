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

    :arg pynodes: Specified pynodes object need to be pgroup.
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


def transfer_shape(source_object, target_objects, replace = True):
    """Copied source shape object into target object,
    Default it will replace target shape objects.

    :arg source_object: PyNode object transfer shape source.
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


def _do_attributes_key_lock_hide(pynode, attr_name_list, keyable = None, lock = None, hide = None):
    """Make attribute keyable or nonkeyable, lock or unlock, and hide or unhide.

    :arg pynode: PyNode need to key, lock, or hide operation.
    :type pynode: pm.PyNode
    :arg attr_name_list: Attribute name need to key, lock, or hide operation.
    :type attr_name_list: list of str
    :key keyable: True to make attribute keyable, False to make non keyable.
    :type keyable: bool or None
    :key lock: True to lock attribute, False to unlock attribute.
    :type lock: bool or None
    :key hide: True to hide attribute, False to unhide attribute.
    :type hide: bool or None
    """
    # Loop through list of attribute name
    for attribute_name in attr_name_list:
        # get attribute node
        if not pynode.hasAttr(attribute_name):
            continue
        att_node = pynode.attr(attribute_name)

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


def lock_attributes(pynode, attr_name_list = None):
    """Lock specified attributes of given PyNode.
    By default will lock all translate, rotate, scale, and visibility.

    :arg pynode: PyNode which attribute need to lock.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to lock.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, lock = True)


def unlock_attributes(pynode, attr_name_list = None):
    """Unlock specified attributes of given PyNode.
    By default will unlock all translate, rotate, scale, and visibility.

    :arg pynode: PyNode which attribute need to unlock.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to unlock.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, lock = False)


def hide_attributes(pynode, attr_name_list = None):
    """Hide specified attributes of given PyNode.
    By default will hide all translate, rotate, scale, and visibility.

    :arg pynode: PyNode which attribute need to hide.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to hide.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, hide = True)


def unhide_attributes(pynode, attr_name_list = None):
    """Unhide specified attributes of given PyNode.
    By default will unhide all translate, rotate, scale, and visibility.

    :arg pynode: PyNode which attribute need to unhide.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to unhide.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, hide = False)


def keyable_attributes(pynode, attr_name_list = None):
    """Make specified attributes of given PyNode keyable.
    By default will make all translate, rotate, scale, and visibility into keyable.

    :arg pynode: PyNode which attribute will be keyable.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to be keyable.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, keyable = True)


def nonkeyable_attributes(pynode, attr_name_list = None):
    """Make specified attributes of given PyNode non keyable.
    By default will make all translate, rotate, scale, and visibility into non keyable.

    :arg pynode: PyNode which attribute will be non keyable.
    :type pynode: pm.PyNode
    :key attr_name_list: Attributes name need to be non keyable.
    :type attr_name_list: list of str
    """
    if attr_name_list is None:
        attr_name_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']

    _do_attributes_key_lock_hide(pynode, attr_name_list, keyable = False)


def get_channelbox_attributes(input_object):
    """Collect all visible attributes in channelbox.

    :arg input_object: PyNode object need to collect attributes from.
    :type input_object: pm.PyNode
    :rtype: list of pm.general.Attribute
    """
    attr_list = input_object.listAttr(keyable = True, scalar = True, multi = True)
    attr_list.extend(input_object.listAttr(channelBox = True))
    return attr_list


def duplicate_original_mesh(source_object, default_shader = True):
    """Duplicate object without any deformer input.

    :arg source_object: PyNode object needs to be duplicated.
    :type source_object: pm.PyNode
    :key default_shader: Assign initialShadingGroup to duplicated object or not, default is True.
    :type default_shader: bool
    :return: Duplicated object, None if source object doesnt have shapes.
    :rtype: pm.PyNode or None
    """
    if not source_object.getShapes():
        return
    shapes_list = pm.ls(source_object.getShapes(), intermediateObjects = True)
    shape_orig = None
    for shape in shapes_list:
        if not shape.inMesh.isDestination() and (shape.outMesh.isSource() or shape.worldMesh[0].isSource()):
            shape_orig = shape
    if not shape_orig:
        return
    duplicate_name = '{}_new'.format(shape_orig.getParent().nodeName(stripNamespace = True))
    duplicated_object = pm.createNode('mesh', skipSelect = True)
    # rename its transform node
    duplicated_object.getParent().rename(duplicate_name)
    # copy the mesh data
    shape_orig.outMesh.connect(duplicated_object.inMesh)
    # done copying, break the connection
    pm.evalDeferred(duplicated_object.inMesh.disconnect)

    if default_shader:
        pm.sets('initialShadingGroup', edit = True, forceElement = duplicated_object.getParent())

    return duplicated_object


