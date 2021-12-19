"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 21 Nov 2021
Info         :

"""
import pymel.core as pm

import FrMaya.core as fmc


def create_expose_rotation(source_object, aim_axis = 'X', up_axis = 'Y', flip = False):
    """Create yaw, pitch, roll attributes to expose given object rotation.

    :arg source_object: PyNode object that need to extract its rotation.
    :type source_object: pm.nt.Transform
    :key aim_axis: Aim rotation axis, X, Y, or Z.
    :type aim_axis: str
    :key up_axis: Up rotation axis, X, Y, or Z.
    :type up_axis: str
    :key flip: If True the aim axis will be flipped.
    :type flip: bool
    :return: PyNode object with expose rotation attributes(yaw, pitch, roll).
    :rtype: pm.nt.Transform
    """
    axis_list = ['X', 'Y', 'Z']
    if aim_axis.upper() not in axis_list or up_axis not in axis_list:
        ValueError('Axis(aim and up) keyword argument accepted value "X", "Y", "Z".')
    multiply = -1 if flip else 1

    pitch_linear_axis = ''
    yaw_linear_axis = ''
    x = 0
    y = 0
    z = 0

    if aim_axis == 'X':
        pitch_linear_axis = up_axis
        yaw_linear_axis = 'Z' if up_axis == 'Y' else 'Y'
        x = 1
        y = 0
        z = 0
    elif aim_axis == 'Y':
        pitch_linear_axis = up_axis
        yaw_linear_axis = 'X' if up_axis == 'Z' else 'Z'
        x = 0
        y = 1
        z = 0
    elif aim_axis == 'Z':
        pitch_linear_axis = up_axis
        yaw_linear_axis = 'Y' if up_axis == 'X' else 'X'
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
    pmm_node.attr('inPoint{}'.format(aim_axis)).set(1 * multiply)

    expose_rot.attr('matrix') >> pmm_node.attr('inMatrix')
    pmm_node.attr('output{}'.format(pitch_linear_axis)) >> expose_rot.attr('pitchLinear')

    bw_node = pm.createNode('blendWeighted', n = '{}_bw'.format(source_object), ss = True)
    bw_node.setAttr('weight[0]', -1)
    pmm_node.attr('output{}'.format(yaw_linear_axis)) >> bw_node.attr('input[0]')
    bw_node.attr('output') >> expose_rot.attr('yawLinear')

    ac_node = pm.createNode('aimConstraint', n = '{}_AC'.format(source_object), ss = True)
    ac_node.attr('target[0].{0}.{0}{1}'.format('targetTranslate', aim_axis)).set(1 * multiply)
    ac_node.attr('worldUpType').set(4)
    ac_node.attr('aimVector').set([x * multiply, y * multiply, z * multiply])
    ac_node.attr('upVector').set([y * multiply, z * multiply, x * multiply])

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
    expression_script += 'vector $vecB = <<{},{},{}>>;\n'.format(*[o * multiply for o in [x, y, z]])
    expression_script += 'vector $vecJ = <<{},{},{}>>;\n'.format(*pmm_node.output.children())
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


def create_spline_ik_rig(joint_guides):
    # wip
    if not isinstance(joint_guides, list):
        raise ValueError('joint_guides argument should be list of joint')

    test_data = {
        'curve': {
            'degree': 1,
            'point': [],
            'knot': []
        }
    }
    for i, each in enumerate(joint_guides):
        curve_point = each.getTranslation(space = 'world').tolist()
        test_data['curve']['point'].append(curve_point)
        # test_data['curve']['knot'].append(float(i+1))
    # test_data['curve']['knot'].extend([0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.0, 8.0])
    test_data['curve']['knot'].extend([0.0, 8.0])

    print test_data
    fmc.build_curve(test_data)


def create_matrix_cons(source, target, space = 'world', maintain_offset = True):
    """Create matrix based constraint.

    :arg source: PyNode object source of the matrix constraint transformation.
    :type source: pm.nt.Transform or pm.nt.Joint
    :arg target: PyNode object that will get constrainted.
    :type target: pm.nt.Transform or pm.nt.Joint
    :key space: 'world' calculate based on source world space. 'local' calculate on source local space.
    :type space: str
    :key maintain_offset: If True, target will keep the transformation as is. False, will match source transformation.
    :type maintain_offset: bool
    :return: All node that used in matrix constraint.
    :rtype: list
    """
    multi_mtx = pm.createNode('multMatrix', ss = True)
    decom_mtx = pm.createNode('decomposeMatrix', ss = True)
    result = [multi_mtx, decom_mtx]
    multi_mtx.attr('matrixSum') >> decom_mtx.attr('inputMatrix')

    if space == 'local':
        offset_val = fmc.get_offset_matrix(target, target.getParent())
        parent_space_node = source
        idx_order = [2, 0, 1]
    else:
        offset_val = fmc.get_offset_matrix(target, source)
        parent_space_node = target
        idx_order = [0, 1, 2]

    if maintain_offset:
        multi_mtx.attr('matrixIn')[idx_order[0]].set(offset_val)

    source.attr('worldMatrix[0]') >> multi_mtx.attr('matrixIn')[idx_order[1]]
    parent_space_node.attr('parentInverseMatrix') >> multi_mtx.attr('matrixIn')[idx_order[2]]

    decom_mtx.attr('outputTranslate') >> target.attr('translate')
    if target.nodeType() == 'joint':
        eul_quat = pm.createNode('eulerToQuat', ss = True)
        quat_inv = pm.createNode('quatInvert', ss = True)
        quat_prod = pm.createNode('quatProd', ss = True)
        quat_eul = pm.createNode('quatToEuler', ss = True)
        result.extend([eul_quat, quat_inv, quat_prod, quat_eul])

        target.attr('jointOrient') >> eul_quat.attr('inputRotate')
        eul_quat.attr('outputQuat') >> quat_inv.attr('inputQuat')
        decom_mtx.attr('outputQuat') >> quat_prod.attr('input1Quat')
        quat_inv.attr('outputQuat') >> quat_prod.attr('input2Quat')
        quat_prod.attr('outputQuat') >> quat_eul.attr('inputQuat')
        quat_eul.attr('outputRotate') >> target.attr('rotate')
    else:
        decom_mtx.attr('outputRotate') >> target.attr('rotate')
    decom_mtx.attr('outputScale') >> target.attr('scale')

    return result
