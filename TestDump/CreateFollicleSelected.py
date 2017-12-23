'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : Dec 7, 2017
Purpose      : 

'''
''' for poly surface'''

import pymel.core as pm

all = pm.ls(os=True)
sel = all[:-1]
mesh = all[-1]

def createFollicleCloseToSelected( sel, mesh, parentCons = True ):
    for o in sel:
        closest = pm.createNode('closestPointOnMesh')
        mesh.outMesh >> closest.inMesh
          
        translate = pm.xform(o,t=True,q=True)
         
        closest.inPositionX.set(translate[0])
        closest.inPositionY.set(translate[1])
        closest.inPositionZ.set(translate[2])
         
        follShp = pm.createNode('follicle')
        follTm = follShp.getParent()
         
        follShp.outRotate >> follTm.rotate
        follShp.outTranslate >> follTm.translate
         
        mesh.worldMatrix >> follShp.inputWolrdMatrix
        mesh.outMesh >> follShp.inputMesh
         
        follShp.simulationMethod.set(0)
        follShp.parameterU.set( closest.result.parameterU.get() )
        follShp.parameterV.set( closest.result.parameterV.get() )
        if parentCons:
            pm.parentConstraint(follTm, o, mo=True)
         
        pm.delete(closest)
createFollicleCloseToSelected(sel,mesh)
