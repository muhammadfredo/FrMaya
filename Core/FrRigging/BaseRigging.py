'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 22 Jul 2017
Purpose      : 

'''

from FrMaya.Core.FrMath import Rotation
from FrMaya.Core import FrMath as frmath
import pymel.core as pm

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
        rotPivA = target.getRotatePivot( space = 'world' )
        rotPivB = orig.getRotatePivot( space = 'world' )
        origTrans = orig.getTranslation( space = 'world' )
        # We subtract the destinations translation from it's rotPivot, before adding it
        # to the source rotPiv. This compensates for offsets in the 2 nodes pivots
        targetTrans = rotPivA + ( origTrans - rotPivB )
        
        # Translate align operation
        orig.setTranslation( targetTrans, space = 'world' )
    
    # Align rotation
    if mode == 'rotate' or mode == 'transform':
        # Create Quaternion object from target PyNode
        Quat = frmath.Quaternion( target.getRotation( space = 'world', quaternion = True ) )
        # orig.setRotation( Quat, space = 'world' )

        # Maybe we should use MyMatrix object in the future for the sake of math XD
        pm.xform( orig, ro = Quat.toEulerian().asList(), eu = True, ws = True )

def jointSplit( pynode, split = 2 ):
    # TODO: joint orientation not yet implement, naming?, return?, replace?
    # check if there is any selection
    sel = pm.ls( os = True )
    # make sure this is joint
    if isinstance( pynode, pm.nodetypes.Joint ) and len( pynode.getChildren() ) > 0 and split > 1:
        # clear selection
        pm.select( clear = True )
        # get first child
        firstChild = pynode.getChildren()[0]
        # get vector
        vecA = frmath.Vector( pynode.getTranslation( space = 'world' ) )
        vecB = frmath.Vector( firstChild.getTranslation( space = 'world' ) )

        parent = pynode
        factor = (vecB - vecA) / split
        for i in range(split-1):
            jnt = pm.createNode('joint')
            pos = factor * ( i + 1 ) + vecA
            jnt.setTranslation( pos.asList() )

            jnt.setParent( parent )
            parent = jnt
        firstChild.setParent( parent )

        # reselect selection if any
        pm.select( sel )

def jointOrient( pynodes ):
    pass



