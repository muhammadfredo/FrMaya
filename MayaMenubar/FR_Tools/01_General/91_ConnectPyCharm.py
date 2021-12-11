"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 04 Nov 2021
Info         :

"""
import maya.cmds as cmds

if not cmds.commandPort(':4434', query=True):
    print 'Connecting to PyCharm...'
    cmds.commandPort(name=':4434')
