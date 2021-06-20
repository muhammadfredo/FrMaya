"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 29 Apr 2021
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm
reload(fmc)
fmc.transfer_skincluster(pm.ls(os=1)[0], pm.ls(os=1)[1:])
