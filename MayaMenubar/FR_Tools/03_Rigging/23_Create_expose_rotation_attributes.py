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
fpt.create_expose_rotation(pm.selected()[0])
