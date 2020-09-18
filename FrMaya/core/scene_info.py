"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 14 Sep 2020
Info         :

"""
import re

import pymel.core as pm
import maya.cmds as mc


def get_duplicate_name():
    """Collect duplicated name in the scene.

    :rtype: list of pm.PyNode
    """
    return [o for o in pm.ls(dag = True, editable = True) if '|' in o and not o.isInstanced()]


def get_pasted_node():
    """Collect pasted node in the scene.

    :rtype: list of pm.PyNode
    """
    return [o for o in pm.ls('pasted__*', editable = True)]


def get_zero_scale(tolerance = 0.001):
    """Collect all object that have zero scale.

    :key tolerance: Zero scale tolerance
    :type tolerance: float
    :rtype: list of pm.nt.Transform
    """
    result = []
    for scl_attr in mc.ls(['*.scaleX', '*.scaleY', '*.scaleZ']):
        val = mc.getAttr(scl_attr)
        if val < tolerance:
            result.append(pm.PyNode(scl_attr).node())
        # if '{:.3f}'.format(mc.getAttr(scl_attr)) == '0.000':
    result = pm.ls(result, editable = True)

    return result


def get_references():
    """Collect all reference in the scene.

    :rtype: list of pm.nt.Reference
    """
    # exclude reference list
    exclude_list = ['sharedReferenceNode']
    # get all editable reference available
    reference_list = pm.ls(type = 'reference', editable = True)
    return [o for o in reference_list if o.name() not in exclude_list]


def get_namespaces(exclude_ref = False):
    """Collect all namespaces in the scene (recursive from root to all child).

    :key exclude_ref: Exclude reference object or not.
    :type exclude_ref: bool
    :rtype: list of unicode
    """
    # exclude namespace list
    exclude_list = ['UI', 'shared']
    # get all namespace available
    namespace_list = pm.namespaceInfo(listOnlyNamespaces = True, recurse = True, shortName = True)
    # filter reference namespace, pm.ls(editable = True) will not work
    if exclude_ref:
        ref_list = get_references()
        exclude_list += [o.referenceFile().namespace for o in ref_list]
    return [o for o in namespace_list if o not in exclude_list]


def get_scene_fps():
    """Get current scene fps as float.

    :rtype: float
    """
    fps_dict = {
        'game': 15.0,
        'film': 24.0,
        'pal': 25.0,
        'ntsc': 30.0,
        'show': 48.0,
        'palf': 50.0,
        'ntscf': 60.0
    }
    non_fps_list = ['hour', 'min', 'sec', 'millisec']

    fps_unicode = pm.currentUnit(q = True, time = True)
    fps_float = fps_dict.get(fps_unicode, None)

    if fps_unicode in non_fps_list:
        return 0.0
    if fps_float is None:
        return float(fps_unicode.replace('fps', ''))
    return fps_float


def get_scene_unit():
    """Get current scene unit of measurement.

    :rtype: unicode
    """
    return pm.currentUnit(q = True, fullName = True, linear = True)


def get_scene_modified():
    """Return True if scene has been modified.

     :rtype: bool
     """
    return mc.file(q = True, modified = True)


def get_bad_shape_name():
    """Collect all bad shape name in the scene.
    Shape name -> transform.name + Shape or ShapeDeformed.

    :rtype: list of pm.nt.Shape
    """
    bad_shape_name = []
    for shape in pm.ls(shapes = True, noIntermediate = True, editable = True):
        transform = shape.getParent()
        tm_name = transform.nodeName(stripNamespace = True)
        shape_name = shape.nodeName(stripNamespace = True)
        regex = r"({0})(ShapeDeformed|Shape)".format(tm_name)
        m = re.match(regex, shape_name)
        if not m:
            bad_shape_name.append(shape)

    return bad_shape_name


def get_empty_mesh():
    """Get empty mesh in current scene.

    :rtype: list of pm.nt.Mesh
    """
    all_mesh = pm.ls(type = 'mesh', editable = True)
    return [o for o in all_mesh if not pm.polyEvaluate(o, face=True)]


def get_start_frame():
    """Get current scene start frame.

    :rtype: float
    """
    return pm.playbackOptions(animationStartTime = True, query = True)


def get_end_frame():
    """Get current scene end frame.

    :rtype: float
    """
    return pm.playbackOptions(animationEndTime = True, query = True)



