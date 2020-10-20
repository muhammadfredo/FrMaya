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


def freeze_transform(pynode, mode = 'Transform'):
    """Freeze translate, rotate, scale specified PyNode.

    :arg pynode: PyNode object need to freeze transform.
    :type pynode: pm.nt.Transform
    :key mode: Transform, translate, rotate, and scale.
    :type mode: str
    :rtype: bool
    """
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
    pm.makeIdentity(pynode, apply = True, translate = t, rotate = r, scale = s)

    return True


def reset_transform(pynode, mode = ''):
    """Reset transform, visibility, or rotate order.

    :arg pynode: PyNode object need to reset transform.
    :type pynode: pm.nt.Transform
    :arg mode: transform, translate, rotate, scale, visibility, and rotate_order. Default will reset all.
    :type mode: str
    :rtype: bool
    """
    # Translate mode
    if mode == 'translate' or mode == 'transform' or mode == '':
        pynode.translateX.set(0)
        pynode.translateY.set(0)
        pynode.translateZ.set(0)
    # Rotate mode
    if mode == 'rotate' or mode == 'transform' or mode == '':
        pynode.rotateX.set(0)
        pynode.rotateY.set(0)
        pynode.rotateZ.set(0)
    # Scale mode
    if mode == 'scale' or mode == 'transform' or mode == '':
        pynode.scaleX.set(1)
        pynode.scaleY.set(1)
        pynode.scaleZ.set(1)
    # Visibility
    if mode == 'visibility' or mode == '':
        pynode.visibility.set(1)
    # Rotate order
    if mode == 'rotate_order' or mode == '':
        pynode.rotateOrder.set(0)

    return True



