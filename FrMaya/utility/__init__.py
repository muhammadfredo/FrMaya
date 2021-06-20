"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 03 Sep 2020
Info         :

"""
try:
    import sys
    _fmc_modules = [o for o in sys.modules.keys() if o.startswith('FrMaya.utility.') and sys.modules[o]]
    _fmc_modules.sort()
    for o in _fmc_modules:
        reload(sys.modules[o])
except (Exception, ImportError):
    pass
from .common import (
    flatten,
    MetaSingleton
)
from .decoration import (
    singelton,
    undoable
)
from .iofile import (
    read_json,
    write_json,
    read_yaml,
    write_yaml,
    read_file_text,
    write_file_text
)


