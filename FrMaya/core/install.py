"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 12 Feb 2018
Refactor Date   : 01 Sep 2020
Info         :

"""
import os
import shutil

from pymel import core as pm


def install(*args, **kwargs):
    # TODO: docstring here
    if kwargs:
        # Maya user script path
        usd = pm.internalVar(usd = True)
        if kwargs.get('source') and kwargs.get('local'):
            # uninstall frmaya if any
            uninstall(frmaya = True)

            # FrMaya script folder path
            script_folder = os.path.join(usd, 'FrMaya')

            # copy frmaya to usd
            shutil.copytree(kwargs.get('source'), script_folder)

            # userSetup.py path
            file_path = os.path.join(usd, 'userSetup.py')

            script_file = ''

            # check if userSetup exist
            if os.path.exists(file_path):
                # TODO: append FrMaya userSetup to existing userSetup
                pass

            script_file += 'import FrMaya\n'
            script_file += 'FrMaya.startup()\n'

            with open(file_path, 'w') as ss:
                ss.write(script_file)

        if kwargs.get('source') and kwargs.get('remote'):
            # uninstall frmaya if any
            uninstall(frmaya = True)

            file_path = os.path.join(usd, 'userSetup.py')

            with open(file_path, 'w') as ss:
                ss.write("import sys\n")
                ss.write("sys.path.append(r'{0}')\n".format(os.path.dirname(kwargs.get('source'))))
                ss.write("import FrMaya\n")
                ss.write("FrMaya.startup()\n")

        return True
    else:
        print 'please specify keyword argument'
        return False


def uninstall(*args, **kwargs):
    # TODO: docstring here
    if kwargs:
        if kwargs.get('frmaya'):
            # Maya user script path
            usd = pm.internalVar(usd = True)
            # FrMaya script folder path
            script_folder = os.path.join(usd, 'FrMaya')

            if os.path.exists(script_folder):
                shutil.rmtree(script_folder, ignore_errors = True)

            # userSetup.py path
            file_path = os.path.join(usd, 'userSetup.py')

            if os.path.exists(file_path):
                os.remove(file_path)
