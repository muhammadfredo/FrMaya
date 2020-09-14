import pymel.core as pm
bs = pm.PyNode('asFaceBS')
sel = pm.ls(os=1)
alias_bs= bs.listAliases()
#'brow_raiser_RShapeDeformed.worldMesh[0]' 'asFaceBS.inputTarget[0].inputTargetGroup[11].inputTargetItem[6000].inputGeomTarget'
for name, att in alias_bs:
    for o in sel:
        if name == o.nodeName():
            num = int(att.split('.weight')[1][1:-1])
            new_shp = o.getShapes(ni=1)[0]
            new_shp.worldMesh[0] >> bs.inputTarget[0].inputTargetGroup[num].inputTargetItem[6000].inputGeomTarget