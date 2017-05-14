'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By             : Muhammad Fredo Syahrul Alam
# Email                      : muhammadfredo@gmail.com
# Start Date               : 12 May, 2017

# Purpose: create menubar in maya
# Bugs: 
# History: 
# Note: 
####################################################################################
####################################################################################
'''
import os
import pymel.core.uitypes as pmui

class Menubar(pmui.SubMenuItem):
    def foo(self):
        print "hello"

    def __init__(self, rootFolder, name=None):
        self.rootFolder = rootFolder

def createMenubar():
    print os.path.dirname(__file__)