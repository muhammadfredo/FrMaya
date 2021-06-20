"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
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

from FrMaya import utility as util


# TODO: need docstring
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
        print 'initialize callback manager'
        self._maya_event_callback = {}
        self._registered_callback = {}

        self._maya_event_callback = copy.deepcopy(self.get_maya_event_callback())

        assert len(self._maya_event_callback) > 0, ''

    def _group_registered_callbacks(self):
        result_data = {'events': {}, 'tags': {}}
        for cb_fn_name, cb_data in self._registered_callback.items():
            for each in result_data:
                if each == 'events':
                    event_or_tag = cb_data['event_name']
                elif each == 'tags':
                    event_or_tag = cb_data['callback_tag']
                else:
                    return None

                if result_data[each].get(event_or_tag):
                    result_data[each][event_or_tag].append(cb_fn_name)
                else:
                    result_data[each][event_or_tag] = [cb_fn_name]
        return result_data

    def add_callback(self, event_name, callback_tag, func):
        my_event_cb = self._maya_event_callback.get(event_name)

        if my_event_cb:
            callback_id = my_event_cb['add_callback'](my_event_cb['event_id'], func)

            self._registered_callback[func.__module__] = {
                'event_name': event_name,
                'callback_tag': callback_tag,
                'callback_id': callback_id
            }

            return True
        else:
            return False

    def remove_callback(self, event_name = '', callback_tag = ''):
        callback_collection = self._group_registered_callbacks()

        cb_id_array = om.MCallbackIdArray()
        cb_fn_name_list = []
        if event_name:
            cb_fn_name_list.extend(callback_collection['events'].get(event_name, []))
        if callback_tag:
            cb_fn_name_list.extend(callback_collection['tags'].get(callback_tag, []))

        for cb_fn_name in cb_fn_name_list:
            cb_id_array.append(self._registered_callback[cb_fn_name]['callback_id'])

        if cb_id_array:
            om.MMessage.removeCallbacks(cb_id_array)

    def show_registered_callback(self, event_name = '', callback_tag = ''):
        result = self._group_registered_callbacks()

        if event_name:
            return result['events'].get(event_name, [])
        elif callback_tag:
            return result['tags'].get(callback_tag, [])
        else:
            return copy.deepcopy(result)

    def show_maya_event_name(self):
        return self._maya_event_callback.keys()


