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


def _texture_file_pattern_to_glob(input_path):
    """Takes an image file path and returns it in glob format if the file path has pattern,
    with the pattern replaced by a '*'.
    Image file path may be numerical sequences, e.g. /path/to/file.1001.exr
    will return as /path/to/file.*.exr.
    Image file path may also use tokens to denote sequences, e.g.
    /path/to/texture.<UDIM>.tif will return as /path/to/texture.*.tif.

    Based from Big roy github gist

    https://gist.github.com/BigRoy/d027323b27bf9de8f92a7c2ea972122a

    :arg input_path: Image file path need to process.
    :type input_path: str or path.Path
    :rtype: path.Path
    """
    input_path = path.Path(input_path)

    # If any of the patterns, convert the pattern
    patterns = {
        "<udim>": "<udim>",
        "<tile>": "<tile>",
        "<uvtile>": "<uvtile>",
        "#": "#",
        "u<u>_v<v>": "<u>|<v>",
        "<frame0": "<frame0\\d+>",
        "<f>": "<f>"
    }
    lower = input_path.lower()
    has_pattern = False
    for pattern, regex_pattern in patterns.items():
        if pattern in lower:
            input_path = re.sub(regex_pattern, "*", input_path, flags = re.IGNORECASE)
            has_pattern = True
    if has_pattern:
        return path.Path(input_path)
    else:
        # pattern not found
        return input_path


def get_file_node_path(texture_file_node):
    """Get file path from file node, preserve pattern format such as <udim> or <f>.

    :arg texture_file_node: File pynode that need to get file path extracted.
    :type texture_file_node: pm.PyNode
    :rtype: path.Path
    """
    # use computedFileTextureNamePattern attr instead fileTextureName,
    # this preserves the <> tag / format pattern
    if texture_file_node.hasAttr('computedFileTextureNamePattern'):
        texture_pattern = texture_file_node.attr('computedFileTextureNamePattern').get()

        patterns = ["<udim>", "<tile>", "u<u>_v<v>", "<f>", "<frame0", "<uvtile>"]
        lower = texture_pattern.lower()
        if any(pattern in lower for pattern in patterns):
            return path.Path(texture_pattern)
    # otherwise use fileTextureName
    return path.Path(texture_file_node.attr('fileTextureName').get())


def get_texture_pattern_files(texture_file_pattern):
    """Collect / glob specified image file path.

    :arg texture_file_pattern: Image file path need to glob,
     file name must have glob pattern '*' (asterix).
    :type texture_file_pattern: str or path.Path
    :rtype: list of path.Path
    """
    texture_file_glob = _texture_file_pattern_to_glob(texture_file_pattern)
    return texture_file_glob.parent.glob(texture_file_glob.name)


def set_default_shader(input_node):
    """Assign initialShadingGroup to specified node.

    :arg input_node: PyNode need to be assign with initialShadingGroup.
    :type input_node: pm.PyNode
    """
    pm.sets('initialShadingGroup', edit = True, forceElement = input_node)


