
import pymel.core as pm
from FrMaya.Core import FrFile
topnode = pm.ls(os=1)
rig_path =  pm.sceneName().replace('_MDL', '_RIG')
pm.saveAs(rig_path)
rig_temp = r"D:\Dropbox\Project_ongoing\Technical_build\Faishal_project\rig_template\RigStarter.ma"
res = pm.importFile(rig_temp, returnNewNodes=True)
joint_res = pm.ls(type='joint')