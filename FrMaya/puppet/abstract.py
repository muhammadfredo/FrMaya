"""
## SCRIPT HEADER ##

Created By   : Muhammad Fredo
Email        : muhammadfredo@gmail.com
Start Date   : 17 Aug 2021
Info         :

AbstractNode
  - PRS:
    - Group: group node(empty transform) for any kind of stuff in a rig system
      - Buffer: a group node act as buffer zero out transform in a rig system
    - Joint: joint node for any kind of stuff in a rig system
      - Bind: joint node specialy for deforming mesh
      - Guide: joint node specialy for guiding auto rig build
    - Control: control node for any kind of animation control stuff in a rig system
      - Static: non moveable control only for changing its property. Ex: Ik/Fk switch
      - Icon: control only used as graphical interface for animator
  - Constraint
    - Parent
    - Point
    - Orient
    - Scale
    - Aim
    - Attach: surface or mesh object
post pone, need to rethink this

# New --->>
* A Component is a kind of entity in rig system.
Component can be interface for rigger and animator.
Component can be hooked to other component.
Component master is framework which contain other components into single root hierarchy structure.
Empty component is possible.
Component with guide but no plugin data will only rebuild guide and reult as bind joint.
  Ex:
    - Limb component, Arm component(inherit from Limb), Leg component(Limb)
    - Spine component, Tail component, Head component, Finger component
    - Wing component, Hair component, Framework component, etc
* A plug-in can be attached to a component.
In scene, plugin discovered by retrieving or processing data from guide.
  Ex:
    - IK/FK Arm plugin, IK Spine plugin, Super placer plugin, Corrective joint plugin, etc
* A Guide is initial data input for component plugin when building rig.
Guide can be from curve or joint object as representation.

# Master component(Framework component): [Super placer plugin]
    # Component(Spine component): [Twist plugin, IK/FK Spine plugin]
    # Component(Arm component): [IK/FK Arm plugin, Twist plugin, Soft IK plugin]
    # Component(Leg component): [IK/FK Leg plugin, Twist plugin, Soft IK plugin]
    # Component(Neck component): [FK plugin]
    # Component(Head component): [FK plugin]
    # Component(Eye component): [Eyelid plugin]
    # Component(Jaw component): [FK plugin]
"""
import abc


class AbstractNode:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_pynode(self):
        pass


class AbstractComponent:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._root_component = False
        self._plugin_collection = []
        self._guides = []
        self._hook_to = None
        self._component_members = []

    @property
    def is_root(self):
        return self._root_component

    def add_plugin(self, comp_plugin):
        # TODO: check compatibility
        if comp_plugin not in self._plugin_collection:
            self._plugin_collection.append(comp_plugin)

    def remove_plugin(self, index):
        self._plugin_collection.remove(index)

    @abc.abstractmethod
    def create(self):
        pass

    @abc.abstractmethod
    def build(self):
        pass


class AbstractPlugin:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass


class AbstractGuide:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass


class RootComponent(AbstractComponent):

    def __init__(self):
        super(RootComponent, self).__init__()
