import json
from collections import namedtuple
from .euler_sim2 import EulerSimulator
from .simulator import Simulator
from typing import Type


class Frame():
    """An immutable data structure designed to hold the state, control and environmental data of a particular instant"""

    def __init__(self, state, control, env):
        self._state = state
        self._control = control
        self._env = env

    @property
    def state(self) -> namedtuple:
        return self._state

    @property
    def control(self) -> namedtuple:
        return self._control

    @property
    def env(self) -> namedtuple:
        return self._env

    def to_json(self) -> str:
        return json.dumps(
            {
                "state": self._state._asdict(),
                "control": self._control._asdict(),
                "env": self._env._asdict()
            }
        )

    @classmethod
    def from_dict(cls, frame_dict, sim_class: Type[Simulator] = EulerSimulator) -> 'Frame':
        """
        Creates a Frame from a nested dict that contains state, control and env.
        The Frame will have state, control and env named tuples that correspond to the specified simulator, which is euler_sim2 by default.
        """
        return cls(
            sim_class.state(**frame_dict['state']),
            sim_class.control(**frame_dict['control']),
            sim_class.env(**frame_dict['env'])
        )

    @classmethod
    def from_json(cls, data, Simulator) -> 'Frame':
        data = json.loads(data)
        state = Simulator.state(**(data['state']))
        control = Simulator.control(**(data['control']))
        env = Simulator.env(**data['env'])
        return cls(state, control, env)

    def __str__(self) -> 'str':
        return "state: {}\n control: {}\n env: {}".format(self._state, self._control, self._env)
