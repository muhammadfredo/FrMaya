"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 20 Jun 2021
Info         :

"""
import pymel.core as pm


def get_unique_name(init_name):
    """
    Return unique name in the scene from specified argument.

    :arg init_name: Name that need to be unique.
    :type init_name: str
    :rtype: str
    """
    new_name = init_name
    i = 1
    while len(pm.ls(new_name)) > 0:
        # generate a new name until there is no object with this name
        new_name = '{}{}'.format(init_name, i)
        i += 1
    return new_name
