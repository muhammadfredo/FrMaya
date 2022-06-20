"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 14 Sep 2020
Info         :

"""
import copy
import re

import pymel.core as pm
import maya.cmds as mc
from pymel import core as pm

from FrMaya.core import naming


# region Get
def get_duplicate_name():
    """Collect duplicated name in the scene.

    :rtype: list of pm.PyNode
    """
    return [o for o in pm.ls(dag = True, editable = True) if '|' in o and not o.isInstanced()]


def get_pasted_node():
    """Collect pasted node in the scene.

    :rtype: list of pm.PyNode
    """
    # example to search pasted node inside hierarchy
    # regex = '\|All\|.*pasted__.*'
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
        exclude_list += [o.referenceFile().namespace for o in ref_list if o.referenceFile()]
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

        num_split = re.search(r'(.+?)(\d*)$', tm_name)
        name_split, number_split = num_split.groups()

        result_num = False
        regex_num = r"({0})(ShapeDeformed|Shape)({1})".format(name_split, number_split)
        if num_split:
            result_num = re.match(regex_num, shape_name)

        regex = r"({0})(ShapeDeformed|Shape)".format(tm_name)
        result = re.match(regex, shape_name)

        if not result and not result_num:
            bad_shape_name.append(shape)

    return bad_shape_name


def get_empty_mesh():
    """Collect empty mesh in current scene.

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


def get_shading_engine_intermediate():
    """Collect all intermediate shape
    that have connection with shading engine.

    :rtype: list of pm.nt.ShadingEngine
    """
    shape_inter_list = pm.ls(type = 'mesh', intermediateObjects = True)

    return [o for o in shape_inter_list if o.shadingGroups()]


def get_unfreeze_transform(translate = True, rotate = True, scale = True):
    """
    Collect all unfreeze transform objects except camera.

    :key translate: If True, enable check on translate attribute.
    :type translate: bool
    :key rotate: If True, enable check on rotation attribute.
    :type rotate: bool
    :key scale: If True, enable check on scale attribute.
    :type scale: bool
    :rtype: list of pm.nt.Transform
    """
    exclude_list = ['camera']
    result = []
    rst_list = pm.ls(type = 'transform')
    for each_rst in rst_list:
        shp = each_rst.getShape()
        if shp and type(shp).__name__.lower() in exclude_list:
            continue

        attrs = []
        if translate:
            trans_attr = ['translateX', 'translateY', 'translateZ']
            attrs.extend([each_rst.attr(o) for o in trans_attr])
        if rotate:
            rot_attr = ['rotateX', 'rotateY', 'rotateZ']
            attrs.extend([each_rst.attr(o) for o in rot_attr])
        if scale:
            scl_attr = ['scaleX', 'scaleY', 'scaleZ']
            attrs.extend([each_rst.attr(o) for o in scl_attr])

        for attr in attrs:
            val = attr.get()
            def_val = pm.attributeQuery(attr.plugAttr(), node = attr.node(), listDefault = True)[0]
            if '{:.3f}'.format(val) != '{:.3f}'.format(def_val):
                result.append(each_rst)
                break

    return result


def get_vertex_count(top_node = None):
    """Get the number of vertices in a scene.

    :key top_node: The top node of the hierarchy you want to check.
    :type top_node: pm.PyNode
    :return: Single, visible, and total mesh instances of vertex count in the scene.
     ['single_mesh', 'total_mesh', 'total_visible']
    :rtype: dict
    """
    if top_node is None:
        mesh_list = [o for o in pm.ls(type = 'mesh', ni = True)]
    else:
        mesh_list = top_node.getChildren(ad = True, type = 'mesh', ni = True)

    vertex_count = {
        'single_mesh': 0,
        'total_mesh': 0,
        'total_visible': 0
    }
    for each_mesh in mesh_list:
        all_instances = each_mesh.getInstances()
        ins_count = 0

        for inst in all_instances:
            if not inst.isVisible():
                continue
            if top_node is None:
                ins_count += 1
            else:
                if inst.hasParent(top_node):
                    ins_count += 1
        vertex_count['single_mesh'] += each_mesh.numVertices()
        vertex_count['total_mesh'] += each_mesh.numVertices() * len(all_instances)
        vertex_count['total_visible'] += each_mesh.numVertices() * ins_count

    return vertex_count
# endregion


# region Clean
def clean_unknown_plugins():
    """Remove all unknown plugins expect nodes that exist in scene.
    http://mayastation.typepad.com/maya-station/2015/04/how-to-prevent-maya-writing-a-requires-command-for-a-plug-in.html
    Some unknown plugins may needed in another environment.
    example: Vray plugin will not available to animator but will available to lighting artist.
    """
    unknown_nodes = set()
    for unknown_node in pm.ls(type = ["unknown", "unknownDag"], editable = True):
        unknown_nodes.add(pm.unknownNode(unknown_node, q = True, plugin = True))

    for unknown_plugin in pm.unknownPlugin(query = True, list = True) or []:
        if unknown_plugin in unknown_nodes:
            pass
        else:
            try:
                pm.unknownPlugin(unknown_plugin, remove = True)
            except Exception as err:
                print(err)


def clean_mentalray_nodes():
    """Remove all mental ray nodes in the scene."""
    mentalray_nodes = ['mentalrayGlobals', 'mentalrayItemsList', 'mentalrayOptions', 'mentalrayFramebuffer']
    result = pm.ls(type = mentalray_nodes)
    result.extend(pm.ls([o + '*' for o in mentalray_nodes]))
    pm.delete(result)


def clean_namespace(namespace_list = None):
    """Remove all namespace or supplied namespace list.

    :key namespace_list: Namespace list that need to be removed.
    :type namespace_list: list of str
    """
    if namespace_list is None:
        namespace_list = get_namespaces(exclude_ref = True)

    for o in namespace_list:
        try:
            pm.namespace(removeNamespace = o, mergeNamespaceWithParent = True)
        except Exception as e:
            print('{}, {}'.format(o, e))


def clean_anim_layer(exception_list = None):
    """Remove all animation layer in the scene.

    :key exception_list: Animation layer name that need to be keep.
    :type exception_list: list of str
    """
    if exception_list is None:
        exception_list = []
    layer_node = pm.ls(type = ['animLayer'])

    delete_later = []
    dirty_layer = []
    for o in layer_node:
        if o.getParent() is None:
            delete_later.append(o)
            continue
        if o not in exception_list:
            dirty_layer.append(o)

    pm.delete(dirty_layer)
    pm.delete(delete_later)


def clean_display_layer(exception_list = None):
    """Remove all display layer in the scene.

    :key exception_list: Display layer name that need to be keep.
    :type exception_list: list of str
    """
    if exception_list is None:
        exception_list = []
    exception_list.append('defaultLayer')
    layer_node = pm.ls(type = ['displayLayer'])
    dirty_layer = [o for o in layer_node if o not in exception_list]

    pm.delete(dirty_layer)


def clean_dag_pose():
    """Remove all dagPose/bindPose nodes in the scene."""
    pm.delete(pm.ls(type = 'dagPose'))


def clean_animation_node():
    """Remove all animation nodes in the scene, set driven key will not get deleted."""
    pm.delete(pm.ls(type = ["animCurveTU", "animCurveTL", "animCurveTA"], editable=True))


def clean_unknown_node(exception_list = None):
    """Remove all unknown nodes in the scene except the nodes that
    originated from plugin specified in exception_list.

    :key exception_list: Unknown nodes plugin name that need to keep.
    :type exception_list: list of str
    """
    if exception_list is None:
        exception_list = []
    unknown_nodes = []
    node_list = pm.ls(type = ['unknown', 'unknownDag'], editable = True)
    for each_node in node_list:
        if pm.unknownNode(each_node, q = True, plugin = True) not in exception_list:
            unknown_nodes.append(each_node)

    pm.delete(unknown_nodes)


def clean_unused_node():
    """Remove all unused nodes in the scene."""
    pm.mel.MLdeleteUnused()


def clean_ngskin_node():
    """Remove all ngskin nodes in the scene."""
    ngskin_nodes = pm.ls(type = ['ngSkinLayerData', 'ngSkinLayerDisplay'])
    pm.delete(ngskin_nodes)


def clean_turtle_node():
    """Remove all presistant turtle node from the scene then unload turtle plugin."""
    turtle_nodes = ['TurtleDefaultBakeLayer', 'TurtleBakeLayerManager', 'TurtleRenderOptions', 'TurtleUIOptions']
    for each_node in turtle_nodes:
        if pm.objExists(each_node):
            turtle_node = pm.PyNode(each_node)
            turtle_node.unlock()
            pm.delete(turtle_node)
            pm.mel.ilrDynamicAttributes(0)
    try:
        pm.pluginInfo('Turtle.mll', edit = True, autoload = False)
        pm.unloadPlugin('Turtle.mll', force = True)
    except Exception as e:
        pass


def clean_empty_mesh():
    """Remove all mesh object which don't have face or vertex data"""
    pm.delete(get_empty_mesh())
# endregion


# region Fix
def fix_shading_engine_intermediate(input_shape_intermediate = None):
    """Re-wire shading engine connection that connect to
    intermediate shape to non intermediate shape.

    :key input_shape_intermediate: Intermediate shape that have shading engine connection and need re-wire.
    :type input_shape_intermediate: list of pm.PyNode
    """
    if input_shape_intermediate is not None:
        # shape_inter_list = copy.deepcopy(input_shape_intermediate)
        shape_inter_list = []
        # if there is non shape, get the shape intermediate
        for each_obj in input_shape_intermediate:
            if issubclass(each_obj.__class__, pm.nt.Transform):
                shape_inter_list.extend([o for o in pm.ls(each_obj.getShapes(), io = True) if o.shadingGroups()])
            elif issubclass(each_obj.__class__, pm.nt.Shape) and each_obj.shadingGroups():
                shape_inter_list.append(each_obj)
    else:
        shape_inter_list = get_shading_engine_intermediate()

    for shape_intermediate in shape_inter_list:
        inter_shd_engine_list = shape_intermediate.shadingGroups()
        inter_connection = shape_intermediate.outputs(type = 'shadingEngine', plugs = True)
        if inter_shd_engine_list[0].name() == 'initialShadingGroup':
            shape_intermediate.instObjGroups[0].disconnect(inter_connection[0])
            continue

        # find shape deformed
        shape_deformed = shape_intermediate.getParent().getShape(noIntermediate = True)
        # noninter_shd_engine_list = shape_deformed.shadingGroups()
        noninter_connection = shape_deformed.outputs(type = 'shadingEngine', plugs = True)
        if noninter_connection:
            shape_deformed.instObjGroups[0].disconnect(noninter_connection[0])

        shape_deformed.instObjGroups[0].connect(inter_connection[0])


def fix_duplicate_name(input_duplicate_name = None):
    """Rename specified node into unique name.

    :key input_duplicate_name: PyNode needs to make the name unique.
    :type input_duplicate_name: list of pm.PyNode
    """
    if input_duplicate_name is not None:
        duplicate_name_list = copy.deepcopy(input_duplicate_name)
    else:
        duplicate_name_list = get_duplicate_name()

    for duplicate_node in duplicate_name_list:
        duplicate_name = duplicate_node.longName()
        shortname = duplicate_node.nodeName()
        newshortname = naming.get_unique_name(shortname)

        pm.rename(duplicate_name, newshortname)
# endregion
