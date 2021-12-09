try:
    import sys
    _ppt_modules = [o for o in sys.modules.keys() if o.startswith('FrMaya.puppet.') and sys.modules[o]]
    _ppt_modules.sort()
    for o in _ppt_modules:
        del sys.modules[o]
except (Exception, ImportError):
    pass
from .constant import (
    MayaColorOverride
)
from .utility import (
    create_expose_rotation,
    create_spline_ik_rig,
    create_matrix_cons,
)
