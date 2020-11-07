"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Nov 2020
Info         :
registered_callbacks:
  after_open:
    id_name:
      func: [(id, func), (id, func), (id, func),...]

data_callbacks:
  after_open:
    id: event_id,
    message: om callback function
  before_open:
    id: event_id,
    message: om callback function
"""
import copy
import inspect
import re

import maya.OpenMaya as om
import pymel.core as pm

from FrMaya import utility as util


@util.singelton
class MyCallbackManager(object):
    def __init__(self, callback_message = None):
        self._callback_data = {}
        self._callback_registered = {}

        if callback_message:
            self._callback_data = copy.deepcopy(callback_message)

    def add_callback(self, event_name, id_name, func):
        event_callback = self._callback_data.get(event_name)
        if not event_callback:
            return False
        event_id = event_callback['id']
        event_message = event_callback['message']

        callback_id = event_message(event_id, func, id_name)

        if self._callback_registered.get(event_name):
            if self._callback_registered[event_name].get(id_name):
                self._callback_registered[event_name][id_name].append((callback_id, func))
            else:
                self._callback_registered[event_name][id_name] = [(callback_id, func)]
        else:
            self._callback_registered[event_name] = {
                id_name: [(callback_id, func)]
            }

        return True

    def remove_callback(self, callback_type = '', id_name = ''):
        pass

    def show_registered_callback(self, event_name = '', id_name = ''):
        if event_name:
            return self._callback_registered.get(event_name, {})
        if id_name:
            pass

    def show_event_callback(self):
        return self._callback_data.keys()


def get_maya_callbacks():
    callback_events = {}
    re_pattern = re.compile(r'(?<=\w)([A-Z])')
    re.sub(r"(\w)([A-Z])", r"\1 \2", "WordWordWord")
    for event_name, event_id in inspect.getmembers(om.MSceneMessage):
        if event_name.startswith('k') and not event_name.endswith('check'):
            if not callback_events.get(event_name):
                key_name = re_pattern.sub(r'_\1', event_name[1:])
                callback_events[key_name.lower()] = {
                    'id': event_id,
                    'message': om.MSceneMessage.addCallback
                }

    return callback_events


callbacks = MyCallbackManager(callback_message = get_maya_callbacks())


