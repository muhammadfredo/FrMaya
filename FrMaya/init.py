"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Nov 2020
Info         :

"""
import pymel.core as pm

from . import core as fmc
from . import utility as util


# Global Data will get depreciated
@util.singelton
class GlobalData(object):

    def __init__(self):
        self.__dict_data = {}

    def get(self, key):
        return self.__dict_data[key]

    def set(self, key, value):
        self.__dict_data[key] = value


def __setup():
    if not pm.about(batch = True):
        fmc.build_menubar()


def startup():
    pm.evalDeferred(__setup)


def install(source_path):
    import FrMaya.tools.AboutFrMaya as AboutFrMaya
    AboutFrMaya.show(source_path = source_path, install_btn = True)


