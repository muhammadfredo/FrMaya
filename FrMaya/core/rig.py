"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 15 Sep 2020
Info         :

"""
import pymel.core as pm


def get_skincluster_node(input_node):
    """Get skincluster node from specified PyNode object.

    :arg input_node: PyNode object that have skincluster.
    :type input_node: pm.nt.Transform
    :rtype: pm.nt.SkinCluster
    """
    history_list = input_node.listHistory(pruneDagObjects = True, interestLevel = True)
    skin_node = None
    for o in history_list:
        if o.nodeType() == 'skinCluster':
            skin_node = o

    return skin_node


def get_skincluster_info(skin_node):
    """Get joint influence and skincluster method.

    :arg skin_node: Skincluster PyNode that need to get info extracted.
    :type skin_node: pm.nt.SkinCluster
    :return: Skincluster joint influence, Skin method index.
    :rtype: (list of pm.nt.Joint, int)
    """
    joint_list = []
    skin_method = 0
    if skin_node:
        joint_list = skin_node.getInfluence(q=True)
        skin_method = skin_node.getSkinMethod()

    return joint_list, skin_method


