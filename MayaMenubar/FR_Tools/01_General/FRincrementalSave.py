'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By            : Muhammad Fredo
# Email                 : muhammadfredo@gmail.com
# Start Date            : February, 2016
# Credit                : Martin Breidt
# Credit Web            : http://scripts.breidt.net/

# Purpose: Easy and organized incremental save
# Bugs: 
# History: 
# Note: Original design from maxscript incremental save created by Martin Breidt
####################################################################################
####################################################################################
'''

import maya.cmds as mc
from shutil import copyfile
import os, glob

def incrementalSave(fullPathFile):
    #spliting path name type
    thePath, theFile = os.path.split(fullPathFile)
    theFile, fileType = os.path.splitext(theFile)
    
    #bak folder variable
    bakFolder = thePath + "/" + theFile + ".bak"
    
    #detect if bak folder exist
    if not os.path.exists(bakFolder):
        os.makedirs(bakFolder)
    
    #how many files already backuped
    bakFiles = bakFolder + "/" + theFile + "_bak_*" + fileType
    count = str( len(glob.glob(bakFiles)) + 1 )
    
    if len(count) == 1:
        count = "00" + count
    elif len(count) == 2:
        count = "0" + count
    
    #new bak file
    bakFile = bakFolder + "/" + theFile + "_bak_" + count + fileType
    
    #save file
    type = "mayaBinary"
    if fileType == ".ma":
        type = "mayaAscii"
    mc.file( save = True, type = type )
    
    #copy the file / backup the file
    result = copyfile(fullPathFile, bakFile)
    print fullPathFile
    print bakFile
    print result

#get full path file
pathFile = mc.file( query = True, sceneName = True )
incrementalSave(pathFile)