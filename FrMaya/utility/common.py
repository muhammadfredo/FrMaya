"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 14 Sep 2020
Info         :

"""
from collections import Iterable
from contextlib import contextmanager
from datetime import datetime


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


def unique_list(input_list):
    """Make list unique by getting rid duplicated value inside the list.

    :arg input_list: List need to be made unique.
    :type input_list: list
    :rtype: list
    """
    return list(set(input_list))


class MetaSingleton(type):
    """Singleton metaclass.
    This should be preferred instead of singleton decorator.
    Using singleton metaclass the singleton class can be inheritance."""
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


@contextmanager
def stopwatch(timer_mssg = ''):
    start_timer = datetime.now()

    yield True

    if timer_mssg:
        timer_mssg = ' - {}'.format(timer_mssg)
    print('{}{}'.format(datetime.now() - start_timer, timer_mssg))
