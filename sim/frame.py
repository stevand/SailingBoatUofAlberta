import json


class Frame():
    """An immutable data structure designed to hold the state, control and environmental data of a particular instant"""
    def __init__(self, state, control, env):
        self._state = state
        self._control = control
        self._env = env
    
    @property
    def state(self):
        return self._state
    
    @property
    def control(self):
        return self._control
    
    @property
    def env(self):
        return self._env

    def tojson(self):
        return json.dumps(
            {
                "state": self._state._asdict(),
                "control": self._state._asdict(),
                "env": self._state._asdict()
            }
        )

    def __str__(self):
        return "state: {}\n control: {}\n env: {}".format(self._state, self._control, self._env)