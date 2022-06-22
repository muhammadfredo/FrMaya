"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 21 Jun 2022
Info         :

"""
import pymel.core as pm
import FrMaya.puppet as fpt
reload(fpt)

try:
    pm.PyNode('ExposeRotationSystem')
except pm.MayaNodeError:
    pm.createNode('transform', n = 'ExposeRotationSystem', ss = True)
last_selection = pm.selected()
fpt.create_expose_rotation(pm.selected()[0], hide_dag = False)
pm.select(last_selection)
