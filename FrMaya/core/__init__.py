from .animation import (
    bake_animation,
    copy_animation,
)
from .general import (
    pgroup,
    split_joint,
    comet_joint_orient,
    build_curve,
    keylockhide_attribute,
    transfer_shape,
)
from .rig import (
    get_skincluster_info,
    get_skincluster_node,
    get_control_files,
    create_control,
    remove_unused_influence,
    transfer_skincluster,
    reset_attributes,
    get_channelbox_attributes,
    set_attrs_default,
)
from .scene_cleanup import (
    clean_unknown_plugins
)
from .scene_info import (
    get_duplicate_name,
    get_namespaces,
    get_pasted_node,
    get_references,
    get_zero_scale,
    get_scene_fps,
    get_scene_modified,
    get_scene_unit,
    get_bad_shape_name,
    get_empty_mesh,
    get_start_frame,
    get_end_frame,
)
from .system import (
    get_menubar_path,
    get_control_curve_path,
    maya_version_as_float,
    install,
    uninstall,
)
from .transformation import (
    align,
    freeze_transform,
    reset_transform,
)
from .uimaya import (
    build_menubar,
    MyQtWindow,
)

