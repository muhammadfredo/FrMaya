"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 20 Feb 2016
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm

if pm.sceneName():
    fmc.backup_file(pm.sceneName())
