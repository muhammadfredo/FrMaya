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

from .init import (
    startup,
    install,
)
from .version import (
    authors,
    basedir,
    version,
    versiontuple,
)

assert sys.version_info > (2, 7), (
    "FrMaya version {0} is compatible with Maya2014/python2.7 or later".format(version())
)
