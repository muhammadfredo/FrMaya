'''
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 21 May, 2017
#
# Purpose: 
# Bugs: 
# History: 
# Note: 
'''

import os
import factories


class BasePath(object):
    '''
    Base class for handle external file
    '''
    
    def __init__(self, pathfile):
        '''
        Base class for handle external file
        
        :param pathfile: Full path file
        '''
        
        self._fullpath = pathfile
        self._filepath = os.path.split( pathfile )
        self._name, self._extention = os.path.splitext( os.path.basename( pathfile ) )
    
    def getFullpath(self):
        '''
        Get fullpath of the file
        '''
        
        return self._fullpath
    
    def getPath(self):
        '''
        Get directory path of the file
        '''
        
        return self._filepath
    
    def getFilename(self):
        '''
        Get filename of the file
        '''
        
        return self._name
    
    def getExtention(self):
        '''
        Get file extention of the file
        '''
        
        return self._extention
    
    def isDir(self):
        '''
        Check if this is a folder or a file
        '''
        
        return os.path.isdir( self._fullpath )
    
    def isFile(self):
        '''
        Check if this is a file
        '''
        
        return not os.path.isdir( self._fullpath )

def isClass(theNode, classString):
    return theNode == factories.__classLookup__(classString)

class PathNode(object):

    def __new__(cls, *args, **kwargs):
        if args:
            # get the input path
            thePath = args[0]

            # if input more than 1, add the other to the path
            if len(args) > 1:
                for o in args[1:]:
                    thePath = cls.join(thePath, o)

            # find appropriate class based on input path,
            # and setup instance of the new class according to what needed
            # return new instance of appropriate class
            self = factories.__factory__(thePath, PathNode, cls)

            return self
        else:
            # in case of failure of factory creation, return pathnode class
            return super( PathNode, cls ).__new__( cls )

    def __init__(self, *args, **kwargs):
        # instance variabele
        self.__fullpath__ = ''

    def __repr__(self):
        return 'PathNode( {0} )'.format( self.__fullpath__ )

    def __add__(self, other):
        try:
            return PathNode(os.path.join(self.fullpath, other))
        except Exception, e:
            print '{0}'.format(e)
            return None

    @staticmethod
    def join(headPath, tailPath):
        return os.path.abspath( os.path.join( headPath, tailPath ) )

    @property
    def fullpath(self):
        return  self.__fullpath__

    @property
    def exists(self):
        return os.path.exists( self.__fullpath__ )


