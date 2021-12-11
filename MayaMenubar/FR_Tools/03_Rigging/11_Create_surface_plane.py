"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 11 Dec 2021
Info         :

"""
import pymel.core as pm
import FrMaya.core as fmc
reload(fmc)

[fmc.create_surface_plane(align_to = o)for o in pm.selected()]
