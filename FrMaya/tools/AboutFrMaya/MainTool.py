"""
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 Sep, 2017
# Last Modified Date       :
# Purpose:
# Bugs:
# History:
# Note:
####################################################################################
####################################################################################
"""
import os
import urllib2
import tempfile
from functools import partial

import pymel.core as pm
from FrMaya.vendor import yaml
from FrMaya.vendor import path

import FrMaya.core as fmc
import FrMaya


class MainGUI(fmc.MyQtWindow):
    """
    Main GUI for FrMaya About
    """

    def __init__(self, source_path = '', *args):
        """
        Constructor of main GUI for FR_RiggingTool
        """
        # Convert ui path file as FrFile Object
        ui_file = path.Path(__file__).parent / 'AboutFrMaya.ui'
        super(MainGUI, self).__init__(ui_file, title_tool = 'About FrMaya', *args)

        self.source_path = path.Path(source_path)

        self.connect_event_handlers()

    def connect_event_handlers(self):
        # show current fr maya version
        self.ui.versionNum_lbl.setText(FrMaya.version())

        self.ui.install_btn.released.connect(partial(self.install_released))
        # self.ui.update_btn.released.connect(partial(self.update_released))
        self.ui.remove_btn.released.connect(partial(self.remove_released))

    def set_source_path(self, input_path):
        source_path = path.Path(input_path)
        self.source_path = source_path

    def install_released(self):
        mssg = 'Local install ::\n'
        mssg += '    FrMaya python package and the module will\n '
        mssg += 'be copied to maya user application directory.\n '
        mssg += '\n'
        mssg += 'Remote install ::\n'
        mssg += '    Only FrMaya module will be copied to maya\n '
        mssg += 'user application directory.'

        # show install option
        result = pm.confirmDialog(
            title = 'FrMaya Install Option',
            button = ['local', 'remote', 'cancel'],
            messageAlign = 'center',
            message = mssg
        )
        try:
            if result == 'local':
                fmc.install(self.source_path, local_install = True)
            elif result == 'remote':
                fmc.install(self.source_path)

            message = 'FrMaya succesfuly installed.\nPlease restart maya.'
        except (Exception, ImportError) as e:
            message = 'FrMaya failed to install.\n{0}'.format(e)

        if result != 'cancel':
            # show result of installation
            pm.confirmDialog(t = 'FrMaya', m = message, b = ['Ok'], db = 'Ok')

    # TODO: Update method need to be implemented
    # def update_released(self):
    #     update_bool = False
    #     build_link = 'https://www.dropbox.com/s/8lh6pbqqh42cktm/build_link.yml?dl=1'
    #
    #     result_url = urllib2.urlopen(build_link)
    #     data = yaml.load(result_url.read())
    #     result_url.close()
    #
    #     server_version = data.get('FrMaya').get('version')
    #     for i in range(len(server_version)):
    #         if FrMaya.versiontuple()[i] < server_version[i]:
    #             update_bool = True
    #             break
    #
    #     if update_bool:
    #         # FIXME: get build_link.yml first, compare version, decide, then download the zip url
    #         temp_zip = os.path.join(tempfile.gettempdir(), 'temp.zip')
    #         temp_frmaya = os.path.join(tempfile.gettempdir(), 'temp_frmaya')
    #         zip_url = data.get('FrMaya').get('zip_url')
    #
    #         # open( temp_zip, 'wb' ).write(
    #         #     urllib2.urlopen( zip_url ).read() )
    #         # print 'INFO: Extracting plugin to : ' + temp_frmaya
    #         # zipfile.ZipFile( temp_zip ).extractall( temp_frmaya )
    #
    #         # check if its local
    #         usd = pm.internalVar(usd = True)
    #         print self.source_path
    #         if self.source_path.startswith(usd):
    #             print 'Great'

    @staticmethod
    def remove_released():
        result = pm.confirmDialog(t = 'FrMaya', b = ['Yes', 'No'], m = 'Are you sure?')

        message = ''
        try:
            if result == 'Yes':
                fmc.uninstall('FrMaya')
                message = 'FrMaya succesfuly removed.\nPlease restart maya.'
        except Exception as e:
            message = 'FrMaya failed to remove.{0}'.format(e)
        # show result of removing frmaya
        pm.confirmDialog(t = 'FrMaya', m = message, b = ['Ok'], db = 'Ok')



