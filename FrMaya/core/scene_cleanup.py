"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import copy

import pymel.core as pm

from . import scene_info


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
        namespace_list = scene_info.get_namespaces(exclude_ref = True)

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
    dirty_layer = [o for o in layer_node if o not in exception_list]
    pm.delete(dirty_layer)


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


def fix_shading_engine_intermediate(input_shape_intermediate = None):
    """Re-wire shading engine connection that connect to
    intermediate shape to non intermediate shape.

    :key input_shape_intermediate: Intermediate shape that have shading engine connection and need re-wire.
    :type input_shape_intermediate: list of pm.PyNode
    """
    if input_shape_intermediate is not None:
        shape_inter_list = copy.deepcopy(input_shape_intermediate)
    else:
        shape_inter_list = scene_info.get_shading_engine_intermediate()

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
    pm.unloadPlugin('Turtle.mll', force = True)


def fix_duplicate_name(input_duplicate_name = None):
    """Rename specified node into unique name.

    :key input_duplicate_name: PyNode needs to make the name unique.
    :type input_duplicate_name: list of pm.PyNode
    """
    if input_duplicate_name is not None:
        duplicate_name_list = copy.deepcopy(input_duplicate_name)
    else:
        duplicate_name_list = scene_info.get_duplicate_name()

    for duplicate_node in duplicate_name_list:
        duplicate_name = duplicate_node.longName()
        shortname = duplicate_node.nodeName()
        newshortname = shortname
        i = 1
        while len(pm.ls(newshortname)) > 0:
            # generate a new name until there is no object with this name
            newshortname = '{}{}'.format(shortname, i)
            i += 1

        pm.rename(duplicate_name, newshortname)





