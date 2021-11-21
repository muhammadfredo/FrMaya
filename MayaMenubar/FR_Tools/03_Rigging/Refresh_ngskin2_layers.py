"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 18 Nov 2021
Info         :

"""
import pymel.core as pm
from ngSkinTools2.api import Layers

import FrMaya.core as fmc


def refresh_ngskin2_layers():
    sel = pm.ls(os = True)
    if not sel:
        return

    for o in sel:
        skin_node = fmc.get_skincluster_node(o)

        layers = Layers(skin_node.longName())
        for l in layers.list():
            state = l.enabled
            l.enabled = not state
            l.enabled = state


refresh_ngskin2_layers()
