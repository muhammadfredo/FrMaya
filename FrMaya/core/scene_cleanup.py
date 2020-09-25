"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import pymel.core as pm

from . import scene_info


def clean_unknown_plugins():
    # TODO: docstring here
    # FIXME: some homework need to be done, need to separate clean and get
    # remove unknownplugins expect nodes that exist in scene
    # http://mayastation.typepad.com/maya-station/2015/04/how-to-prevent-maya-writing-a-requires-command-for-a-plug-in.html
    # some unknown plugins may needed in another environment
    # example: Vray plugin will not available to animator but will available to lighting artist

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
    # TODO: docstring here
    # FIXME: some homework need to be done, need to separate clean and get
    mentalray_type = ['mentalrayGlobals', 'mentalrayItemsList', 'mentalrayOptions', 'mentalrayFramebuffer']
    result = pm.ls(type = mentalray_type)
    if result:
        pm.delete(result)


def clean_namespace():
    # TODO: docstring here
    # FIXME: some homework need to be done, need to separate clean and get
    namespace_list = [] # get_namespaces()

    for o in namespace_list:
        try:
            pm.namespace(removeNamespace = o, mergeNamespaceWithParent = True)
        except Exception as e:
            print('{}, {}'.format(o, e))


def clean_anim_layer():
    # TODO: docstring here
    # FIXME: some homework need to be done
    default_layer = ['BaseAnimation']
    layer_node = pm.ls(type = ['animLayer'])
    dirty_layer = [o for o in layer_node if o not in default_layer]
    pm.delete(dirty_layer)

    # need evalDeferred waiting to update or something
    # or else it will screw up some transform that got anim layer connection
    pm.evalDeferred("pm.delete(pm.PyNode('BaseAnimation'))")


def clean_display_layer():
    # TODO: docstring here
    # FIXME: some homework need to be done
    default_layer = ['defaultLayer']
    layer_node = pm.ls(type = ['displayLayer'])
    dirty_layer = [o for o in layer_node if o not in default_layer]

    pm.delete(dirty_layer)


def fix_shading_engine_intermediate():
    # TODO: docstring here
    # FIXME: some homework need to be done
    shape_inter_list = scene_info.get_shading_engine_intermediate()
    # shape_inter_list = pm.ls(type = 'mesh', intermediateObjects = True)
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

        shape_deformed.instObjGroups[0] >> inter_connection[0]
    #     if inter_shd_engine_list:
    #         if inter_shd_engine_list[0].name() == 'initialShadingGroup':
    #             continue
    #         the_object = shape_intermediate.getParent()
    #         shape_deformed = the_object.getShape(noIntermediate = 1)
    #         noninter_shd_engine_list = shape_deformed.shadingGroups()
    #         if noninter_shd_engine_list:
    #             if noninter_shd_engine_list[0].name() == 'initialShadingGroup':
    #                 continue
    #             inter_connection = shape_intermediate.outputs(type = 'shadingEngine', plugs = 1)
    #             noninter_connection = shape_deformed.outputs(type = 'shadingEngine', plugs = 1)
    #
    #             shape_intermediate.instObjGroups[0].disconnect(destination = inter_connection[0])
    #             shape_deformed.instObjGroups[0].disconnect(destination = noninter_connection[0])
    #
    #             shape_deformed.instObjGroups[0] >> inter_connection[0]







