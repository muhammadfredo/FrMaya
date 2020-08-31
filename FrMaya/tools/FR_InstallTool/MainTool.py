"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 29 Apr 2018
Purpose      :

"""
import FrMaya.core.uimaya
from FrMaya.vendor import path


class MainGUI(FrMaya.core.uimaya.MyQtWindow):

    def __init__(self, *args):
        # Convert ui path file as FrFile Object
        ui_file = path.Path(__file__).parent / 'FR_InstallTool.ui'
        super(MainGUI, self).__init__(ui_file, *args)
