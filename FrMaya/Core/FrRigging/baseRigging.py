'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jul 2017
Purpose      : 

'''
import copy
import collections

import pymel.core as pm
from FrMaya.vendor import path

from FrMaya.Core import FrMath as frmath


def pgroup( pynodes, world = False, re = "", suffix = "" ):
    '''
    Create pgroup on supplied pynode
    
    :param pynodes: List of pynode
    :param world: Position of group in world pos or object pos, True or False value
    :param re: Find and replace input pynode name
    :param suffix: Suffix to add to pynode name
    '''
    
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False

    # Initiate return variable
    output = []
    
    # Group created on each object transformation
    if not world:
        for o in pynodes:
            # Name var
            theName = o.name()
            
            # Replace object name if any
            if re != "":
                theName = theName.replace( re, suffix )
            else:
                theName = theName + suffix
            
            # Create group for each supplied object
            grp = pm.group( empty = True, name = theName )
            
            # Snap the group to each object transformation
            alignMath( grp, o, mode = 'transform' )
            
            # Get object parent
            parent = o.getParent()
            
            # If the object have parent,
            # Parent the group to object parent 
            if parent:
                grp.setParent( parent )
            
            # Parent the object to Group
            o.setParent( grp )
            # Collect group to output
            output.append(grp)
    
    else:
        # Name var
        theName = pynodes[0].name()
        
        # Replace object name if any
        if re != "":
            theName = theName.replace( re, suffix )
        else:
            theName = theName + suffix
        
        # Create single group
        grp = pm.group( empty = True, name = theName )
        
        # Collect group to output
        output.append( grp )
        
        # Loop through all supplied object and parent it to group
        for o in pynodes:
            o.setParent( grp )
        
    return output

def align( orig, target, mode = 'transform' ):
    '''
    Align from orig pynode to target pynode using contraint method
    
    :param pynodes: List of pynode, count total 2
    :param mode: transform, translate, rotate
    '''
    
    # Snap position
    if mode == 'translate' or mode == 'transform':
        # Snap position of orig node to target node using constraint
        cons = pm.pointConstraint( target, orig, maintainOffset = False )
        # Delete the constraint
        pm.delete( cons )
    
    # Snap rotation
    if mode == 'rotate' or mode == 'transform':
        # Snap rotation of orig node to target node using constraint
        cons = pm.orientConstraint( target, orig, maintainOffset = False )
        # Delete the constraint
        pm.delete( cons )

def freezeTransform( pynodes, mode = 'transform' ):
    '''
    Freeze transform, translate, rotate, scale all supplied pynode
    depend on the mode
    
    :param pynodes: List of pynode
    :param mode: transform, translate, rotate, scale
    '''
    
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False
    
    # Initiate variable for makeIdentity command
    t = False; r = False; s = False
    
    # Translate mode
    if mode == 'translate' or mode == 'transform':
        t = True
    # Rotate mode
    if mode == 'rotate' or mode == 'transform':
        r = True
    # Scale mode
    if mode == 'scale' or mode == 'transform':
        s = True
    
    # Freeze transform command
    for o in pynodes:
        pm.makeIdentity( o, apply = True, translate = t, rotate = r, scale = s )

def zerooutTransform( pynodes, mode = 'transform' ):
    '''
    Zero out transform, visibility, and rotate order
    
    :param pynodes: list of pynode
    :param mode: transform, translate, rotate, scale, visibility, rotateorder
    '''
    
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False
    
    for o in pynodes:
        # Translate mode
        if mode == 'translate' or mode == 'transform':
            o.translateX.set(0)
            o.translateY.set(0)
            o.translateZ.set(0)
        # Rotate mode
        if mode == 'rotate' or mode == 'transform':
            o.rotateX.set(0)
            o.rotateY.set(0)
            o.rotateZ.set(0)
        # Scale mode
        if mode == 'scale' or mode == 'transform':
            o.scaleX.set(1)
            o.scaleY.set(1)
            o.scaleZ.set(1)
        # Visibility
        if mode == 'visibility':
            o.visibility.set(1)
        # Rotate order
        if mode == 'rotateorder':
            o.rotateOrder.set(0)

def keylockhideAttribute( pynodes, attributesString, keyable = None, lock = None, hide = None ):
    '''
    Make attribute keyable or not, lock or unlock, and hide or unhide
    
    :param pynodes: list of pynode
    :param attributesString: List of attribute as string, ex => [ 'translateX', 'scaleZ' ]
    :param keyable: None = Ignore; True or False
    :param lock: None = Ignore; True or False
    :param hide: None = Ignore; True or False
    '''
    
    # Filter supplied pynodes, if equal to 0 then return false
    if len(pynodes) == 0:
        return False
    
    # TODO: change this to more 'PyNode' way
    # Loop through list of attribute string
    for o in attributesString:
        # Loop through list of pynode
        for x in pynodes:
            # Set attribute as PyNode object 
            attNode = pm.PyNode( '{0}.{1}'.format( x.nodeName(), o ) )
            
            # Keyable or non keyable operation
            if not keyable == None:
                attNode.setKeyable( keyable )
                
                # Make sure attribute still showed in channelbox
                if not keyable:
                    attNode.showInChannelBox( True )
            
            # Lock or unlock operation
            if not lock == None:
                attNode.setLocked( lock )
            
            # Hide or unhide operation
            if not hide == None:
                # Attribute still showed in channelbox if it still keyable
                if hide:
                    attNode.setKeyable( False )
                    attNode.showInChannelBox( False )
                # Set keyable to true will show the attribute in channelbox
                elif not hide:
                    attNode.setKeyable( True )

def alignMath( orig, target, mode = 'transform' ):
    '''
    Align from orig pynode to target pynode using math element ( matrix, quaternion, vector, etc)

    :param orig: PyNode which will get transform applied
    :param target: The destination of alignMath operation
    :param mode: transform, translate, rotate
    '''
    
    # I got this align translate and some rotation algoritm
    # from Red9 SnapRuntime plugin
    
    # Align translate
    if mode == 'translate' or mode == 'transform':
        try:
            rotPivA = target.getRotatePivot( space = 'world' )
            rotPivB = orig.getRotatePivot( space = 'world' )
            origTrans = orig.getTranslation( space = 'world' )
            # We subtract the destinations translation from it's rotPivot, before adding it
            # to the source rotPiv. This compensates for offsets in the 2 nodes pivots
            targetTrans = rotPivA + ( origTrans - rotPivB )
        except:
            if type(target) == pm.MeshVertex:
                targetTrans = target.getPosition(space = 'world')
        
        # Translate align operation
        orig.setTranslation( targetTrans, space = 'world' )
    
    # Align rotation
    if mode == 'rotate' or mode == 'transform':
        # Create Quaternion object from target PyNode
        Quat = frmath.Quaternion( target.getRotation( space = 'world', quaternion = True ) )
        # orig.setRotation( Quat, space = 'world' )

        # Maybe we should use MyMatrix object in the future for the sake of math XD
        pm.xform( orig, ro = Quat.toEulerian().asList(), eu = True, ws = True )

def jointSplit( pynode, split = 2, replace = True ):
    '''
    Split joint from given parameter

    :param pynode: A single joint PyNode
    :param split: Number, how many split the joint will be splited
    :param replace: Bool value, new chain of splited joint or replace the input joint
    :return: list of splited joint
    '''

    # TODO: naming not yet implement, wait until we build modular auto rigging
    # init output data
    output = []
    # check if there is any selection, and store it
    sel = pm.ls( os = True )
    # make sure this is joint
    # if isinstance( pynode, pm.nodetypes.Joint ) and pynode.type() == 'joint' and len( pynode.getChildren() ) > 0 and split > 1:
    if pynode.type() == 'joint' and len( pynode.getChildren() ) > 0 and split > 1:
        # clear selection
        pm.select( clear = True )
        # get first child
        firstChild = pynode.getChildren()[0]
        # get vector
        vecA = frmath.Vector( pynode.getTranslation( space = 'world' ) )
        vecB = frmath.Vector( firstChild.getTranslation( space = 'world' ) )

        parent = pynode
        if not replace:
            jnt = pm.createNode('joint')
            alignMath(jnt, pynode)
            parent = jnt
            output.append(parent)

        factor = (vecB - vecA) / split
        for i in range(split-1):
            jnt = pm.createNode('joint')
            pos = factor * ( i + 1 ) + vecA

            # set splited joint translate
            jnt.setTranslation( pos.asList() )
            # set splited joint rotation
            alignMath( jnt, pynode, mode = 'rotate' )

            # set parent splited joint
            jnt.setParent( parent )
            # clean transformation on joint
            freezeTransform( [jnt] )

            # append newly created split joint to output
            output.append( jnt )
            # set new variable parent
            parent = jnt

        if not replace:
            jnt = pm.createNode('joint')
            alignMath(jnt, firstChild)
            jnt.setParent( parent )
            output.append(jnt)
        else:
            firstChild.setParent( parent )

        # reselect selection if any
        pm.select( sel )

    return output

def cometJoint_orient( pynodes, aimAxis = [ 1, 0, 0 ], upAxis = [ 0, 0, 1 ], upDir = [ 1, 0, 0 ], doAuto = False ):
    # Filter supplied pynodes, if equal to 0 then return false
    if len( pynodes ) == 0:
        return False

    # make sure only joint get passed through here
    pynodes = pm.ls( pynodes, type = 'joint' )

    # init variable prevUp for later use
    prevUp = frmath.Vector()

    for i, o in enumerate(pynodes):
        # first we need to unparent everthing and then store that,
        childs = o.getChildren()
        for x in childs:
            x.setParent(None)

        # find parent for later in case we need it
        parent = o.getParent()

        # Now if we have a child joint... aim to that
        try:
            aimTgt = pm.ls( childs, type='joint' )[0]
        except:
            aimTgt = None

        if aimTgt:
            # init variable upVec using upDir variable
            upVec = frmath.Vector( upDir )

            # first off... if doAuto is on, we need to guess the cross axis dir
            if doAuto:
                # now since the first joint we want to match the second orientation
                # we kind of hack the things passed in if it is the first joint
                # ie: if the joint doesnt have a parent... or if the parent it has
                # has the 'same' position as itself... then we use the 'next' joints
                # as the up cross calculations
                jntVec = frmath.Vector( o.getRotatePivot( space = 'world' ) )
                if parent:
                    parentVec.setValue( parent.getRotatePivot( space = 'world' ) )
                else:
                    parentVec = copy.copy( jntVec )
                aimTgtVec = frmath.Vector( aimTgt.getRotatePivot( space = 'world' ) )

                # how close to we consider 'same'?
                tol = 0.0001

                vecCond = jntVec - parentVec
                posCond = [ abs(x) for x in vecCond.asList() ]
                if parent == None or posCond[0] <= tol and posCond[1] <= tol and posCond[2] <= tol:
                    # get aimChild
                    aimChilds = aimTgt.getChildren()
                    try:
                        aimChild = pm.ls( aimChilds, type = 'joint' )[0]
                    except:
                        aimChild = None

                    # get aimChild vector
                    if aimChild:
                        aimChildVec = frmath.Vector( aimChild.getRotatePivot( space = 'world' ) )
                    else:
                        aimChildVec = frmath.Vector()

                    # find the up vector using child vector of aim target
                    upVec = ( jntVec - aimTgtVec ).cross( aimChildVec - aimTgtVec )
                else:
                    # find the up vector using the parent vector
                    upVec = ( parentVec - jntVec ).cross( aimTgtVec - jntVec )

            # reorient the current joint
            aCons = pm.aimConstraint( aimTgt, o, aimVector = aimAxis, upVector = upAxis, worldUpVector = upVec.asList(), worldUpType = 'vector', weight = 1 )
            pm.delete(aCons)

            # now compare the up we used to the prev one
            curUp = frmath.Vector( upVec.asList() ).normal()
            # dot product for angle between... store for later
            dot = curUp.dot(prevUp)
            prevUp = frmath.Vector( upVec.asList() )

            if i > 0 and dot <= 0:
                # adjust the rotation axis 180 if it looks like we have flopped the wrong way!
                # TODO: fix here
                # pm.xform( o, relative = True, objectSpace = True, rotateAxis = True )
                o.rotateX.set( o.rotateX.get() + ( aimAxis[0] * 180 ) )
                o.rotateY.set( o.rotateY.get() + ( aimAxis[1] * 180 ) )
                o.rotateZ.set( o.rotateZ.get() + ( aimAxis[2] * 180 ) )

                prevUp *= -1
        elif parent:
            # otherwise if there is no target, just dup orientation of parent...
            alignMath( o, parent, mode = 'rotate' )

        # and now finish clearing out joint axis ...
        pm.joint( o, e = True, zeroScaleOrient = True )
        freezeTransform( [ o ] )

        # now that we are done ... reparent
        if len(childs) > 0:
            for x in childs:
                x.setParent(o)

    return True
# return list of controller, and other data to use
def getControlFiles(name = ''):
    '''
    Get available control on control folder

    :return: list of all control file in PathNode object
    '''

    # get FrRigging folder PathNode
    FrRiggingFolder = path.Path(__file__).parent
    # get control folder PathNode
    controlFolder = FrRiggingFolder / 'control'

    controlFiles = controlFolder.glob('*.json')
    if name:
        controlFiles = [o for o in controlFiles if o.filename == name]

    # return list of .mel file PathNode
    return controlFiles

def buildCurve(data):
    for key, value in data.iteritems():
        degree = value.get('degree')
        periodic = value.get('periodic')
        point = value.get('point')
        knot = value.get('knot')

        # convert list to tupple
        point = [(o[0], o[1], o[2]) for o in point]

        curve = pm.curve(d = degree, per = periodic, p = point, k = knot)
    return curve

# att plan for below function, type of control, name, transform, color, group count
def createControl(filenode, transform = None, name = '', suffix = 'Ctl', color = None, group = ['Grp']):
    # check function attribute, and modify it if its on default mode
    # fill fullpath variable from filenode,
    # if filenode is name of control grab it from getControl
    try:
        controlpath = filenode.data
    except:
        try:
            controlfile = getControlFiles(filenode)[0]
            controlpath = controlfile.data
        except:
            return None
    # modify if name att on default
    if not name:
        name = 'FrControl'
    # add suffix to name
    name += '_' + suffix
    # modify if transform is None
    if not transform:
        transform = pm.dt.Matrix()

    # import control
    curveControl = buildCurve(controlpath)
    # grab transform of imported control
    # ctl = pm.ls(impNodes, type = 'transform')[0]

    # rename control
    curveControl.rename(name)
    # retransform control
    curveControl.setMatrix(transform, worldSpace = True)
    # pgroup the control
    resgrp = {}
    inputGrp = curveControl
    for o in group:
        resgrp[o] = pgroup([inputGrp], re = suffix, suffix = o)[0]
        inputGrp = resgrp[o]
        suffix = o

    # create control tuple class
    ControlTuple = collections.namedtuple('ControlTuple', 'control groupDict')
    # create instance of control tuple and assign the value
    result = ControlTuple(control = curveControl, groupDict = resgrp)

    return result

