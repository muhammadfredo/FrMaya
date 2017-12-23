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
# TODO: add __add__ and __str__
import os

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

class Folder(BasePath):
    '''
    Some shit
    '''
    
    def __init__(self):
        pass
