"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jun 2022
Info         :

"""
import pymel.core as pm
import FrMaya.puppet as fpt
reload(fpt)

fpt.create_corrective_joint(pm.selected()[0])
