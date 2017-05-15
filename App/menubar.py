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
    def __new__(cls, menubarPath, parent = None):
        # give menubar proper name which is basename instead fullpath name
        menubarName = os.path.basename( menubarPath )
        menuId = cls.getMenuId( menubarName.replace( "_", " " ) )
        
        # delete existing menu if the menu already exist
        if pywin.menu( menuId, ex = 1 ):
            pywin.deleteUI(menuId)
            
        self = pywin.menu( menuId, l = menuId, aob = 1, tearOff = 1, p = parent )
        return pmui.SubMenuItem.__new__(cls, self)
    
    @staticmethod
    def getMenuId(name):
        # get menu name and use it for menu identifier
        menuName = ""
        for char in name:
            if char.isalpha() or char.isdigit() or char.isspace():
                menuName += char
        return menuName
 
    def __init__(self, menubarPath, name=None, parent=None):
        self.menubarPath = menubarPath
        
        self.buildSubMenu( self )
    
    def buildSubMenu(self, parent):
        # get all subfolder
        subfolder = os.listdir( parent.menubarPath )
        
        for o in subfolder:
#             Menubar( os.path.join( parent.menubarPath, o ), parent = self )
            pywin.subMenuItem( label = o, subMenu = 1, p = self, tearOff = 1, postMenuCommandOnce = 1 )

def buildMenubar():
# TODO: Next create .ini which makes different between submenu and toolmenu
    # get all menubar root item
    menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    menubarList = os.listdir( menubarItemPath )
    # get maya main window
    mainWindow = mel.eval( "$temp=$gMainWindow" )
    
    # build all menubar root item
    for o in menubarList:
        Menubar( os.path.join( menubarItemPath, o ), parent = mainWindow )
    
    print "Fucking Asshole"