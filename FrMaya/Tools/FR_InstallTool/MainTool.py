'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 29 Apr 2018
Purpose      :

'''

from FrMaya.Core.FrInterface import baseInterface
from FrMaya.Core import FrFile


class MainGUI( baseInterface.BasePsWindow ):

    def __init__(self, *args):
        # Convert ui path file as FrFile Object
        ui_file = FrFile.PathNode( __file__ ).parent.getChildren( 'FR_InstallTool.ui' )
        super( MainGUI, self ).__init__( ui_file, *args )