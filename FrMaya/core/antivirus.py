"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 19 Apr 2021
Info         :

"""
import os
import re

import pymel.core as pm

import FrMaya.utility as util


# TODO: write docstring
def find_self_duplicate_script_nodes():
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
    maya_user_dir = pm.internalVar(userAppDir = True)
    user_setup_mel = os.path.join(maya_user_dir, 'scripts', 'userSetup.mel')
    user_setup_py = os.path.join(maya_user_dir, 'scripts', 'userSetup.py')
    user_setup_mel_data = util.read_file_text(user_setup_mel) if os.path.exists(user_setup_mel) else ''
    user_setup_py_data = util.read_file_text(user_setup_py) if os.path.exists(user_setup_py) else ''
    vaccine_py = os.path.join(maya_user_dir, 'scripts', 'vaccine.py')
    vaccine_pyc = os.path.join(maya_user_dir, 'scripts', 'vaccine.pyc')

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
    malware_files = find_malware_files()

    for each_file in malware_files:
        try:
            os.remove(each_file)
        except:
            print 'Failed to remove ~> {}'.format(each_file)
