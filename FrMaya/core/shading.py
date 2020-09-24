"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 16 Sep 2020
Info         :

"""
import re

import pymel.core as pm
from FrMaya.vendor import path


def get_file_node_path(input_node):
    # TODO: docstring here
    # FIXME: some homework need to be done, after finish need to include into core.init
    """Get the file path used by a Maya file node.
    Args: input_node (str): Name of the Maya file node
    Returns: str: the file path in use
    """
    # if the path appears to be sequence, use computedFileTextureNamePattern,
    # this preserves the <> tag
    if pm.attributeQuery('computedFileTextureNamePattern', node = input_node, exists = True):
        texture_pattern = input_node.attr('computedFileTextureNamePattern').get()

        patterns = ["<udim>", "<tile>", "u<u>_v<v>", "<f>", "<frame0", "<uvtile>"]
        lower = texture_pattern.lower()
        if any(pattern in lower for pattern in patterns):
            return texture_pattern

    # otherwise use fileTextureName
    return input_node.attr('fileTextureName').get()


# Big roy
# this is from https://gist.github.com/BigRoy/d027323b27bf9de8f92a7c2ea972122a
# modify it to use path.Path
def seq_to_glob(input_path):
    """Takes an image sequence path and returns it in glob format,
    with the frame number replaced by a '*'.
    Image sequences may be numerical sequences, e.g. /path/to/file.1001.exr
    will return as /path/to/file.*.exr.
    Image sequences may also use tokens to denote sequences, e.g.
    /path/to/texture.<UDIM>.tif will return as /path/to/texture.*.tif.
    Args:
        input_path (str): the image sequence path
    Returns:
        str: Return glob string that matches the filename pattern.
    """
    # FIXME: some homework need to be done, after finish need to include into core.init
    # TODO: docstring here
    assert isinstance(input_path, path.Path) or isinstance(input_path, str) or isinstance(input_path,
                                                                                          unicode), 'Wrong input_path'
    input_path = path.Path(input_path)

    # If any of the patterns, convert the pattern
    patterns = {"<udim>": "<udim>", "<tile>": "<tile>", "<uvtile>": "<uvtile>", "#": "#", "u<u>_v<v>": "<u>|<v>",
        "<frame0": "<frame0\d+>", "<f>": "<f>"}

    lower = input_path.lower()
    has_pattern = False
    for pattern, regex_pattern in patterns.items():
        if pattern in lower:
            input_path = re.sub(regex_pattern, "*", input_path, flags = re.IGNORECASE)
            has_pattern = True

    if has_pattern:
        return path.Path(input_path)

    base = input_path.basename()
    matches = list(re.finditer(r'\d+', base))
    if matches:
        match = matches[-1]
        new_base = '{0}*{1}'.format(base[:match.start()], base[match.end():])
        head = input_path.dirname()
        # return head.join(new_base)
        return head / new_base
    else:
        return input_path
