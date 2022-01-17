"""
Module hierarchy
+ antivirus
+ message
+ naming
+ scene_info
+ shading
+ system
+ transformation
    + general
    + scene_cleanup
    + uimaya
        + animation
        + rig

the plan
+ antivirus >> standalone
+ message >> standalone
+ naming >> standalone
+ scene_info >> scene
+ shading >> general
+ transformation >> standalone
+ general >> standalone
+ scene_cleanup >> scene
"""
try:
    import sys
    _fmc_modules = [o for o in sys.modules.keys() if o.startswith('FrMaya.core.') and sys.modules[o]]
    _fmc_modules.sort()
    for o in _fmc_modules:
        reload(sys.modules[o])
except (Exception, ImportError):
    pass
from .animation import (
    bake_animation,
    copy_animation,
)
from .antivirus import (
    clean_malware_files,
    clean_outliner_command_script,
    clean_virus,
)
from .general import (
    backup_file,
    build_curve,
    create_surface_plane,
    duplicate_original_mesh,
    get_channelbox_attributes,
    get_soft_selection,
    hide_attributes,
    keyable_attributes,
    lock_attributes,
    nonkeyable_attributes,
    pgroup,
    serialize_curve,
    transfer_shape,
    unhide_attributes,
    unlock_attributes,
)
from .message import (
    MyCallbackManager
)
from .naming import (
    get_unique_name
)
from .rig import (
    comet_joint_orient,
    create_control,
    create_follicle_object_position,
    create_follicle_uv,
    create_soft_cluster,
    get_control_files,
    get_skincluster_info,
    get_skincluster_node,
    prune_skincluster,
    remove_unused_influence,
    reset_attributes,
    set_attrs_default,
    split_joint,
    transfer_skincluster,
)
from .scene import (
    clean_anim_layer,
    clean_animation_node,
    clean_dag_pose,
    clean_display_layer,
    clean_empty_mesh,
    clean_mentalray_nodes,
    clean_namespace,
    clean_ngskin_node,
    clean_turtle_node,
    clean_unknown_node,
    clean_unknown_plugins,
    clean_unused_node,
    fix_duplicate_name,
    fix_shading_engine_intermediate,
    get_bad_shape_name,
    get_duplicate_name,
    get_empty_mesh,
    get_end_frame,
    get_namespaces,
    get_pasted_node,
    get_references,
    get_scene_fps,
    get_scene_modified,
    get_scene_unit,
    get_shading_engine_intermediate,
    get_start_frame,
    get_unfreeze_transform,
    get_zero_scale,
)
from .shading import (
    get_file_node_path,
    glob_texture_files,
    set_default_shader,
)
from .system import (
    check_local_package,
    download_latest_version,
    get_control_curve_path,
    get_menubar_path,
    get_server_version,
    install,
    maya_version_as_float,
    uninstall,
)
from .transformation import (
    align,
    freeze_transform,
    get_offset_matrix,
    reset_transform,
    world_space_translate,
    xform_mirror
)
from .uimaya import (
    build_menubar,
    get_icon_file,
    get_maya_window,
    MyQtWindow,
)

