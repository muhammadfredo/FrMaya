"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 29 Agt 2020
Info         :

"""
import os
import json

from FrMaya.vendor import path
from pymel import core as pm


def singelton(input_class):
    instances = {}

    def get_instance(*args, **kwargs):
        if input_class not in instances:
            instances[input_class] = input_class(*args, **kwargs)

        return instances[input_class]

    return get_instance()


def undoable(input_function):
    """
    from "Kriss Andrews" on http://blog.3dkris.com/
    A decorator that will make commands undoable in maya
    """

    def decorator_code(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        function_return = None

        try:
            function_return = input_function(*args, **kwargs)

        finally:
            pm.undoInfo(closeChunk=True)
            return function_return

    return decorator_code


def read_json(input_path):
    """
    Open and read json file

    :arg input_path: absolute json file path
    :type input_path: path.Path
    :return: dictionary of json file data
    :rtype: dict
    """
    if os.path.isfile(input_path):
        with open(input_path) as data_stream:
            return json.load(data_stream)
    return None


def write_json(input_path, input_data):
    """
    Write json file from dictionary

    :arg input_path: absolute json file path
    :type input_path: path.Path
    :arg input_data: data as dictionary
    :type input_data: dict
    :return: None
    """
    with open(input_path, 'w') as outfile:
        json.dump(input_data, outfile)


