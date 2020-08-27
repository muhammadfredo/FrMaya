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

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtCompat
import maya.OpenMayaUI as omui


class BasePsWindow(QtWidgets.QWidget):
    '''
    Pyside base class for dialog window inside maya
    '''
    
    @staticmethod
    def getMayaWindow():
        '''
        Get maya window
        '''
        
        # Get maya main window pointer
        mayaWindowPtr = omui.MQtUtil.mainWindow()
        
        # Wrap maya main window pointer as QWidget
        if mayaWindowPtr is not None:
            return shiboken.wrapInstance( long( mayaWindowPtr ), QtWidgets.QWidget )
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
    
    def BuildUi(self, UIfile):
        '''
        Building Pyside UI from UI file
        
        :param UIfile: UI file as 'BasePath' object
        '''

        # Set main layout of the window
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins( 4,4,4,4 )
        self.setLayout( self.mainLayout )
        
        # Load the UI file
        self.ui = self.setup_ui(UIfile.fullpath)
        
        # Add loaded UI to main layout
        self.mainLayout.addWidget( self.ui )
        
        # Set window size the same as size from UI file 
        size = self.ui.size()
        self.resize( size.width(), size.height() )

    def __init__(self, UIfile, Title = '', *args, **kwargs):
        '''
        Pyside base class for dialog window inside maya
        
        :param uiFile: UI file as 'BasePath' object
        '''
        
        # Init parent class
        super( BasePsWindow, self ).__init__(*args, **kwargs)
        
        # Get maya window to parent for current tool
        MayaWindow = self.getMayaWindow()
        # qtwidgets.QWidget.__init__(self, MayaWindow)
        
        if MayaWindow != False:
            # Parent current tool to maya window 
            self.setParent( MayaWindow )
            # Set usual window system frame,
            # like title, min, and max bar 
            self.setWindowFlags( QtCore.Qt.Window )
            # Set current window tool name
            if not Title:
                Title = UIfile.name
            self.setWindowTitle( Title )
            # Build UI tool from UI file
            self.BuildUi(UIfile)


