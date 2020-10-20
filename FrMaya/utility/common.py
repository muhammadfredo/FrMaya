"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 14 Sep 2020
Info         :

"""
from collections import Iterable


def __flatten(input_iter):
    for item in input_iter:
        if isinstance(item, Iterable) and not isinstance(item, unicode):
            for x in __flatten(item):
                yield x
        else:
            yield item


def flatten(input_list):
    """Flatten nested list.

    :arg input_list: Nested list need to be flatten.
    :type input_list: list of list
    :rtype: list
    """
    return list(__flatten(input_list))



