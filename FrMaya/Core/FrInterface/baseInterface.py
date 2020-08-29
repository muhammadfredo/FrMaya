'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 8 Jul, 2016
#
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
# the new way
try:
    import shiboken
except ImportError:
    import shiboken2 as shiboken

from FrMaya.vendor.Qt import QtCore
from FrMaya.vendor.Qt import QtWidgets
from FrMaya.vendor.Qt import QtCompat
import maya.OpenMayaUI as omui
import pymel.core as pm


class MyQtWindow(QtWidgets.QWidget):
    '''
    Pyside base class for dialog window inside maya
    '''
    
    @staticmethod
    def get_maya_window():
        '''
        Get maya window
        '''
        
        # Get maya main window pointer
        maya_window_ptr = omui.MQtUtil.mainWindow()
        
        # Wrap maya main window pointer as QWidget
        if maya_window_ptr is not None:
            return shiboken.wrapInstance( long( maya_window_ptr ), QtWidgets.QWidget )
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
    
    def build_ui(self, ui_file):
        '''
        Building Pyside UI from UI file
        
        :param ui_file: UI file as 'BasePath' object
        '''

        # Set main layout of the window
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins( 4,4,4,4 )
        self.setLayout( self.mainLayout )
        
        # Load the UI file
        self.ui = self.setup_ui(ui_file.abspath())
        
        # Add loaded UI to main layout
        self.mainLayout.addWidget( self.ui )
        
        # Set window size the same as size from UI file 
        size = self.ui.size()
        self.resize( size.width(), size.height() )

    def __init__(self, ui_file, title_tool = '', *args, **kwargs):
        '''
        Pyside base class for dialog window inside maya
        
        :param uiFile: UI file as 'BasePath' object
        '''
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
            self.setParent( maya_window )
            # Set usual window system frame,
            # like title, min, and max bar 
            self.setWindowFlags( QtCore.Qt.Window )
            # Set current window tool name
            if not title_tool:
                title_tool = ui_file.name
            self.setWindowTitle(title_tool)
            self.setObjectName(title_tool)
            # Build UI tool from UI file
            self.build_ui(ui_file)

            pm.dockControl(
                title_tool,
                label = title_tool.replace("_", " "),
                area = 'left',
                content = title_tool,
                width = self.ui.size().width(),
                allowedArea = ['right', 'left']
            )


