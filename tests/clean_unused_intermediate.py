"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 08 Jan 2022
Info         :

"""
import pymel.core as pm

foo = pm.ls(type='mesh', intermediateObjects=True)
for o in foo:
    if not o.outputs() and not o.inputs():
        pm.delete(o)
    #print o, o.outputs(), o.inputs()