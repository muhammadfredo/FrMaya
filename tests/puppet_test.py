"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 25 Aug 2021
Info         :

To create rig:
import FrMaya.puppet as ppt

# find spine guide template create root component
root_guide = ppt.api.get_guide('3_placer_root')
root_cmp = ppt.api.create_component('All', root = True, guide = root_guide)

# find spine guide template then create spine component
spine_guide = ppt.api.get_guide('spine_biped')
spine_cmp = ppt.api.create_component('spine', hook = root, guide = spine_guide)

# add plugins
framework_plugin = ppt.api.get_plugin('framework')
root_cmp.add_plugin(framework_plugin)
spine_plugins = ppt.api.get_available_plugins(filter = spine_cmp)
spine_cmp.add_plugins(spine_plugins)

# create component as well the guides in the scene,
# recursive to all childrenthat hook to the component
root_cmp.create()

# setup leg component
leg_guide = ppt.api.get_guide('leg_biped')
leg_cmp = ppt.api.create_component('leg', hook = root, mirror = True, guide = leg_guide)
leg_plugins = ppt.api.get_available_plugins(filter = leg_cmp)
leg_cmp.add_plugins(leg_plugins)

# create leg component in the scene
leg_cmp.create()

# build the rig
root_cmp.build()

"""
