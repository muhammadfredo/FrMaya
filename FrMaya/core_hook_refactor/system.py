"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 31 Agt 2020
Info         :

"""
import os

from FrMaya.vendor import path


def get_menubar_path():
    # type : () -> List[path.Path]
    """Collect menubar path from FR_MYMENUBAR environment"""
    menubar_environ = os.environ.get('FR_MYMENUBAR')

    if not menubar_environ:
        return []

    menubar_path_list = menubar_environ.split(';')
    return [path.Path(o) for o in menubar_path_list if os.path.exists(o)]


