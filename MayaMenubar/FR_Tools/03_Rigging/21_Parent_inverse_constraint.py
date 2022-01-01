"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 25 Dec 2021
Info         :

a constraitnt from follicle to control but the control chain still works

same world transform:
    - target -> source
    - target.parent -> space keyword argument
under follicle influence:
    - source, space keyword argument
control chain:
    - target, target.parent
"""
import pymel.core as pm
import FrMaya.puppet as fpt
reload(fpt)

if pm.selected():
    sel = pm.selected()
    fpt.create_matrix_cons(sel[0], sel[2], space = sel[1], maintain_offset = False)
