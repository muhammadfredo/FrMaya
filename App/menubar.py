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
        
        self.buildSubMenu( self.menubarPath, self )
    
    def buildSubMenu(self, fullpath, parent):
        # list all folder, file on current path(fullpath)
        for o in os.listdir( fullpath ):
            # fullpath of each file/folder inside current path(fullpath)
            thePath = os.path.join( fullpath, o ).replace("\\","/")
            # separated filename and extension
            fileName, ext = os.path.splitext( o )
            
            # check if the path is file or folder
            if os.path.isdir( thePath ):
                # create submenu
                submenu = pywin.subMenuItem( label = o, subMenu = 1, p = parent, tearOff = 1, postMenuCommandOnce = 1 )
                # recursive buildSubMenu
                self.buildSubMenu( thePath, submenu )
            # if file is python
            elif ext == '.py':
                # get nice name for menu label
                menuId = self.getMenuId( fileName.replace( "_", " " ) )
                # command of menuitem
                commandScript = 'execfile("{0}")'.format( thePath )
                # create menuitem
                pywin.menuItem( label = menuId, p = parent, tearOff = 1, command = commandScript )
            elif ext == '.mel':
                # get nice name for menu label
                menuId = self.getMenuId( fileName.replace( "_", " " ) )
                # command of menuitem
                commandScript = 'import maya.mel as mel\nmel.eval( "source \\"{0}\\"" )'.format( thePath )
                # create menuitem
                pywin.menuItem( label = menuId, p = parent, tearOff = 1, command = commandScript )

def buildMenubar():
    # get all menubar root item
    menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    menubarList = os.listdir( menubarItemPath )
    # get maya main window
    mainWindow = mel.eval( "$temp=$gMainWindow" )
    
    # build all menubar root item
    for o in menubarList:
        Menubar( os.path.join( menubarItemPath, o ), parent = mainWindow )