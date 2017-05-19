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
import PySide.QtGui as qtgui
import PySide.QtCore as qtcore
import PySide.QtUiTools as qtuit
import maya.OpenMayaUI as omui
import shiboken
import os

class FR_BaseQWidget(qtgui.QWidget):
    '''
    Base class for all FR tool PySide widget which will parented to maya main window
    '''
    def GetMayaWindow(self):
        mayaWindowPtr = omui.MQtUtil.mainWindow()
        
        if mayaWindowPtr is not None:
            return shiboken.wrapInstance( long( mayaWindowPtr ), qtgui.QWidget )
        else:
            return False
    
    def BuildUi(self, uiFile):
        currentDir = os.path.dirname(__file__)
        uiFileFullPath = os.path.abspath( os.path.join( currentDir, "uiFile", uiFile + ".ui" ) )
        
        theFile = qtcore.QFile( uiFileFullPath )
        theFile.open( qtcore.QFile.ReadOnly )
        
        self.mainLayout = qtgui.QVBoxLayout()
        self.mainLayout.setContentsMargins( 4,4,4,4 )
        self.setLayout( self.mainLayout )
        
        loader = qtuit.QUiLoader()
        self.ui = loader.load( theFile, parentWidget = self )
        
        self.mainLayout.addWidget( self.ui )
        
        size = self.ui.size()
        self.resize( size.width(), size.height() )
        
        theFile.close()

    def __init__(self, uiFile, *args, **kwargs):
        '''
        Constructor
        '''
        super( FR_BaseQWidget, self ).__init__(*args, **kwargs)
        
        MayaWindow = self.GetMayaWindow()
        
        if MayaWindow != False:
            self.setParent( MayaWindow )
            self.setWindowFlags( qtcore.Qt.Window )
            self.setWindowTitle( uiFile )
            self.BuildUi(uiFile)