"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 21 Dec 2021
Info         :

"""
import pymel.core as pm
import FrMaya.puppet as fpt
reload(fpt)

[fpt.remove_matrix_cons(o) for o in pm.selected()]
