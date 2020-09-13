"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jul 2017
Purpose      :

"""
import collections

import pymel.core as pm
from FrMaya.vendor import path

import FrMaya.utility as util
from .. import general


def keylockhide_attribute(pynodes, attributes_string, keyable = None, lock = None, hide = None):
    """
    Make attribute keyable or not, lock or unlock, and hide or unhide

    :param pynodes: list of pynode
    :param attributes_string: List of attribute as string, ex => [ 'translateX', 'scaleZ' ]
    :param keyable: None = Ignore; True or False
    :param lock: None = Ignore; True or False
    :param hide: None = Ignore; True or False
    """

    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # TODO: change this to more 'PyNode' way
    # Loop through list of attribute string
    for o in attributes_string:
        # Loop through list of pynode
        for x in pynodes:
            # Set attribute as PyNode object 
            att_node = pm.PyNode('{0}.{1}'.format(x.nodeName(), o))

            # Keyable or non keyable operation
            if keyable is not None:
                att_node.setKeyable(keyable)

                # Make sure attribute still showed in channel box
                if not keyable:
                    att_node.showInChannelBox(True)

            # Lock or unlock operation
            if lock is not None:
                att_node.setLocked(lock)

            # Hide or unhide operation
            if hide is not None:
                # Attribute still showed in channel box if it still keyable
                if hide:
                    att_node.setKeyable(False)
                    att_node.showInChannelBox(False)
                # Set keyable to true will show the attribute in channel box
                elif not hide:
                    att_node.setKeyable(True)


# return list of controller, and other data to use
def get_control_files(name = ''):
    """
    Get available control on control folder

    :return: list of all control file in PathNode object
    """

    # get FrRigging folder PathNode
    fr_rigging_folder = path.Path(__file__).parent
    # get control folder PathNode
    control_folder = fr_rigging_folder / 'control'

    control_files = control_folder.glob('*.json')
    if name:
        control_files = [o for o in control_files if o.filename == name]

    # return list of .mel file PathNode
    return control_files


def build_curve(data):
    curve = None
    for key, value in data.iteritems():
        degree = value.get('degree')
        periodic = value.get('periodic')
        point = value.get('point')
        knot = value.get('knot')

        # convert list to tuple
        point = [(o[0], o[1], o[2]) for o in point]

        curve = pm.curve(d = degree, per = periodic, p = point, k = knot)
    return curve


# att plan for below function, type of control, name, transform, color, group count
def create_control(control_file, transform = None, name = '', suffix = 'Ctl', color = None, group = None):
    if group is None:
        group = ['Grp']
    if transform is None:
        transform = pm.dt.Matrix()
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
    curve_control = build_curve(control_data)
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
