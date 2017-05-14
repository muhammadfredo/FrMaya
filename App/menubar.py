'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 May, 2017

# Purpose: create menubar in maya
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
import os
import pymel.core.uitypes as pmui
import pymel.core.windows as pywin
import maya.mel as mel
 
class Menubar(pmui.SubMenuItem):
    def __new__(cls, rootFolder, name, parent = None):
#         menuId = cls.generateMenuId("test")
#         print name
#         print rootFolder
#         if pywin.menu( menuId, ex = 1 ):
#             pywin.deleteUI(menuId)
        print 2
#         self = pywin.menu( menuId, l = "test", aob = 1, tearOff = 1, p = parent )
#         pmui.SubMenuItem.__new__(cls, self)
 
    def __init__(self, rootFolder, name=None, parent=None):
        menubarName = os.path.basename(rootFolder)
        print 1
        super( Menubar, self ).__init__( name = menubarName, parent = parent )
        print 3

def buildMenubar():
    # get menubar item
    menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    rootMenubar = os.path.join( menubarItemPath, os.listdir( menubarItemPath )[0] )
    # get maya main window
    mainWindow = mel.eval( "$temp=$gMainWindow" )
    
    # try build the menu
    Menubar( rootMenubar, name = "Asu", parent = mainWindow )
    
    print "Fucking Asshole"