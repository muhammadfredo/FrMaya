"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import pymel.core as pm

from . import general, scene_info


def bake_animation(input_node):
    """
    """
    # TODO: docstring here
    # FIXME: some homework need to be done
    # pause viewport maya
    pm.general.refresh(suspend = True)
    # format time range
    timerange = '{}:{}'.format(scene_info.get_start_frame(), scene_info.get_end_frame())
    # bake keys
    pm.bakeResults(input_node, simulation = True, t = timerange, hi = 'below',
                   at = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'],
                   sampleBy = 1, oversamplingRate = 1,
                   disableImplicitControl = True, preserveOutsideKeys = False, sparseAnimCurveBake = False,
                   removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False,
                   minimizeRotation = True, controlPoints = False, shape = False)
    # end of pause viewport maya
    pm.general.refresh(suspend = False)


def copy_animation(source_object, target_objects, attr_name_list = None, relative = False):
    """Copy animation from single source to multiple target.

    :arg source_object: PyNode object copy animation source.
    :type source_object: pm.PyNode
    :arg target_objects: PyNodes object copy animation destination.
    :type target_objects: list of pm.PyNode
    :key attr_name_list: Attributes name need to copy the animation.
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






