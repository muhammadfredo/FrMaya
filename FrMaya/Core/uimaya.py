"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 12 May 2017
Refactor Date   : 29 Agt 2020
Info         :

"""
import os

import maya.mel as mel
import pymel.core as pm
import pymel.core.uitypes as pmui
import pymel.core.windows as pywin
from maya import mel as mel
from pymel import core as pm
from pymel.core import uitypes as pmui, windows as pywin


def get_menu_name(name):
    """
    :param name:
    """
    # type: str > str
    # TODO: write docstring documentation here

    # get menu name and use it for menu identifier
    menu_name = ""
    for char in name:
        if char.isalpha() or char.isdigit() or char.isspace():
            menu_name += char
    return menu_name


class Menubar(pmui.SubMenuItem):
    def __new__(cls, menubar_path, parent = None):
        """
        Before initialize of the object,
            create the menubar root, convert menubar_path to menubarName,
            hook/parent it to maya menubar, and refresh the whole menubar if the menubar root already exist

        :param cls: The class of this object
        :param menubar_path: Path folder to collection of folder which will be used as menubar root
        :param parent: Parent of menubar root, in this case $gMainWindow
        """

        # give menubar proper name which is basename instead fullpath name
        menubar_name = os.path.basename(menubar_path)
        menu_name = get_menu_name(menubar_name.replace("_", " "))

        # delete existing menu if the menu already exist
        if pywin.menu(menu_name, ex = 1):
            pywin.deleteUI(menu_name)

        # TODO: need comment here
        self = pywin.menu(menu_name, label = menu_name, aob = True, tearOff = True, p = parent)
        return pmui.SubMenuItem.__new__(cls, self)

    def __init__(self, menubar_path, name = None, parent = None):
        """
        An Object that handle building menubar in maya

        :param menubar_path: Path folder to collection of folder which will be used as menubar root
        :param name: Menubar root name
        :param parent: Parent of menubar root, in this case $gMainWindow
        """

        # Convert input variable to object variable
        self.menubarPath = menubar_path

        # Refresh menu each time the menuitem will opened
        self.postMenuCommand(pm.Callback(self.refresh_menu))

    def refresh_menu(self):
        """
        Refresh the submenu each time cursor hover to this menubar root
        """

        # Delete all submenu
        self.deleteAllItems()
        # Rebuild all submenu
        self.build_sub_menu(self.menubarPath, self)

    def build_sub_menu(self, fullpath, parent):
        """
        Build submenu, can be recursive

        :param fullpath: path folder to collection of folder or file
            which will be used to create menuItem or Submenu
        :param parent: submenu or menu parent which will be parented to
        """

        # list all folder, file on current path(fullpath)
        for o in os.listdir(fullpath):
            # fullpath of each file/folder inside current path(fullpath)
            the_path = os.path.join(fullpath, o).replace("\\", "/")
            # separated filename and extension
            file_name, ext = os.path.splitext(o)

            # check if the path is file or folder
            if os.path.isdir(the_path):
                # remove number and underline
                # number and underline in folder for sorting purpose :))
                try:
                    int(o[:1])
                    o = o[3:]
                    o = o.replace("_", " ")
                except ValueError:
                    pass
                # create submenu
                submenu = pywin.subMenuItem(label = o, subMenu = True, p = parent, tearOff = True,
                                            postMenuCommandOnce = 1)
                # recursive buildSubMenu
                self.build_sub_menu(the_path, submenu)
            # if file is python
            elif ext == '.py':
                # get nice name for menu label
                menu_name = get_menu_name(file_name.replace("_", " "))
                # command of menuitem
                command_script = 'execfile("{0}")'.format(the_path)
                # create menuitem
                pywin.menuItem(label = menu_name, p = parent, tearOff = True, command = command_script)
            elif ext == '.mel':
                # get nice name for menu label
                menu_name = get_menu_name(file_name.replace("_", " "))
                # command of menuitem
                command_script = 'import maya.mel as mel\nmel.eval( "source \\"{0}\\"" )'.format(the_path)
                # create menuitem
                pywin.menuItem(label = menu_name, p = parent, tearOff = True, command = command_script)


def build_menubar():
    """
    Build menubar function
    """
    # TODO: change BasePath to abstract class
    import FrMaya.App as app

    menubar_item_path = os.path.join(os.path.dirname(app.__file__), 'menubarItem')
    # get all menubar root item
    #     menubarItemPath = os.path.join( os.path.dirname(__file__), 'menubarItem' )
    menubar_list = os.listdir(menubar_item_path)
    # get maya main window
    main_window = mel.eval("$temp=$gMainWindow")

    # build all menubar root item
    for o in menubar_list:
        Menubar(os.path.join(menubar_item_path, o), parent = main_window)
