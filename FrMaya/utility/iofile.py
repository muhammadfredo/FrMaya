"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Sep 2020
Info         :

"""
import os
import json

from FrMaya.vendor import path


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




