'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : Des 30, 2017
Purpose      :

'''

import glob
import os
import json
from baseFile import PathNode


class DigiNode( PathNode ):

    def __init__(self, *args, **kwargs):
        # digi is pun to digital, digital monster
        # instance variabele
        self.__nodeName__ = ''
        self.__digiPath__ = ''

        if self.__fullpath__:
            self.__digiPath__, self.__nodeName__ = os.path.split( self.__fullpath__ )

    @property
    def name(self):
        return self.__nodeName__

    @property
    def path(self):
        '''
        return path to this node
        '''
        return self.__digiPath__

    @property
    def parent(self):
        '''
        return parent of this node, type of the node depend will be factorized bt PathNode
        '''
        return PathNode( self.__digiPath__ )

class FolderNode(DigiNode):

    def __init__(self, *args, **kwargs):
        super(FolderNode, self).__init__()

    def __repr__(self):
        return 'FolderNode( {0} )'.format( self.__fullpath__ )

    def getChildrens(self, filters = ''):
        if not filters:
            filters = '*'

        listData = glob.glob( self.join( self.__fullpath__, filters ) )
        return [ PathNode( o ) for o in listData ]

    def getChildren(self, namefile = ''):
        if not namefile:
            try:
                return self.getChildrens()[0]
            except:
                return None

        child = PathNode( self.join( self.__fullpath__, namefile ) )

        return child

class FileNode(DigiNode):

    def __init__(self, *args, **kwargs):
        super(FileNode, self).__init__()

        # instance variabele
        self.__fileName__ = ''
        self.__extention__ = ''

        if self.__fullpath__:
            self.__fileName__, self.__extention__ = os.path.splitext( self.__nodeName__ )

    def __repr__(self):
        return 'FileNode( {0} )'.format( self.__fullpath__ )

    @property
    def name(self):
        return self.__fileName__

    @property
    def extention(self):
        return self.__extention__

class JsonNode(FileNode):
    """
    file node for json file
    """

    def __init__(self, *args, **kwargs):
        """Constructor for JsonNode"""
        super(JsonNode, self).__init__()
    
    @property
    def data(self):
        return json.load( open(self.fullpath) )





