'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 22 July, 2017
#
# Purpose: 
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''

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
                theName.replace( re, suffix )
            
            # Create group for each supplied object
            grp = pm.group( empty = True, name = theName + suffix )
            
            # Snap the group to each object transformation
            grp.setTransformation( o.getTransformation() )
            
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
            theName.replace( re, suffix )
        
        # Create single group
        grp = pm.group( empty = True, name = theName + suffix )
        
        # Collect group to output
        output.append( grp )
        
        # Loop through all supplied object and parent it to group
        for o in pynodes:
            o.setParent( grp )
        
    return output

def align( pynodes, mode = 'transform' ):
    '''
    Align from first pynode to second pynode
    
    :param pynodes: List of pynode, count total 2
    :param mode: transform, translate, rotate
    '''
    
    # Filter supplied pynodes, if less than 2 then return false
    if len(pynodes) < 2:
        return False
    
    # Assign supplied pynodes to local variable
    first, second = pynodes[0], pynodes[1]
    
    # Snap position
    if mode == 'translate' or mode == 'transform':
        # Snap position of first node to second node using constraint
        cons = pm.pointConstraint( second, first, maintainOffset = False )
        # Delete the constraint
        pm.delete( cons )
    
    # Snap rotation
    if mode == 'rotate' or mode == 'transform':
        # Snap rotation of first node to second node using constraint
        cons = pm.orientConstraint( second, first, maintainOffset = False )
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