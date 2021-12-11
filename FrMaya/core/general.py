"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 11 Sep 2020
Info         :

"""
from collections import OrderedDict

import maya.api.OpenMaya as om
import pymel.core as pm
from FrMaya.vendor import path

from . import transformation, naming


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


def build_curve(curve_data, parent_curve = None, parent_type = 'transform'):
    """Build curve shape from dictionary curve data.

    :arg curve_data: Dictionary curve data.
     {'curve_shape_name': {
       'degree': int,
       'periodic': bool,
       'point': nested list,
       'knot': list of float
     } }
    :type curve_data: dict
    :key parent_curve: If supplied, the curve shape will be parented to it instead.
    :type parent_curve: pm.nt.Transform or pm.nt.Joint
    :key parent_type: Sets parent type of newly-created curve shape.
    :type parent_type: str
    :return: Curve PyNode object.
    :rtype: pm.nt.Transform or pm.nt.Joint
    """
    if parent_curve is None:
        parent_curve = pm.createNode(parent_type, name = naming.get_unique_name('fr_curve'))
    else:
        # clean shapes
        shapes = parent_curve.getShapes()
        pm.delete(shapes)

    for key, value in curve_data.items():
        new_curve = pm.curve(
            d = value.get('degree', 3),
            per = value.get('periodic', False),
            p = [tuple(o) for o in value.get('point', [[0, 0, 0]])],
            k = value.get('knot', [1.0, 0.0])
        )
        curve_shapes = new_curve.getShapes()
        pm.parent(curve_shapes, parent_curve, addObject = True, shape = True)
        pm.delete(new_curve)

        curve_color = value.get('color', 17)
        for each_crv in curve_shapes:
            # colorize curve
            color_attr = 'overrideColor'
            if isinstance(curve_color, list):
                each_crv.overrideRGBColors.set(True)
                color_attr = 'overrideColorRGB'
            each_crv.attr(color_attr).set(curve_color)
            each_crv.overrideEnabled.set(True)

            # rename each curve
            each_crv.rename('{0}Shape{1}'.format(parent_curve.nodeName(), key.replace('curve', '')))

    return parent_curve


def serialize_curve(pynode):
    """Serialize curve shape node into dictionary data.

    :arg pynode: Specified pynode object need to be serialized.
    :type pynode: pm.PyNode
    :rtype: dict
    """
    curves = pynode.getShapes()
    if not curves:
        return

    curve_data = OrderedDict()
    for i, each_crv in enumerate(curves):
        if each_crv.nodeType() != 'nurbsCurve':
            continue

        curve_name = 'curve{:02d}'.format(i)
        curve_data[curve_name] = OrderedDict()
        curve_data[curve_name]['degree'] = each_crv.degree()
        if each_crv.f.get() == 0:
            periodic = False
        else:
            periodic = True
        curve_data[curve_name]['periodic'] = periodic
        curve_data[curve_name]['point'] = [o.tolist() for o in each_crv.getCVs()]
        curve_data[curve_name]['knot'] = each_crv.getKnots()
        if each_crv.overrideRGBColors.get():
            color_val = list(each_crv.overrideColorRGB.get())
        else:
            color_val = each_crv.overrideColor.get()
        curve_data[curve_name]['color'] = color_val

    return curve_data


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
    # extend to include non keyable attribue
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


def get_soft_selection():
    """Return list of [vertex index, vertex soft selection influence].

    :rtype: list of list
    """
    soft_selection = om.MGlobal.getRichSelection(True)
    selection = soft_selection.getSelection()

    selection_iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
    elements = []
    while not selection_iter.isDone():
        dag_path, component = selection_iter.getComponent()
        node = pm.PyNode(dag_path.fullPathName())
        fn_component = om.MFnSingleIndexedComponent(component)
        for i in range(fn_component.getCompleteData()):
            index_component = fn_component.element(i)
            inf_val = fn_component.weight(i).influence

            elements.append([node.vtx[index_component], inf_val])
        selection_iter.next()
    return elements


def backup_file(file_path):
    """Backup supplied file into file.versions folder and add version number on their file name.

    :arg file_path: Source file (absolute path) which need to get backup.
    :type file_path: str or path.Path
    :return: Latest backup file (absolute path).
    :rtype: path.Path
    """
    file_path = path.Path(file_path)
    dir_path = file_path.parent
    file_name = file_path.stem
    file_ext = file_path.ext

    # backup directory
    backup_dir = dir_path / '{}.versions'.format(file_name)

    # detect if backup directory exist
    if not backup_dir.exists():
        backup_dir.makedirs()

    backup_file_glob = backup_dir.glob('{}.v*{}'.format(file_name, file_ext))
    version_count = 1
    if backup_file_glob:
        backup_file_glob.sort()
        latest_file = backup_file_glob[-1]
        version_count = int(latest_file.stem.replace('{}.v'.format(file_name), ''))
        version_count += 1

    # new version file
    backup_file_path = backup_dir / '{}.v{:03d}{}'.format(file_name, version_count, file_ext)

    # copy the file / backup the file
    file_path.copyfile(backup_file_path)
    return backup_file_path.abspath()


def create_surface_plane(axis = 'x', width = 0.5):
    """Create surface plane and return transform pynode of the surface plane.

    :key axis: Surface normal direction in 'x', 'y', 'z'. Default 'x'
    :type axis: str
    :key width: The width of the plane. Default: 0.5
    :type width: float
    :rtype: pm.nt.Transform
    """
    axis_dict = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
    res = pm.nurbsPlane(
        axis = axis_dict[axis],
        width = width,
        degree = 1,
        constructionHistory = False
    )[0]
    return res

