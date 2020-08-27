import maya.cmds as mc


def getJointFromSelected():
    '''
    Check all object transform in scene, if object not in default transform select it
    '''
    obj = mc.ls(os=True)

    skins = []
    joints = []

    # get skincluster from object
    for o in obj:
        history = mc.listHistory(o, pdo=True, il=1)
        for x in history:
            if mc.nodeType(x) == "skinCluster":
                skins.append(x)

    # get joint from skincluster
    for o in skins:
        joints = joints + mc.skinCluster(o, q=True, inf=1)

    mc.select(joints)


getJointFromSelected()