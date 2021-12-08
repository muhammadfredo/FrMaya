"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 11 Sep 2020
Info         :

"""
import pymel.core as pm


def align(source, target, mode = 'transform', align_trans = None):
    """Align source PyNode to target PyNode.

    :arg source: PyNode object need to align.
    :type source: pm.nt.Transform
    :arg target: Destination of align operation.
    :type target: pm.nt.Transform
    :key mode: transform, translate, rotate.
    :type mode: str
    :key align_trans: Align axis target. Default value is [1, 1, 1].
    :type align_trans: list of int
    """
    if align_trans is None:
        align_trans = [1, 1, 1]
    # Align translate from Red9 SnapRuntime plugin
    if mode == 'translate' or mode == 'transform':
        if type(target) == pm.MeshVertex:
            target_trans = target.getPosition(space = 'world')
        else:
            rot_piv_a = target.getRotatePivot(space = 'world')
            rot_piv_b = source.getRotatePivot(space = 'world')
            orig_trans = source.getTranslation(space = 'world')

            for i, o in enumerate(align_trans):
                rot_piv_a[i] = rot_piv_a[i] * o

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


def xform_mirror(source, across = 'YZ', behaviour = True):
    """Mirrors transform across hyperplane.
    Code based on https://gist.github.com/rondreas/1c6d4e5fc6535649780d5b65fc5a9283

    :arg source: PyNode object need to mirror.
    :type source: pm.nt.Transform
    :key across: Plane which to mirror across('XY', 'YZ', 'XZ').
    :type across: str
    :key behaviour: If False it use Orientation mode.
    :type behaviour: bool
    """
    # Validate plane which to mirror across,
    if across not in ['XY', 'YZ', 'XZ']:
        raise ValueError("Keyword Argument: 'across' not of accepted value ('XY', 'YZ', 'XZ').")

    # Get the worldspace matrix, as a list of 16 float values
    mtx = pm.xform(source, q = True, ws = True, m = True)

    # Invert rotation columns,
    rx = [n * -1 for n in mtx[0:9:4]]
    ry = [n * -1 for n in mtx[1:10:4]]
    rz = [n * -1 for n in mtx[2:11:4]]

    # Invert translation row,
    t = [n * -1 for n in mtx[12:15]]

    # Set matrix based on given plane, and whether to include behaviour or not.
    if across is 'XY':
        mtx[14] = t[2]  # set inverse of the Z translation

        # Set inverse of all rotation columns but for the one we've set translate to.
        if behaviour:
            mtx[0:9:4] = rx
            mtx[1:10:4] = ry

    elif across is 'YZ':
        mtx[12] = t[0]  # set inverse of the X translation

        if behaviour:
            mtx[1:10:4] = ry
            mtx[2:11:4] = rz
    else:
        mtx[13] = t[1]  # set inverse of the Y translation

        if behaviour:
            mtx[0:9:4] = rx
            mtx[2:11:4] = rz

    # Finally set matrix for source,
    pm.xform(source, ws = True, m = mtx)


def world_space_translate(source, offset_values, absolute = False):
    """Translate source PyNode in world space.

    :arg source: PyNode object need to offset.
    :type source: pm.nt.Transform
    :arg offset_values: Translation value offset.
    :type offset_values: list of float or list of int
    :key absolute: If False it translate relative to current position.
    :type absolute: bool
    """
    if len(offset_values) != 3:
        raise ValueError('Need list with length of 3')
    orig_trans = source.getTranslation(space = 'world')

    target_trans = offset_values
    if not absolute:
        target_trans += orig_trans
    # Translate align operation
    source.setTranslation(target_trans, space = 'world')


def get_offset_matrix(source, parent_offset):
    """Return offset matrix value from given nodes.

    :arg source: Offset matrix value will get extracted from this PyNode object.
    :type source: pm.PyNode
    :arg parent_offset: Parent space for calculating offset matrix.
    :type parent_offset: pm.PyNode
    :rtype: pm.dt.Matrix
    """
    return source.worldMatrix[0].get() * parent_offset.worldInverseMatrix[0].get()
