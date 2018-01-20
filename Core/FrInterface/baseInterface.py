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

import os
import shiboken

import PySide.QtCore as qtcore
import PySide.QtGui as qtgui
import PySide.QtUiTools as qtuit
import maya.OpenMayaUI as omui


class BasePsWindow(qtgui.QWidget):
    '''
    Pyside base class for dialog window inside maya
    '''
    
    @staticmethod
    def GetMayaWindow():
        '''
        Get maya window
        '''
        
        # Get maya main window pointer
        mayaWindowPtr = omui.MQtUtil.mainWindow()
        
        # Wrap maya main window pointer as QWidget
        if mayaWindowPtr is not None:
            return shiboken.wrapInstance( long( mayaWindowPtr ), qtgui.QWidget )
        else:
            return False
    
    def BuildUi(self, UIfile):
        '''
        Building Pyside UI from UI file
        
        :param UIfile: UI file as 'BasePath' object
        '''
        
        # Open ui file, and prepare for reading the file
        theFile = qtcore.QFile( UIfile.fullpath )
        theFile.open( qtcore.QFile.ReadOnly )
        
        # Set main layout of the window
        self.mainLayout = qtgui.QVBoxLayout()
        self.mainLayout.setContentsMargins( 4,4,4,4 )
        self.setLayout( self.mainLayout )
        
        # Load the UI file
        loader = qtuit.QUiLoader()
        self.ui = loader.load( theFile, parentWidget = self )
        
        # Add loaded UI to main layout
        self.mainLayout.addWidget( self.ui )
        
        # Set window size the same as size from UI file 
        size = self.ui.size()
        self.resize( size.width(), size.height() )
        
        # Close the UI file
        theFile.close()

    def __init__(self, UIfile, Title = '', *args, **kwargs):
        '''
        Pyside base class for dialog window inside maya
        
        :param uiFile: UI file as 'BasePath' object
        '''
        
        # Init parent class
        super( BasePsWindow, self ).__init__(*args, **kwargs)
        
        # Get maya window to parent for current tool
        MayaWindow = self.GetMayaWindow()
        
        if MayaWindow != False:
            # Parent current tool to maya window 
            self.setParent( MayaWindow )
            # Set usual window system frame,
            # like title, min, and max bar 
            self.setWindowFlags( qtcore.Qt.Window )
            # Set current window tool name
            if not Title:
                Title = UIfile.name
            self.setWindowTitle( Title )
            # Build UI tool from UI file
            self.BuildUi(UIfile)


