"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jan 2022
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm


def remove_unused_influence_hierarchy():
    for o in pm.selected():
        children = o.getChildren(ad = True)
        for x in children:
            skin_node = fmc.get_skincluster_node(x)
            if skin_node:
                fmc.remove_unused_influence(skin_node)


remove_unused_influence_hierarchy()
