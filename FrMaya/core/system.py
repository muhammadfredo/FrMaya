"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 31 Agt 2020
Info         :

"""
import os
import shutil

import pymel.core as pm
from FrMaya.vendor import path


def __get_environ_path(environ_key):
    """Collect path from given environment key."""
    environ_value = os.environ.get(environ_key)

    if not environ_value:
        return []

    environ_path_list = environ_value.split(';')
    return [path.Path(o) for o in environ_path_list if os.path.exists(o)]


def get_menubar_path():
    """Collect menubar path from FR_MYMENUBAR environment."""
    return __get_environ_path('FR_MYMENUBAR')


def get_control_curve_path():
    """Collect control curve path from FR_CONTROLCURVE environment."""
    return __get_environ_path('FR_CONTROLCURVE')


def maya_version_as_float():
    # TODO: docstring here
    version = 2012.0
    if pm.about(version = True) == '2016 Extension 2':
        return 2016.5
    try:
        return pm.mel.getApplicationVersionAsFloat()
    except Exception as e:
        version_string = pm.about(version = True)
        temp_string = version_string.split()[0]
        return float(temp_string)


def install(*args, **kwargs):
    # TODO: docstring here
    # FIXME: some homework need to be done
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
    # FIXME: some homework need to be done
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


