'''
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 19 Jan 2018
Purpose      : 

'''

import collections

def convert(dictname, dictionary):
    return collections.namedtuple(dictname, dictionary.keys())(**dictionary)



