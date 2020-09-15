"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 13 Sep 2020
Info         :

"""
import collections

import pymel.core as pm
from FrMaya.vendor import path

import FrMaya.utility as util
from . import general
from . import system


def get_control_files(name = ''):
    """Collect all control files from all path in FR_CONTROLCURVE.

    :key name: If specified, only return control file of a specified name.
    :type name: str
    :rtype: list of path.Path
    """
    # get all control folder path
    control_dir_list = system.get_control_curve_path()
    # collect all control files and flatten it
    control_files = [control_dir.glob('*.json') for control_dir in control_dir_list]
    control_files = util.flatten(control_files)
    if name:
        control_files = [o for o in control_files if o.filename == name]

    return control_files


def create_control(control_file, transform = pm.dt.Matrix(), name = 'FrControl', suffix = 'Ctl', group = None):
    """Create control curve for FrMaya rig.

    :arg control_file: Control file absolute path or control file name.
    :type control_file: path.Path or str
    :key transform: Sets transformation of the newly-created control.
    :type transform: pm.dt.Matrix
    :key name: Sets the name of the newly-created control.
    :type name: str
    :key suffix: Add suffix to the name.
    :type suffix: str
    :key group: Sets group chain on newly-created control.
    :type group: list of str
    :return: ControlTuple(control = control_curve, group_data = group_dict_data)
    :rtype: (pm.nt.Transform, dict of pm.nt.Transform)
    """
    if group is None:
        group = ['Grp']
    # if control_file is file name of control grab it from get_control_files
    control_file_path = path.Path(control_file)
    if not control_file_path.exists():
        control_file_path = get_control_files(control_file)[0]
    # add suffix to name
    name += '_' + suffix
    # read control file
    control_data = util.read_json(control_file_path)
    # build control curve
    curve_control = general.build_curve(control_data)
    # rename control
    curve_control.rename(name)
    # retransform control
    curve_control.setMatrix(transform, worldSpace = True)
    # pgroup the control
    resgrp = {}
    input_grp = curve_control
    for o in group:
        resgrp[o] = general.pgroup([input_grp], re = suffix, suffix = o)[0]
        input_grp = resgrp[o]
        suffix = o
    # create control tuple class
    ControlTuple = collections.namedtuple('ControlTuple', 'control group_data')
    # create instance of control tuple and assign the value
    result = ControlTuple(control = curve_control, group_data = resgrp)

    return result




