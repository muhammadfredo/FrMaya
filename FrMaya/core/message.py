"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo Syahrul Alam
Email        : muhammadfredo@gmail.com
Start Date   : 03 Nov 2020
Info         :

alternative_callback_data: header data
  "id": (callback id)
    "event_name": "after_open"
    "callback_tag": fr_maya

maya_event_callbacks:
  after_open:
    event_id: event_id,
    add_callback: om callback function
  before_open:
    event_id: event_id,
    add_callback: om callback function
"""
import copy
import inspect
import re

import maya.OpenMaya as om
import pymel.core as pm

from FrMaya import utility as util


class MyCallbackManager(object):
    __metaclass__ = util.MetaSingleton

    @staticmethod
    def get_maya_event_callback():
        # example regex subs -> re.sub(r"(\w)([A-Z])", r"\1 \2", "WordWordWord")
        callback_events = {}
        re_pattern = re.compile(r'(?<=\w)([A-Z])')
        for event_name, event_id in inspect.getmembers(om.MSceneMessage):
            if event_name.startswith('k') and not event_name.endswith('check'):
                if not callback_events.get(event_name):
                    key_name = re_pattern.sub(r'_\1', event_name[1:])
                    callback_events[key_name.lower()] = {
                        'event_id': event_id,
                        'add_callback': om.MSceneMessage.addCallback,
                    }

        return callback_events

    def __init__(self):
        self._maya_event_callback = {}
        self._registered_callback = {}

        self._maya_event_callback = copy.deepcopy(self.get_maya_event_callback())

        assert len(self._maya_event_callback) > 0, ''

    def _collect_registered_callbacks(self):
        result_data = {'events': {}, 'tags': {}}
        for cb_id, cb_data in self._registered_callback.items():
            for each in result_data:
                if each == 'events':
                    event_or_tag = cb_data['event_name']
                elif each == 'tags':
                    event_or_tag = cb_data['callback_tag']
                else:
                    return None

                if result_data[each].get(event_or_tag):
                    result_data[each][event_or_tag].append(cb_id)
                else:
                    result_data[each][event_or_tag] = [cb_id]
        return result_data

    def add_callback(self, event_name, callback_tag, func):
        maya_event_callbacks = self._maya_event_callback.get(event_name)
        my_event_cb = maya_event_callbacks.get(event_name)

        if my_event_cb:
            callback_id = my_event_cb['add_callback'](my_event_cb['id'], func)

            self._registered_callback[str(callback_id)] = {
                'event_name': event_name,
                'callback_tag': callback_tag
            }

            return True
        else:
            return False

    def remove_callback(self, event_name = '', callback_tag = ''):
        callback_collection = self._collect_registered_callbacks()

        cb_id_array = om.MCallbackIdArray()
        temp_list = []
        if event_name:
            temp_list.extend(callback_collection['events'].get(event_name, []))
        if callback_tag:
            temp_list.extend(callback_collection['tags'].get(callback_tag, []))

        for o in temp_list:
            cb_id_array.append(o)

        if cb_id_array:
            om.MMessage.removeCallbacks(cb_id_array)

    def show_registered_callback(self, event_name = '', callback_tag = ''):
        result = self._collect_registered_callbacks()

        if event_name:
            return result['events'].get(event_name, [])
        elif callback_tag:
            return result['tags'].get(callback_tag, [])
        else:
            return copy.deepcopy(result)

    def show_maya_event_name(self):
        return self._maya_event_callback.keys()


callbacks = MyCallbackManager()


