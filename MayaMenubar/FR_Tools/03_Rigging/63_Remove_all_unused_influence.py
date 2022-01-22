"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jan 2022
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm


all_skin_node = pm.ls(type='skinCluster')
[fmc.remove_unused_influence(o) for o in all_skin_node]
