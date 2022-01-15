"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 25 Dec 2021
Info         :

"""
import pymel.core as pm

if len(pm.selected()) >= 2:
    attr_list = ['translate', 'rotate', 'scale', 'jointOrient']
    sel = pm.selected()
    for attr_name in attr_list:
        print '{} >> {}'.format(sel[0], sel[1])
        sel[0].attr(attr_name) >> sel[1].attr(attr_name)