"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 11 Sep 2020
Info         :

"""
import pymel.core as pm


def align(source, target, mode = 'transform'):
    """Align source PyNode to target PyNode.

    :arg source: PyNode object need to align.
    :type source: pm.nt.Transform
    :arg target: Destination of align operation.
    :type target: pm.nt.Transform
    :key mode: Transform, translate, rotate.
    :type mode: str
    """
    # Align translate from Red9 SnapRuntime plugin
    if mode == 'translate' or mode == 'transform':
        if type(target) == pm.MeshVertex:
            target_trans = target.getPosition(space = 'world')
        else:
            rot_piv_a = target.getRotatePivot(space = 'world')
            rot_piv_b = source.getRotatePivot(space = 'world')
            orig_trans = source.getTranslation(space = 'world')
            # We subtract the destinations translation from it's rotPivot, before adding it
            # to the source rotPiv. This compensates for offsets in the 2 nodes pivots
            target_trans = rot_piv_a + (orig_trans - rot_piv_b)

        # Translate align operation
        source.setTranslation(target_trans, space = 'world')
    if mode == 'rotate' or mode == 'transform':
        # Get rotation as quaternion
        rot_qt = target.getRotation(space = 'world', quaternion = True)
        source.setRotation(rot_qt, space = 'world')


def freeze_transform(pynodes, mode = 'Transform'):
    """Freeze translate, rotate, scale specified PyNodes.

    :arg pynodes: PyNodes object need to freeze transform.
    :type pynodes: list of pm.nt.Transform
    :key mode: Transform, translate, rotate, and scale.
    :type mode: str
    :rtype: bool
    """
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False
    # Initiate variable for makeIdentity command
    t = False
    r = False
    s = False
    if mode == 'translate' or mode == 'Transform':
        t = True
    if mode == 'rotate' or mode == 'Transform':
        r = True
    if mode == 'scale' or mode == 'Transform':
        s = True
    # Freeze transform command
    for o in pynodes:
        pm.makeIdentity(o, apply = True, translate = t, rotate = r, scale = s)

    return True


def reset_transform(pynodes, mode = ''):
    """Reset transform, visibility, or rotate order.

    :arg pynodes: PyNodes object need to reset transform.
    :type pynodes: list of pm.nt.Transform
    :arg mode: transform, translate, rotate, scale, visibility, and rotate_order. Default will reset all.
    :type mode: str
    :rtype: bool
    """
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return
    for o in pynodes:
        # Translate mode
        if mode == 'translate' or mode == 'transform' or mode == '':
            o.translateX.set(0)
            o.translateY.set(0)
            o.translateZ.set(0)
        # Rotate mode
        if mode == 'rotate' or mode == 'transform' or mode == '':
            o.rotateX.set(0)
            o.rotateY.set(0)
            o.rotateZ.set(0)
        # Scale mode
        if mode == 'scale' or mode == 'transform' or mode == '':
            o.scaleX.set(1)
            o.scaleY.set(1)
            o.scaleZ.set(1)
        # Visibility
        if mode == 'visibility' or mode == '':
            o.visibility.set(1)
        # Rotate order
        if mode == 'rotate_order' or mode == '':
            o.rotateOrder.set(0)

    return True



