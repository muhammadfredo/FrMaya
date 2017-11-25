
'''
*******************************
          FrMaya
*******************************

Created By            : Muhammad Fredo Syahrul Alam
Copyright             : Muhammad Fredo Syahrul Alam
Email                 : muhammadfredo@gmail.com
Start Date            : 10 May, 2017
Purpose               : 

'''
import os

__versiontuple__ = (0, 6, 0)
__version__ = '.'.join(str(x) for x in __versiontuple__)
__authors__ = ['Muhammad Fredo']

import sys
assert sys.version_info > (2, 7), ( "FrMaya version {0} is compatible with Maya2014/python2.7 or later".format(__version__) )

def setup():
    # old way
#     import App.menubar as menubar
#     reload( menubar )
    # the new way, more consistent with the other
    from Core.FrInterface import Menubar
    reload( Menubar )
    
    Menubar.buildMenubar()

def startup():
    import pymel.core as pm
    
    pm.evalDeferred( setup )