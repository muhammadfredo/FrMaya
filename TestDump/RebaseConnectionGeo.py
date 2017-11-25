import pymel.core as pm

sel=pm.ls(os=1)
def rebaseGeo(o):
    base = None; orig = None; final = None
    shps=o.getShapes()
    for x in shps:
        if x.isIntermediate():
            if 'Orig' in x.name():
                orig = x
            else:
                base = x
        else:
            final = x
    #print base, orig, final
    baseConnectTo = pm.listConnections(orig.worldMesh,p=1,d=1)[0]
    base.worldMesh >> baseConnectTo
    shdConnectTo = pm.listConnections(base.instObjGroups,p=1,d=1)[0]
    final.instObjGroups >> shdConnectTo
for o in sel:
    rebaseGeo(o)