'''
####################################################################################
####################################################################################
## SCRIPT HEADER ##
# Created By            : Muhammad Fredo Syahrul Alam
# Email                 : muhammadfredo@gmail.com
# Start Date            : 10 May, 2017
# Credit                : Muhammad Fredo
#
# Purpose:
# Bugs:
# History:
# Note:
####################################################################################
####################################################################################
'''
import os

def setup():
    import App.menubar as menubar
    
    menubar.buildMenubar()

def startup():
    import pymel.core as pm
    
    pm.evalDeferred( setup )