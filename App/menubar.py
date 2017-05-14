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
        menubarName = os.path.basename( menubarPath )
        menuId = cls.getMenuId( menubarName.replace( "_", " " ) )
        
        if pywin.menu( menuId, ex = 1 ):
            pywin.deleteUI(menuId)
            
        self = pywin.menu( menuId, l = menuId, aob = 1, tearOff = 1, p = parent )
        return pmui.SubMenuItem.__new__(cls, self)
    
    @staticmethod
    def getMenuId(name):
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
# TODO : - Make it possible to create multiple menubarItem root
# TODO : - Next create .ini which makes different between submenu and toolmenu
    # get menubar item
    menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    rootMenubarPath = os.path.join( menubarItemPath, os.listdir( menubarItemPath )[0] )
    # get maya main window
    mainWindow = mel.eval( "$temp=$gMainWindow" )
    
    # try build the menu
    Menubar( rootMenubarPath, parent = mainWindow )
    
    print "Fucking Asshole"