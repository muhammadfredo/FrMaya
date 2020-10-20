"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 12 May 2017
Refactor Date   : 29 Agt 2020
Info         :

"""
import os

try:
    import shiboken
except ImportError:
    import shiboken2 as shiboken
from maya import mel as mel
from maya import OpenMayaUI as omui
from pymel import core as pm
from pymel.core import uitypes as pmui
from pymel.core import windows as pywin
from FrMaya.vendor.Qt import QtCore, QtCompat, QtWidgets

from FrMaya.core import system


def get_menu_name(name):
    """Make any supplied string suitable/nice for menubar name.

    :arg name: Name need to make nice for menubar.
    :type name: str
    :return: Nice menu name for menubar.
    :rtype: str
    """

    # get menu name and use it for menu identifier
    menu_name = ""
    for char in name:
        if char == '_' or char == '-':
            char = ' '
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
        menu_name = get_menu_name(menubar_name)

        # delete existing menu if the menu already exist
        if pywin.menu(menu_name, ex = 1):
            pywin.deleteUI(menu_name)

        # build root menu and return it as pmui.SubMenuItem
        self = pywin.menu(menu_name, label = menu_name, aob = True, tearOff = True, p = parent)
        return pmui.SubMenuItem.__new__(cls, self)

    def __init__(self, menubar_path, name = None, parent = None):
        """
        An Object that handle building menubar in maya

        :param menubar_path: Path folder to collection of folder which will be used as menubar root
        :param name: Menubar root name
        :param parent: Parent of menubar root, in this case $gMainWindow
        """
        super(Menubar, self).__init__()

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
        for dir_name in os.listdir(fullpath):
            # fullpath of each file/folder inside current path(fullpath)
            the_path = os.path.join(fullpath, dir_name).replace("\\", "/")
            # separated filename and extension
            file_name, ext = os.path.splitext(dir_name)

            # remove number and underline
            # number and underline in folder for sorting purpose :))
            try:
                int(file_name[:1])
                file_name = file_name[3:]
            except ValueError:
                pass
            # get nice name for menu label
            menu_name = get_menu_name(file_name)

            # check if the path is file or folder
            if os.path.isdir(the_path):
                # create submenu
                submenu = pywin.subMenuItem(label = menu_name, subMenu = True, p = parent, tearOff = True,
                                            postMenuCommandOnce = 1)
                # recursive buildSubMenu
                self.build_sub_menu(the_path, submenu)
            # if file is python
            elif ext == '.py':
                # command of menuitem
                command_script = 'execfile("{0}")'.format(the_path)
                # create menuitem
                pywin.menuItem(label = menu_name, p = parent, tearOff = True, command = command_script)
            elif ext == '.mel':
                # command of menuitem
                command_script = 'import maya.mel as mel\nmel.eval( "source \\"{0}\\"" )'.format(the_path)
                # create menuitem
                pywin.menuItem(label = menu_name, p = parent, tearOff = True, command = command_script)


def build_menubar():
    """Build menubar function"""
    menubar_path_list = system.get_menubar_path()
    print menubar_path_list
    # get all menubar root item
    menubar_list = []
    for o in menubar_path_list:
        menubar_list += o.listdir()
    # get maya main window
    main_window = mel.eval("$temp=$gMainWindow")

    # build all menubar root item
    for menubar_root in menubar_list:
        Menubar(menubar_root, parent = main_window)


class MyQtWindow(QtWidgets.QWidget):
    """
    Pyside base class for dialog window inside maya
    """

    @staticmethod
    def get_maya_window():
        """
        Get maya window
        """

        # Get maya main window pointer
        maya_window_ptr = omui.MQtUtil.mainWindow()

        # Wrap maya main window pointer as QWidget
        if maya_window_ptr is not None:
            return shiboken.wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)
        else:
            return False

    @staticmethod
    def setup_ui(uifile, base_instance=None):
        """Load a Qt Designer .ui file and returns an instance of the user interface
        Args:
            uifile (str): Absolute path to .ui file
            base_instance (QWidget): The widget into which UI widgets are loaded
        Returns:
            QWidget: the base instance
        """
        ui = QtCompat.loadUi(uifile)  # Qt.py mapped function
        if not base_instance:
            return ui
        else:
            for member in dir(ui):
                if not member.startswith('__') and \
                   member is not 'staticMetaObject':
                    setattr(base_instance, member, getattr(ui, member))
            return ui

    def __init__(self, ui_file, title_tool = '', *args, **kwargs):
        """
        Pyside base class for dialog window inside maya

        :param uiFile: UI file as 'BasePath' object
        """
        # remove existing tool first
        try:
            pm.deleteUI(title_tool)
        except Exception as e:
            print e
        # Init parent class
        super(MyQtWindow, self).__init__(*args, **kwargs)

        self.ui = None
        self.mainLayout = None

        # Get maya window to parent for current tool
        maya_window = self.get_maya_window()
        # qtwidgets.QWidget.__init__(self, MayaWindow)

        if maya_window:
            # Parent current tool to maya window
            self.setParent(maya_window)
            # Set usual window system frame,
            # like title, min, and max bar
            self.setWindowFlags(QtCore.Qt.Window)
            # Set current window tool name
            if not title_tool:
                title_tool = ui_file.name
            self.setWindowTitle(title_tool)
            self.setObjectName(title_tool)
            # Build UI tool from UI file
            self.build_ui(ui_file)

    def build_ui(self, ui_file):
        """
        Building Pyside UI from UI file

        :param ui_file: UI file as 'BasePath' object
        """

        # Set main layout of the window
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self.mainLayout)

        # Load the UI file
        self.ui = self.setup_ui(ui_file.abspath())

        # Add loaded UI to main layout
        self.mainLayout.addWidget(self.ui)

        # Set window size the same as size from UI file
        size = self.ui.size()
        self.resize(size.width(), size.height())

    def docking(self, direction = 'left'):
        title_tool = self.objectName()
        width_tool = self.size().width()
        pm.dockControl(
            title_tool,
            label = title_tool.replace("_", " "),
            area = direction,
            content = title_tool,
            width = width_tool,
            allowedArea = ['right', 'left']
        )

