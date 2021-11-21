"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 09 Nov 2021
Info         :

"""
import pymel.core as pm

import FrMaya.core as fmc

[fmc.duplicate_original_mesh(o) for o in pm.selected()]