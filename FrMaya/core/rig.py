"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 15 Sep 2020
Info         :

"""


def get_skincluster_node(input_node):
    # TODO: docstring here
    history_list = input_node.listHistory(pruneDagObjects = True, interestLevel = True)
    skin_node = None
    for o in history_list:
        if o.nodeType() == 'skinCluster':
            skin_node = o

    return skin_node


def get_joint_influence(skin_node):
    # TODO: docstring here
    joint_list = []
    skin_method = 0
    if skin_node:
        joint_list = skin_node.getInfluence(q=True)
        skin_method = skin_node.getSkinMethod()

    return joint_list, skin_method


