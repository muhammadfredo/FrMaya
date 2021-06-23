"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 19 Apr 2021
Info         :

"""
import os
import re

import FrMaya.vendor.path as path
import pymel.core as pm

import FrMaya.utility as util


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
