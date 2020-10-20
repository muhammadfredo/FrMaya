import pymel.core as pm
import maya.cmds as mc

ctl = pm.ls('*CTL')
atts = ['.translateX','.translateY','.translateZ','.rotateX','.rotateY','.rotateZ']
res =[]
for o in ctl:
    for x in atts:
        if not ('%.4f' % mc.getAttr(o+x) == '0.0000' or '%.4f' % mc.getAttr(o+x) == '-0.0000'):
            print o+x, '%.4f' % mc.getAttr(o+x)
            res.append(o)
            break

pm.select(res)