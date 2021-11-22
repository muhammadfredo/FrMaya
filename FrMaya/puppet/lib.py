"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 21 Nov 2021
Info         :

"""
import pymel.core as pm

import FrMaya.core as fmc


def create_expose_rotation(source_object, aim_axis = 'X', up = 'Y', mult = 1):
    axis_list = ['X', 'Y', 'Z']
    if aim_axis not in axis_list or up not in axis_list:
        ValueError('Axis(aim and up) keyword argument accepted value "X", "Y", "Z".')

    pitch_linear_axis = ''
    yaw_linear_axis = ''
    x = 0
    y = 0
    z = 0

    if aim_axis == 'X':
        pitch_linear_axis = up
        yaw_linear_axis = 'Z' if up == 'Y' else 'Y'
        x = 1
        y = 0
        z = 0
    elif aim_axis == 'Y':
        pitch_linear_axis = up
        yaw_linear_axis = 'X' if up == 'Z' else 'Z'
        x = 0
        y = 1
        z = 0
    elif aim_axis == 'Z':
        pitch_linear_axis = up
        yaw_linear_axis = 'Y' if up == 'X' else 'X'
        x = 0
        y = 0
        z = 1

    for attr_name in ['yaw', 'pitch', 'roll']:
        source_object.addAttr(attr_name, at = 'doubleAngle', k = True)

    expose_rot_name = '{}_exposeRot'.format(source_object.nodeName())
    expose_rot = pm.createNode('transform', n = expose_rot_name, ss = True)
    for attr_name in ['yawLinear', 'pitchLinear', 'yaw', 'pitch', 'roll']:
        attr_type = 'doubleAngle' if attr_name == 'roll' else 'double'
        expose_rot.addAttr(attr_name, at = attr_type, k = True, h = True)

    source_object.attr('rotateX') >> expose_rot.attr('rotateX')
    source_object.attr('rotateY') >> expose_rot.attr('rotateY')
    source_object.attr('rotateZ') >> expose_rot.attr('rotateZ')
    source_object.attr('rotateOrder') >> expose_rot.attr('rotateOrder')
    expose_rot.attr('roll') >> source_object.attr('roll')

    pmm_node = pm.createNode('pointMatrixMult', n = '{}_pmm'.format(source_object), ss = True)
    pmm_node.attr('inPoint{}'.format(aim_axis)).set(1 * mult)

    expose_rot.attr('matrix') >> pmm_node.attr('inMatrix')
    pmm_node.attr('output{}'.format(pitch_linear_axis)) >> expose_rot.attr('pitchLinear')

    bw_node = pm.createNode('blendWeighted', n = '{}_bw'.format(source_object), ss = True)
    bw_node.setAttr('weight[0]', -1)
    pmm_node.attr('output{}'.format(yaw_linear_axis)) >> bw_node.attr('input[0]')
    bw_node.attr('output') >> expose_rot.attr('yawLinear')

    ac_node = pm.createNode('aimConstraint', n = '{}_AC'.format(source_object), ss = True)
    ac_node.attr('target[0].{0}.{0}{1}'.format('targetTranslate', aim_axis)).set(1 * mult)
    ac_node.attr('worldUpType').set(4)
    ac_node.attr('aimVector').set([x * mult, y * mult, z * mult])
    ac_node.attr('upVector').set([y * mult, z * mult, x * mult])

    expose_rot.attr('matrix') >> ac_node.attr('target[0].targetParentMatrix')
    expose_rot.attr('rotateOrder') >> ac_node.attr('constraintRotateOrder')

    oc_node = pm.createNode('orientConstraint', n = '{}_OC'.format(source_object), ss = True)
    oc_node.attr('interpType').set(0)

    expose_rot.attr('rotateX') >> oc_node.attr('target[0].{0}.{0}X'.format('targetRotate'))
    expose_rot.attr('rotateY') >> oc_node.attr('target[0].{0}.{0}Y'.format('targetRotate'))
    expose_rot.attr('rotateZ') >> oc_node.attr('target[0].{0}.{0}Z'.format('targetRotate'))
    expose_rot.attr('rotateOrder') >> oc_node.attr('constraintRotateOrder')
    expose_rot.attr('rotateOrder') >> oc_node.attr('target[0].targetRotateOrder')
    ac_node.attr('constraintRotateX') >> oc_node.attr('constraintJointOrientX')
    ac_node.attr('constraintRotateY') >> oc_node.attr('constraintJointOrientY')
    ac_node.attr('constraintRotateZ') >> oc_node.attr('constraintJointOrientZ')
    oc_node.attr('constraintRotate{}'.format(aim_axis)) >> expose_rot.attr('roll')

    yaw_uc_node = pm.createNode('unitConversion', n = '{}_yaw_UC'.format(source_object), ss = True)
    pitch_uc_node = pm.createNode('unitConversion', n = '{}_pitch_UC'.format(source_object), ss = True)
    expose_rot.attr('yaw') >> yaw_uc_node.attr('input')
    expose_rot.attr('pitch') >> pitch_uc_node.attr('input')
    yaw_uc_node.attr('output') >> source_object.attr('yaw')
    pitch_uc_node.attr('output') >> source_object.attr('pitch')

    # EXPRESSION
    expression_script = ''
    expression_script += 'vector $vecB = <<{},{},{}>>;\n'.format(*[o * mult for o in [x, y, z]])
    expression_script += 'vector $vecJ = <<{},{},{}>>;\n'.format(*pmm_node.output.get())
    expression_script += 'float $bendAngle = acos(clamp(-1.0, 1.0, dot($vecB, $vecJ)));\n'
    expression_script += 'float $yaw = asin(clamp(-1.0, 1.0, {}.yawLinear));\n'.format(expose_rot.nodeName())
    expression_script += 'float $pitch = asin({}.pitchLinear);\n'.format(expose_rot.nodeName())
    expression_script += 'float $sumAngle = abs($yaw) + abs($pitch);\n\n'
    expression_script += 'if($sumAngle > 1.0e-07)\n'
    expression_script += '{\n'
    expression_script += '\t{}.yaw = $bendAngle * $yaw / $sumAngle;\n'.format(expose_rot)
    expression_script += '\t{}.pitch = $bendAngle * $pitch / $sumAngle;\n'.format(expose_rot)
    expression_script += '}\n'
    expression_script += 'else\n'
    expression_script += '{\n'
    expression_script += '\t{}.yaw = $bendAngle;\n'.format(expose_rot)
    expression_script += '\t{}.pitch = 0.0;\n'.format(expose_rot)
    expression_script += '}'
    expression_node = pm.expression(
        s = expression_script, o = '', uc = 'all', n = '{}_EXP'.format(source_object), ae = 1
    )

    for n in [expose_rot, pmm_node, bw_node, oc_node, ac_node, expression_node]:
        if n.hasAttr('ihi'):
            n.attr('ihi').set(0)
        if n.hasAttr('intermediateObject'):
            n.attr('intermediateObject').set(True)

        attr_list = ['intermediateObject']
        attr_list.extend([o.attrName() for o in fmc.get_channelbox_attributes(n)])

        fmc.lock_attributes(n, attr_name_list = attr_list + ['ihi'])
        fmc.nonkeyable_attributes(n, attr_name_list = attr_list)
        fmc.hide_attributes(n, attr_name_list = attr_list)

    expose_rot.setParent(source_object, r = True)
    ac_node.setParent(expose_rot, r = True)
    oc_node.setParent(expose_rot, r = True)

    return expose_rot
