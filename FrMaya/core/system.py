"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 31 Agt 2020
Info         :

"""
import os
import re
import shutil
import tempfile
import urllib2
import zipfile

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
    """Install FrMaya package.

    :arg source_path: Downloaded or cloned FrMaya package absolute path.
    :type source_path: str or path.Path
    :key local_install: If True, FrMaya package will be copied into maya user application directory.
    :type local_install: bool
    :rtype: bool
    """
    frmaya_content = ['FrMaya', 'MayaMenubar', 'RigData', 'startup', 'LICENSE.txt', 'README.md']
    source_path = path.Path(source_path).abspath()
    installed_title = source_path.name
    assert source_path.exists(), 'Source path did not exist!!!'
    assert installed_title, 'Package title not found!!!'
    for each in frmaya_content:
        sub_item = source_path / each
        assert sub_item.exists(), '{} did not exists, make sure its exists!!'.format(sub_item)

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
        # create FrMaya root dir
        if not target_dir.exists():
            target_dir.mkdir()
        # copy all sub content into target_dir
        for each in frmaya_content:
            src = source_path / each
            tgt = target_dir / each
            if src.isdir():
                shutil.copytree(src.abspath(), tgt.abspath())
            elif src.isfile():
                shutil.copy(src.abspath(), tgt.abspath())
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
    """Uninstall FrMaya package.

    :arg installed_title: FrMaya package title name.
    :type installed_title: str
    """
    assert installed_title, 'Package title not found!!!'
    assert installed_title != 'maya', '{} is not package!!'.format(installed_title)
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
        shutil.rmtree(installed_pkg, ignore_errors = True)


def get_server_version():
    """Get FrMaya version from github.

    :rtype: list of int
    """
    url_address = 'https://raw.githubusercontent.com/muhammadfredo/FrMaya/master/FrMaya/version.py'
    url_data = urllib2.urlopen(url_address).read(200)
    result = re.search(r'(\d+), (\d+), (\d+)', url_data, re.MULTILINE)
    if result:
        version_list = [int(v) for v in result.groups()]
        return version_list
    else:
        raise ValueError('Cannot get server version!!!')


def download_latest_version(target_name = '', target_dir = None):
    """Download latest FrMaya version from github.

    :key target_name: Zip or directory new downloaded data.
    :type target_name: str
    :key target_dir: Directory where the download will placed.
    :type target_dir: str or path.Path
    :return: FrMaya master zip and FrMaya extracted zip file.
    :rtype: tuple of str
    """
    url_address = 'https://github.com/muhammadfredo/FrMaya/archive/master.zip'
    if target_dir is None:
        temp_dir = path.Path(tempfile.gettempdir())
    else:
        temp_dir = path.Path(target_dir)
    temp_frmaya_zip = temp_dir / '{}.zip'.format(target_name)
    temp_frmaya_dir = temp_dir / target_name

    with open(temp_frmaya_zip, 'wb') as temp_zip:
        temp_zip.write(urllib2.urlopen(url_address).read())
    zipfile.ZipFile(temp_frmaya_zip).extractall(temp_frmaya_dir)

    return temp_frmaya_zip, temp_frmaya_dir


def check_local_package(installed_title):
    """Check installed package in Maya user application directory.

    :return: True if its exists, Falser otherwise
    :rtype: bool
    """
    user_app_dir = path.Path(pm.internalVar(uad = True))
    installed_dir = user_app_dir / installed_title

    if installed_dir.isfile():
        return False
    elif installed_dir.isdir():
        return True
    else:
        return False




