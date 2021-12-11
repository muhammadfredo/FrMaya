"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 11 Dec 2021
Info         :

"""
import pymel.core as pm
import FrMaya.puppet as fpt

sel = pm.selected()
fpt.create_matrix_cons(sel[0], sel[1])
