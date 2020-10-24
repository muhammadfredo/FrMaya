"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Sep 2020
Info         :

"""
import os


__versiontuple__ = (1, 0, 3)
__version__ = '.'.join(str(x) for x in __versiontuple__)
__authors__ = ['Muhammad Fredo']
__basedir__ = os.path.abspath(os.path.dirname(__file__))


def versiontuple():
    return __versiontuple__


def version():
    return __version__


def authors():
    return __authors__


def basedir():
    return __basedir__
