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
import shutil
from functools import partial

import pymel.core as pm
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
        self.ui.update_btn.released.connect(partial(self.update_released))
        self.ui.remove_btn.released.connect(partial(self.remove_released))

    def set_source_path(self, input_path):
        source_path = path.Path(input_path)
        self.source_path = source_path

    @staticmethod
    def check_update():
        local_version = FrMaya.versiontuple()
        server_version = fmc.get_server_version()
        for lv, sv in zip(local_version, server_version):
            if lv < sv:
                return True
        return False

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
                fmc.install(self.source_path, package_title = 'FrMaya', local_install = True)
            elif result == 'remote':
                fmc.install(self.source_path, package_title = 'FrMaya')

            message = 'FrMaya succesfuly installed.\nPlease restart maya.'
        except (Exception, ImportError) as e:
            message = 'FrMaya failed to install.\n{0}'.format(e)

        if result != 'cancel':
            # show result of installation
            pm.confirmDialog(t = 'FrMaya', m = message, b = ['Ok'], db = 'Ok')

    def update_released(self):
        mssg = 'Installed version :  '
        mssg += '{}\n '.format(FrMaya.version())
        mssg += 'Server version   :  '
        mssg += '{}\n\n'.format('.'.join(str(x) for x in fmc.get_server_version()))
        if self.check_update():
            mssg += 'New version available!!'
            btn_list = ['Yes', 'No']
        else:
            mssg += 'No new version.'
            btn_list = ['Ok']
        result = pm.confirmDialog(t = 'FrMaya Update', b = btn_list, m = mssg)

        message = ''
        try:
            if result == 'Yes':
                zip_file, new_frmaya_dir = fmc.download_latest_version(target_name = 'FrMaya')

                # check if its local
                frmaya_local = fmc.check_local_package('FrMaya')
                if frmaya_local:
                    fmc.install(new_frmaya_dir, local_install = True)
                else:
                    old_package_dir = path.Path(FrMaya.basedir()).parent
                    shutil.rmtree(old_package_dir, ignore_errors = True)
                    shutil.copytree(new_frmaya_dir.abspath(), old_package_dir.abspath())
                    fmc.install(old_package_dir)

                message = 'FrMaya succesfuly updated.\nPlease restart maya.'
        except Exception as e:
            message = 'FrMaya failed to update.\n{0}'.format(e)

        # show result of updating frmaya
        pm.confirmDialog(t = 'FrMaya info', m = message, b = ['Ok'], db = 'Ok')

    @staticmethod
    def remove_released():
        result = pm.confirmDialog(t = 'FrMaya Remove', b = ['Yes', 'No'], m = 'Are you sure?')

        message = ''
        try:
            if result == 'Yes':
                fmc.uninstall('FrMaya')
                message = 'FrMaya succesfuly removed.\nPlease restart maya.'
        except Exception as e:
            message = 'FrMaya failed to remove.{0}'.format(e)
        # show result of removing frmaya
        pm.confirmDialog(t = 'FrMaya info', m = message, b = ['Ok'], db = 'Ok')



