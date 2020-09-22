"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Sep 2020
Info         :

"""
import pymel.core as pm


def singelton(input_class):
    """A decorator that will turn class into singleton."""
    instances = {}

    def get_instance(*args, **kwargs):
        if input_class not in instances:
            instances[input_class] = input_class(*args, **kwargs)

        return instances[input_class]

    return get_instance()


def undoable(input_function):
    """A decorator that will make commands undoable in maya.
    from "Kriss Andrews" on http://blog.3dkris.com/
    """
    def decorator_code(*args, **kwargs):
        pm.undoInfo(openChunk=True)
        function_return = None

        try:
            function_return = input_function(*args, **kwargs)

        finally:
            pm.undoInfo(closeChunk=True)
            return function_return

    return decorator_code


