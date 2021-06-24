"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 03 Sep 2020
Info         :

"""
import os
import json

from FrMaya.vendor import path, yaml


def read_json(input_path):
    """Open and read json file.

    :arg input_path: absolute json file path.
    :type input_path: path.Path
    :return: json file data
    :rtype: dict or None
    """
    if os.path.isfile(input_path):
        with open(input_path) as data_stream:
            return json.load(data_stream)
    return None


def write_json(input_path, input_data):
    """Write json file from dictionary.

    :arg input_path: absolute json file path.
    :type input_path: path.Path
    :arg input_data: data as dictionary.
    :type input_data: dict
    :rtype: None
    """
    with open(input_path, 'w') as outfile:
        json.dump(input_data, outfile)


def read_yaml(input_path):
    """Open and read yaml file.

    :arg input_path: absolute yaml file path.
    :type input_path: str
    :return: yaml file data.
    :rtype: dict or None
    """
    if os.path.isfile(input_path):
        with open(input_path) as data_stream:
            return yaml.load(data_stream)
    return None


def write_yaml(input_path, input_data):
    """Write yaml file from dictionary.

    :arg input_path: absolute yaml file path.
    :type input_path: str
    :arg input_data: data as dictionary.
    :type input_data: dict
    :rtype: None
    """
    with open(input_path, 'w') as outfile:
        yaml.dump(input_data, outfile, default_flow_style = False)


def read_file_text(input_path):
    """Open and read ascii text file

    :arg input_path: absolute ascii text file path
    :type input_path: str
    :return: File text data.
    :rtype: str or None
    """
    if os.path.isfile(input_path):
        with open(input_path) as data_stream:
            return data_stream.read()
    return None


def write_file_text(input_path, input_data):
    """Write text file from any kind of format

    :arg input_path: absolute text file path
    :type input_path:str
    :arg input_data: data with any kind of format
    :type input_data: str
    :rtype: None
    """
    with open(input_path, "w") as outfile:
        outfile.write(input_data)




