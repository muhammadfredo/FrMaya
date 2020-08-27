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
__basedir__ = os.path.abspath(os.path.dirname(__file__))

import sys
assert sys.version_info > (2, 7), ( "FrMaya version {0} is compatible with Maya2014/python2.7 or later".format(__version__) )

from .Core import FrSystem

@FrSystem.singelton
class GlobalData(object):

    def __init__(self):
        self.__dict_data = {}

    def get(self, key):
        return self.__dict_data[key]

    def set(self, key, value):
        self.__dict_data[key] = value

def versiontuple():
    return __versiontuple__

def version():
    return __version__

def authors():
    return __authors__

def basedir():
    return __basedir__

def __lib_package():
    sys.path.append( os.path.join( basedir(), 'Lib' ) )

def __setup():
    # add third party package
    __lib_package()

    # assign frmaya version to global data
    GlobalData.set('version', version())

    import pymel.core as pm
    # the new way, more consistent with the other
    from Core.FrInterface import menubar
    reload( menubar )

    if not pm.about(batch = True):
        menubar.buildMenubar()

def startup():
    import pymel.core as pm
    
    pm.evalDeferred( __setup )

def install(source_path):
    # add third party package
    __lib_package()

    import FrMaya.Tools.AboutFrMaya as AboutFrMaya
    AboutFrMaya.show(source_path = source_path, install_btn = True)






