"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 02 May 2021
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm


def select_joint_from_skincluster():
    sel = pm.ls(os = True)
    skin_nodes = []
    for o in sel:
        skin_nodes.extend(fmc.get_skincluster_nodes(o))
    print skin_nodes
    joint_list = []
    for o in skin_nodes:
        joint_list.extend(fmc.get_skincluster_info(o)['joint_list'])
    pm.select(joint_list)


select_joint_from_skincluster()
