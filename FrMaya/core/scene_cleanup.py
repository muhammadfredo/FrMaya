"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import pymel.core as pm


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







