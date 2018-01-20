'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : Jan 06, 2018
Purpose      :

'''

import os

def __superPath__(thePath):
    # default path
    if thePath == None or thePath == '':
        return os.path.expanduser( '~' )

    # make sure we modify only folder path
    if os.path.isdir(thePath):
        # check if last path had slash,
        # eg > 'D:\Dropbox\' should be > 'D:\Dropbox
        res = os.path.split( thePath )
        if not res[ 1 ]:
            return res[0]

    return thePath

def __classLookup__(classString):
    import nodeFile

    classDict = {
        'DigiNode' : nodeFile.DigiNode,
        'FolderNode' : nodeFile.FolderNode,
        'FileNode' : nodeFile.FileNode,
        'JsonNode' : nodeFile.JsonNode }

    return classDict.get(classString)

def __getClass__(thePath):
    if thePath == '':
        raise ValueError( 'input empty, stupid shit!!!' )
    elif os.path.isdir( thePath ):
        return __classLookup__('FolderNode')
    elif os.path.isfile( thePath ):
        if thePath.endswith('.json'):
            return __classLookup__('JsonNode')
        else:
            return __classLookup__('FileNode')
    else:
        return None

class FactoryException(Exception):
    pass

def __factory__(thePath, pathnode, cls):
    # modified path based on special symbol or name
    thePath = __superPath__(thePath)

    # get the new class from class factory
    newCls = __getClass__(thePath)

    # if new class not found, use default class which is PathNode
    if not newCls:
        raise FactoryException('New class not found, check input PathNode')

    # create new instance of the new class
    theNode = super( pathnode, cls ).__new__( newCls )

    # set new class fullpath attributes
    theNode.__fullpath__ = thePath

    return theNode



