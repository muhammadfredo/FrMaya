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
    """Return maya version as float.

    :rtype: float
    """
    if pm.about(version = True) == '2016 Extension 2':
        return 2016.5
    try:
        return pm.mel.getApplicationVersionAsFloat()
    except Exception as e:
        version_string = pm.about(version = True)
        temp_string = version_string.split()[0]
        return float(temp_string)


def install(source_path, local_install = False):
    # TODO: docstring here
    # FIXME: some homework need to be done
    source_path = path.Path(source_path)
    assert source_path.exists(), 'Source path did not exist!!!'
    installed_title = source_path.stem
    # Maya user application directory
    user_app_dir = path.Path(pm.internalVar(uad = True))
    # create modules dir
    module_dir = user_app_dir / 'modules'
    if not module_dir.exists():
        module_dir.mkdir()

    # uninstall first if any
    uninstall(installed_title)
    if local_install:
        # FrMaya script folder path
        target_dir = user_app_dir / installed_title
        # copy frmaya to user script directory
        shutil.copytree(source_path, target_dir)
    else:
        target_dir = source_path

    # write module file
    module_file = module_dir / '{}.mod'.format(installed_title)
    with open(module_file, 'w') as ss:
        ss.write('+ FrMaya any {}\n'.format(target_dir))
        ss.write('scripts+:=startup\n')
        ss.write('PYTHONPATH+:=\n')
        ss.write('PYTHONPATH+:=startup\n')
        ss.write('FR_MYMENUBAR+:=MayaMenubar\n')
        ss.write('FR_CONTROLCURVE+:=RigData\\ControlCurve\n')

    return True


def uninstall(installed_title):
    # TODO: docstring here
    # FIXME: some homework need to be done
    # Maya user application directory
    user_app_dir = path.Path(pm.internalVar(uad = True))
    # modules dir
    module_dir = user_app_dir / 'modules'
    module_file = module_dir / '{}.mod'.format(installed_title)
    if module_file.exists():
        module_file.remove()

    # installed package
    installed_pkg = user_app_dir / installed_title
    if installed_pkg.exists():
        shutil.rmtree(ignore_errors = True)


