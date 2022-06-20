"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 31 Agt 2020
Info         :

alternative_callback_data: header data
  "id": (callback id)
    "event_name": "after_open"
    "callback_tag": fr_maya

maya_event_callbacks:
  after_open:
    event_id: event_id,
    add_callback: om callback function
  before_open:
    event_id: event_id,
    add_callback: om callback function

"""
import copy
import inspect
import os
import re
import shutil
import tempfile
import urllib2
import zipfile

import pymel.core as pm
from maya import OpenMaya as om

from FrMaya import utility as util
from FrMaya.vendor import path


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


# region FrMaya dir system
def __get_environ_path(environ_key):
    """Collect path from given environment key."""
    environ_value = os.environ.get(environ_key)
    result = []

    if not environ_value:
        return result

    environ_path_list = environ_value.split(';')
    for each_path in environ_path_list:
        each_path = path.Path(each_path)

        if not each_path.exists():
            continue

        # make sure default directory first in the order
        if 'FrMaya' in each_path:
            result.insert(0, each_path)
        else:
            result.append(each_path)

    return result


def get_menubar_path():
    """Collect menubar path from FR_MYMENUBAR environment."""
    return __get_environ_path('FR_MYMENUBAR')


def get_control_curve_path():
    """Collect control curve path from FR_CONTROLCURVE environment."""
    return __get_environ_path('FR_CONTROLCURVE')
# endregion


# region FrMaya package installation
def install(source_path, package_title = '', local_install = False):
    """Install FrMaya package.

    :arg source_path: Downloaded or cloned FrMaya package absolute path.
    :type source_path: str or path.Path
    :key package_title: Package name.
    :type package_title: str
    :key local_install: If True, FrMaya package will be copied into maya user application directory.
    :type local_install: bool
    :rtype: bool
    """
    frmaya_content = ['FrMaya', 'MayaMenubar', 'RigData', 'startup', 'LICENSE.txt', 'README.md']
    source_path = path.Path(source_path).abspath()
    if package_title:
        installed_title = package_title
    else:
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
        ss.write('MAYA_SCRIPT_PATH+:=startup\n')
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
    :rtype: tuple of path.Path
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

    return path.Path(temp_frmaya_zip).abspath(), path.Path(temp_frmaya_dir).abspath()


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
# endregion


# TODO: update to api 2.0 ??
# region Maya Callback
class MyCallbackManager(object):
    __metaclass__ = util.MetaSingleton

    @staticmethod
    def get_maya_event_callback():
        """
        Return dictionary data of Maya events callback.

        after_open:
            event_id: event_id,

            add_callback: open Maya callback function.
        before_open:
            event_id: event_id,

            add_callback: open Maya callback function.
        :rtype: dict
        """
        # example regex subs -> re.sub(r"(\w)([A-Z])", r"\1 \2", "WordWordWord")
        callback_events = {}
        re_pattern = re.compile(r'(?<=\w)([A-Z])')
        for event_name, event_id in inspect.getmembers(om.MSceneMessage):
            if event_name.startswith('k') and not event_name.endswith('check'):
                if not callback_events.get(event_name):
                    key_name = re_pattern.sub(r'_\1', event_name[1:])
                    callback_events[key_name.lower()] = {
                        'event_id': event_id,
                        'add_callback': om.MSceneMessage.addCallback,
                    }

        return callback_events

    def __init__(self):
        """Class to manage callback for FrMaya system."""
        print 'initialize callback manager'
        self._maya_event_callback = {}
        self._registered_callback = {}

        self._maya_event_callback = copy.deepcopy(self.get_maya_event_callback())

        assert len(self._maya_event_callback) > 0, ''

    def _group_registered_callbacks(self):
        """
        Return registered callbacks based on events or tags callback.

        events:
            event_name: [callback function name, ..],

        tags:
            callback_tag: [callback function name, ..],

        :rtype: dict
        """
        result_data = {'events': {}, 'tags': {}}
        for cb_fn_name, cb_data in self._registered_callback.items():
            for each in result_data:
                if each == 'events':
                    event_or_tag = cb_data['event_name']
                elif each == 'tags':
                    event_or_tag = cb_data['callback_tag']
                else:
                    return None

                if result_data[each].get(event_or_tag):
                    result_data[each][event_or_tag].append(cb_fn_name)
                else:
                    result_data[each][event_or_tag] = [cb_fn_name]
        return result_data

    def add_callback(self, event_name, callback_tag, func):
        """
        Return True if it success add callback to callback manager, False otherwise.

        :arg event_name: Maya event nice name.
        :type event_name: str
        :arg callback_tag: A tag to group callback in callback manager.
        :type callback_tag: str
        :arg func: Python function.
        :rtype: bool
        """
        my_event_cb = self._maya_event_callback.get(event_name)

        if my_event_cb:
            callback_id = my_event_cb['add_callback'](my_event_cb['event_id'], func)

            self._registered_callback[func.__module__] = {
                'event_name': event_name,
                'callback_tag': callback_tag,
                'callback_id': callback_id
            }

            return True
        else:
            return False

    def remove_callback(self, event_name = '', callback_tag = ''):
        """
        Remove callback based on specified keyword argument.
        If both keyword specified, it will performed both action.

        :key event_name: Maya event name callback which want to removed.
        :type event_name: str
        :key callback_tag: Callback tag which want to removed.
        :type callback_tag: str
        """
        callback_collection = self._group_registered_callbacks()

        cb_id_array = om.MCallbackIdArray()
        cb_fn_name_list = []
        if event_name:
            cb_fn_name_list.extend(callback_collection['events'].get(event_name, []))
        if callback_tag:
            cb_fn_name_list.extend(callback_collection['tags'].get(callback_tag, []))

        for cb_fn_name in cb_fn_name_list:
            cb_id_array.append(self._registered_callback[cb_fn_name]['callback_id'])

        if cb_id_array:
            om.MMessage.removeCallbacks(cb_id_array)

    def show_registered_callback(self, event_name = '', callback_tag = ''):
        """
        Return registered callback based on specified keyword,
        if both keyword did not specified, it will return both group data (event name and tag).

        :key event_name: Maya event name callback which callback group want to retrieved.
        :type event_name: str
        :key callback_tag: Callback tag which callback group want to retrieved.
        :type callback_tag: str
        :rtype: dict or list
        """
        result = self._group_registered_callbacks()

        if event_name:
            return result['events'].get(event_name, [])
        elif callback_tag:
            return result['tags'].get(callback_tag, [])
        else:
            return copy.deepcopy(result)

    def show_maya_event_name(self):
        """
        Return list of Maya event nice name.

        :rtype: list of str
        """
        return self._maya_event_callback.keys()
# endregion


# region Antivirus
def find_self_duplicate_script_nodes():
    """
    Collect harmful self duplicate script nodes in the scene.
    All script node that create/write files consider to be harmful by this function.

    :rtype: list of pm.nt.Script
    """
    regexp_py_write_files = re.compile(r'(with open\().*(\.write)', re.DOTALL)
    regexp_mel_write_files = re.compile(r'(fopen (\(|)\$\w+(\)|) (\(|)\"[wa]\"(\)|))', re.DOTALL)
    script_nodes = pm.ls(type = 'script')

    self_duplicator_nodes = []
    for each_node in script_nodes:
        # script node should not be able to write files!!!
        # mel
        mel_res_before = regexp_mel_write_files.search(each_node.before.get() or '')
        mel_res_after = regexp_mel_write_files.search(each_node.after.get() or '')
        # python
        py_res_before = regexp_py_write_files.search(each_node.before.get() or '')
        py_res_after = regexp_py_write_files.search(each_node.after.get() or '')

        if mel_res_before or mel_res_after or py_res_before or py_res_after:
            self_duplicator_nodes.append(each_node)
    return self_duplicator_nodes


def find_malware_script_job():
    """
    Collect all harmful script job ids in the scene.
    The Script job which consider to be harmful based on Autodesk scurity fix.

    :rtype: list of int
    """
    script_jobs = pm.scriptJob(listJobs = True)

    a = -1
    if pm.mel.whatIs('$autoUpdateAttrEd_aoto_int') != 'Unknown':
        a = int(pm.mel.eval('$temp=$autoUpdateAttrEd_aoto_int'))

    malware_ids = []
    for each_job in script_jobs:
        if each_job.startswith(str(a)):
            malware_ids.append(a)
        if 'leukocyte.antivirus()' in each_job:
            job_id = int(each_job.split(":")[0])
            malware_ids.append(job_id)
    return malware_ids


def clean_virus():
    """Delete all harmful script node and kill all harmful script job."""
    self_duplicator_nodes = find_self_duplicate_script_nodes()
    malware_script_job_ids = find_malware_script_job()

    # first kill the mel globals!
    virus_procs = [
        'UI_Mel_Configuration_think',
        'UI_Mel_Configuration_think_a',
        'UI_Mel_Configuration_think_b',
        'autoUpdateAttrEd_SelectSystem',
        'autoUpdatcAttrEd',
        'autoUpdatoAttrEnd'
    ]
    for each_proc in virus_procs:
        if pm.mel.whatIs(each_proc) == 'Mel procedure entered interactively.':
            pm.mel.eval('global proc {0}(){error -sl "attempted to run corrupted command: {0}";}'.format(each_proc))

    for each_node in self_duplicator_nodes:
        pm.delete(each_node)
    for each_id in malware_script_job_ids:
        pm.scriptJob(kill = each_id, force = True)


def find_malware_files():
    """
    Collect all  script files that breed the malware.

    :rtype: list of path.Path
    """
    maya_user_dir = path.Path(pm.internalVar(userAppDir = True))
    user_setup_mel = maya_user_dir / 'scripts' / 'userSetup.mel'
    user_setup_py = maya_user_dir / 'scripts' / 'userSetup.py'
    user_setup_mel_data = util.read_file_text(user_setup_mel) if user_setup_mel.exists() else ''
    user_setup_py_data = util.read_file_text(user_setup_py) if user_setup_py.exists() else ''
    vaccine_py = maya_user_dir / 'scripts' / 'vaccine.py'
    vaccine_pyc = maya_user_dir / 'scripts' / 'vaccine.pyc'

    malware_files = []
    if 'fuck_All_U' in user_setup_mel_data:
        malware_files.append(user_setup_mel)
    if 'leukocyte' in user_setup_py_data and 'vaccine' in user_setup_py_data:
        malware_files.append(user_setup_py)
    if os.path.exists(vaccine_py):
        malware_files.append(vaccine_py)
    if os.path.exists(vaccine_pyc):
        malware_files.append(vaccine_pyc)

    return malware_files


def clean_malware_files():
    """Delete all harmful malware script files."""
    malware_files = find_malware_files()

    for each_file in malware_files:
        try:
            os.remove(each_file)
        except:
            print 'Failed to remove ~> {}'.format(each_file)


def clean_outliner_command_script():
    outliner_panels = pm.getPanel(typ='outlinerPanel')
    dirty_commands = ['look']
    for each in outliner_panels:
        if pm.outlinerEditor(each.name(), q = True, selectCommand = True) in dirty_commands:
            pm.outlinerEditor(each.name(), e = True, selectCommand = '')
# endregion
