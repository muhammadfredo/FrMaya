"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 18 Dec 2021
Info         :

"""
import pymel.core as pm


for o in pm.ls(defaultNodes = True):
    if pm.lockNode(o, q = True, lockUnpublished = True)[0]:
        pm.lockNode(o, lock = False, lockUnpublished = False)
