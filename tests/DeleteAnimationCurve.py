import pymel.core as pm

def getAnimCurve():
    animCurves = pm.ls(type=["animCurveTU", "animCurveTL", "animCurveTA"], editable=True)
    return animCurves

yoo = getAnimCurve()
print yoo
print len(yoo)
pm.delete(yoo)


