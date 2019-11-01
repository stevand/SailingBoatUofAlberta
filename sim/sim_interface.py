import json
from frame import Frame

class SimulatorInterface():
    """A class that facilitates the stateful encapsulation of a simulator. It enables easy backwards/forwards traversal and importing/exporting of a simulation."""

    def __init__(self, simulator, interval, start_state):
        """Initializes the interface with the given simulator and time interval between frames (in ms)"""
        self._start_state = start_state
        self._frames = []
        self._sim = simulator
        self._interval = interval

    def simulate(self, control, env):
        """Runs the simulator and returns the next frame"""
        if self._frames:
            prev_state = self._frames[-1].state
        else:
            prev_state = self._start_state
            
        next_state = self._sim.simulate(prev_state, control, env, self._interval)
        new_frame = Frame(next_state, control, env)
        self._frames.append(new_frame)
        return new_frame

    def frames(self):
        """Returns a list of all frames in sequential order. Pinky promise not to change anything"""
        return self._frames
    
    def export_states(self):
        """Returns a serialized (JSON) string representing the internal list of s   tates"""
        return json.dumps(self._states)

    def import_states(self, states):
        """Imports a serialized (JSON) string representing a list of states, and goes to the beggining of it"""
        self._states = json.loads(states)


    
