"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import pymel.core as pm

from . import scene_info


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


def copy_animation():
    # TODO: docstring here
    # FIXME: this is not ready function
    # FIXME: some homework need to be done
    att_list = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY', 'scaleZ']

    sel = pm.ls(os = 1)
    char_obj = None
    dummy_obj = None
    for i, o in enumerate(sel):
        res_num = i % 2
        # even number
        if res_num == 0:
            # dummy
            dummy_obj = o
        else:
            # odd number
            # character
            char_obj = o
        print 'odd or not', res_num
        print char_obj
        print dummy_obj

        if res_num == 1 and char_obj and dummy_obj:
            # snap char to dummy
            parent_cons = pm.parentConstraint(dummy_obj, char_obj, maintainOffset = False)
            pm.delete(parent_cons)

            # copy animation
            for x in att_list:
                dummy_att = dummy_obj.attr(x)
                anim_node = dummy_att.inputs()[0]

                anim_node.output >> char_obj.attr(x)






