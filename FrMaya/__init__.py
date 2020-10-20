"""
*******************************
          FrMaya
*******************************

Created By            : Muhammad Fredo Syahrul Alam
Copyright             : Muhammad Fredo Syahrul Alam
Email                 : muhammadfredo@gmail.com
Start Date            : 10 May, 2017
Purpose               :

"""
import sys

import FrMaya.utility as util
from .version import (
    authors,
    basedir,
    version,
    versiontuple,
)

assert sys.version_info > (2, 7), (
    "FrMaya version {0} is compatible with Maya2014/python2.7 or later".format(version())
)


@util.singelton
class GlobalData(object):

    def __init__(self):
        self.__dict_data = {}

    def get(self, key):
        return self.__dict_data[key]

    def set(self, key, value):
        self.__dict_data[key] = value


def __setup():
    # assign frmaya version to global data
    GlobalData.set('version', version())

    import pymel.core as pm
    # the new way, more consistent with the other
    from . import core as fmc

    if not pm.about(batch = True):
        fmc.build_menubar()


def startup():
    import pymel.core as pm

    pm.evalDeferred(__setup)


def install(source_path):
    import FrMaya.tools.AboutFrMaya as AboutFrMaya
    AboutFrMaya.show(source_path = source_path, install_btn = True)
