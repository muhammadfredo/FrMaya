'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 May, 2017
#
# Purpose: create menubar in maya
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
import os
import pymel.core as pm
import pymel.core.uitypes as pmui
import pymel.core.windows as pywin
import maya.mel as mel
 
class Menubar(pmui.SubMenuItem):
    def __new__(cls, menubarPath, parent = None):
        '''
        Before initialize of the object,
            create the menubar root, convert menubarPath to menubarName,
            hook/parent it to maya menubar, and refresh the whole menubar if the menubar root already exist
        
        :param cls: The class of this object
        :param menubarPath: Path folder to collection of folder which will be used as menubar root
        :param parent: Parent of menubar root, in this case $gMainWindow
        '''
        
        # give menubar proper name which is basename instead fullpath name
        menubarName = os.path.basename( menubarPath )
        menuName = cls.getMenuName( menubarName.replace( "_", " " ) )
        
        # delete existing menu if the menu already exist
        if pywin.menu( menuName, ex = 1 ):
            pywin.deleteUI(menuName)
            
        self = pywin.menu( menuName, l = menuName, aob = True, tearOff = True, p = parent )
        return pmui.SubMenuItem.__new__(cls, self)
    
    @staticmethod
    def getMenuName(name):
        '''
        TODO: write docstring documentation here
        :param name:
        '''
        
        # get menu name and use it for menu identifier
        menuName = ""
        for char in name:
            if char.isalpha() or char.isdigit() or char.isspace():
                menuName += char
        return menuName

    def __init__(self, menubarPath, name=None, parent=None):
        '''
        An Object that handle building menubar in maya
        
        :param menubarPath: Path folder to collection of folder which will be used as menubar root
        :param name: Menubar root name
        :param parent: Parent of menubar root, in this case $gMainWindow
        '''
        
        # Convert input variable to object variable
        self.menubarPath = menubarPath
        
        # Refresh menu each time the menuitem will opened
        self.postMenuCommand( pm.Callback( self.refreshMenu ) )
    
    def refreshMenu(self):
        '''
        Refresh the submenu each time cursor hover to this menubar root
        '''
        
        # Delete all submenu
        self.deleteAllItems()
        # Rebuild all submenu
        self.buildSubMenu( self.menubarPath, self )
    
    def buildSubMenu(self, fullpath, parent):
        '''
        Build submenu, can be recursive
        
        :param fullpath: path folder to collection of folder or file
            which will be used to create menuItem or Submenu
        :param parent: submenu or menu parent which will be parented to
        '''
        
        # list all folder, file on current path(fullpath)
        for o in os.listdir( fullpath ):
            # fullpath of each file/folder inside current path(fullpath)
            thePath = os.path.join( fullpath, o ).replace("\\","/")
            # separated filename and extension
            fileName, ext = os.path.splitext( o )
            
            # check if the path is file or folder
            if os.path.isdir( thePath ):
                # create submenu
                submenu = pywin.subMenuItem( label = o, subMenu = True, p = parent, tearOff = True, postMenuCommandOnce = 1 )
                # recursive buildSubMenu
                self.buildSubMenu( thePath, submenu )
            # if file is python
            elif ext == '.py':
                # get nice name for menu label
                menuName = self.getMenuName( fileName.replace( "_", " " ) )
                # command of menuitem
                commandScript = 'execfile("{0}")'.format( thePath )
                # create menuitem
                pywin.menuItem( label = menuName, p = parent, tearOff = True, command = commandScript )
            elif ext == '.mel':
                # get nice name for menu label
                menuName = self.getMenuName( fileName.replace( "_", " " ) )
                # command of menuitem
                commandScript = 'import maya.mel as mel\nmel.eval( "source \\"{0}\\"" )'.format( thePath )
                # create menuitem
                pywin.menuItem( label = menuName, p = parent, tearOff = True, command = commandScript )

def buildMenubar():
    '''
    Build menubar function
    '''
    
    # get all menubar root item
    menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    menubarList = os.listdir( menubarItemPath )
    # get maya main window
    mainWindow = mel.eval( "$temp=$gMainWindow" )
    
    # build all menubar root item
    for o in menubarList:
        Menubar( os.path.join( menubarItemPath, o ), parent = mainWindow )