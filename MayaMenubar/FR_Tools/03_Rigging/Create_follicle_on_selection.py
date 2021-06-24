"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 04 May 2021
Info         :

"""
import FrMaya.core as fmc
import pymel.core as pm


def create_follicle_on_selection():
    sel = pm.ls(os = True)
    if len(sel) > 1:
        src_obj = sel[0]
        trgt_objs = sel[1:]
        follicle_list = fmc.create_follicle_object_position(src_obj, trgt_objs)

        for f, t in zip(follicle_list, trgt_objs):
            f.rename('{}_foll'.format(t.nodeName()))
            res = pm.parentConstraint(f, t, mo = True)
            res.setParent(world = True)


create_follicle_on_selection()
