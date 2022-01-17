"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import pymel.core as pm

from . import general, scene


def bake_animation(input_object, translate = True, rotate = True, scale = False, time_range = None, hierarchy = True):
    """Bake animation specified PyNode object.
    
    :arg input_object: PyNode object need to bake the animation.
    :type input_object: pm.PyNode
    :key translate: If True, all translate attributes will get bake animation.
    :type translate: bool
    :key rotate: If True, all rotate attributes will get bake animation.
    :type rotate: bool 
    :key scale: If True, all scale attributes will get bake animation.
    :type scale: bool
    :key time_range: Specified start and end frame of bake animation.
     Default using current scene start and end frame.
    :type time_range: list of int 
    :key hierarchy: If True, all children of specified PyNode object will get bake animation.
    :type hierarchy: bool
    """
    if time_range is None:
        time_range = [scene.get_start_frame(), scene.get_end_frame()]
    if hierarchy:
        hi_format = 'below'
    else:
        hi_format = 'none'
    attr_list = []
    if translate:
        attr_list.extend(['tx', 'ty', 'tz'])
    if rotate:
        attr_list.extend(['rx', 'ry', 'rz'])
    if scale:
        attr_list.extend(['sx', 'sy', 'sz'])

    # pause viewport maya
    pm.general.refresh(suspend = True)
    # format time range
    timerange_format = '{}:{}'.format(time_range[0], time_range[1])
    # bake keys
    pm.bakeResults(
        input_object, simulation = True, t = timerange_format, hi = hi_format,
        at = attr_list, sampleBy = 1, oversamplingRate = 1,
        disableImplicitControl = True, preserveOutsideKeys = False, sparseAnimCurveBake = False,
        removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False,
        minimizeRotation = True, controlPoints = False, shape = False
    )
    # end of pause viewport maya
    pm.general.refresh(suspend = False)


def copy_animation(source_object, target_objects, attr_name_list = None, relative = False):
    """Copy animation from single source to multiple target.

    :arg source_object: PyNode object copy animation source.
    :type source_object: pm.PyNode
    :arg target_objects: PyNodes object copy animation destination.
    :type target_objects: list of pm.PyNode
    :key attr_name_list: Attributes name need to copy the animation.
     Default is using all visible attributes in channelbox.
    :type attr_name_list: list of str
    :key relative: If True, target object will keep the initial attribute value.
    :type relative: bool
    """
    if attr_name_list is None:
        attr_name_list = []

    if len(attr_name_list) > 0:
        attr_name_list = [attr_name for attr_name in attr_name_list if source_object.hasAttr(attr_name)]
    else:
        attr_name_list = [attr_node.attrName() for attr_node in general.get_channelbox_attributes(source_object)]

    for attr_name in attr_name_list:
        # If attribute doesnt have anim key, skip it
        keyframe_count = pm.keyframe(source_object, attribute = attr_name, q = True, keyframeCount = True)
        if not keyframe_count:
            continue

        pm.copyKey(source_object, attribute = attr_name)

        paste_key_data = {
            'attribute': attr_name,
            'clipboard': 'anim',
            'option': 'replaceCompletely'
        }
        if relative:
            # calculate offset value before paste the key
            src_val = source_object.attr(attr_name).get()
            for tgt_obj in target_objects:
                tgt_val = tgt_obj.attr(attr_name).get()
                offset_value = tgt_val - src_val
                paste_key_data['valueOffset'] = offset_value

                pm.pasteKey(tgt_obj, **paste_key_data)
        else:
            pm.pasteKey(target_objects, **paste_key_data)






