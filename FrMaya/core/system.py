"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 31 Agt 2020
Info         :

"""
import os

from FrMaya.vendor import path


def __get_environ_path(environ_key):
    """Collect path from given environment key."""
    environ_value = os.environ.get(environ_key)

    if not environ_value:
        return []

    environ_path_list = environ_value.split(';')
    return [path.Path(o) for o in environ_path_list if os.path.exists(o)]


def get_menubar_path():
    """Collect menubar path from FR_MYMENUBAR environment."""
    return __get_environ_path('FR_MYMENUBAR')


def get_control_curve_path():
    """Collect control curve path from FR_CONTROLCURVE environment."""
    return __get_environ_path('FR_CONTROLCURVE')


