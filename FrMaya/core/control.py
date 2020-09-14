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


# return list of controller, and other data to use
def get_control_files(name = ''):
    """
    Get available control on control folder
    # TODO: docstring here
    :return: list of all control file in PathNode object
    """
    # get control folder PathNode
    control_dir_list = system.get_control_curve_path()

    control_files = [control_dir.glob('*.json') for control_dir in control_dir_list]
    control_files = util.flatten(control_files)
    if name:
        control_files = [o for o in control_files if o.filename == name]

    # return list of .mel file PathNode
    return control_files


# att plan for below function, type of control, name, transform, color, group count
def create_control(control_file, transform = pm.dt.Matrix(), name = '', suffix = 'Ctl', color = None, group = None):
    # TODO: docstring here
    if group is None:
        group = ['Grp']
    # check function attribute, and modify it if its on default mode
    # fill full path variable from control_file,
    # if control_file is name of control grab it from getControl
    control_file_path = path.Path(control_file)
    if not control_file_path.exists():
        control_file_path = get_control_files(control_file)[0]
    # modify if name att on default
    if not name:
        name = 'FrControl'
    # add suffix to name
    name += '_' + suffix

    control_data = util.read_json(control_file_path)
    # import control
    curve_control = general.build_curve(control_data)
    # grab transform of imported control
    # ctl = pm.ls(impNodes, type = 'transform')[0]

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
    ControlTuple = collections.namedtuple('ControlTuple', 'control groupDict')
    # create instance of control tuple and assign the value
    result = ControlTuple(control = curve_control, groupDict = resgrp)

    return result




