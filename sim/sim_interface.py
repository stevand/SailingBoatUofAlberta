import json

class SimulatorInterface():
    """A class that facilitates the stateful encapsulation of a simulator. It enables easy backwards/forwards traversal and importing/exporting of a simulation."""

    def __init__(self, simulator, interval):
        """Initializes the interface with the given simulator and time interval between frames (in seconds)"""
        self._states = []
        self._sim = simulator
        self._interval = interval

    def simulate(self):
        """Runs the simulator and returns the next state"""
        old_state = self._states[-1]
        next_state = self._sim.next_state(old_state, self._interval)
        self._states.append(next_state)
        return current_state
    
    def get_state(self, frame_num=None, time=None):
        """Fetches the state at the given frame_num or time (in seconds from start). If neither are specified, returns the current state"""
        if time is not None:
            return self._states[frame_num(time)]
        return self._states[-1]
    
    def time(self, frame_num=None):
        """Returns the total time elapsed at the given frame_num. If frame_num is not specified, returns the current time"""
        if frame_num is None:
            frame_num = len(self._states) - 1
        return frame_num * self._interval

    def frame_num(self, time=None):
        """Returns the frame_num at the given time. If time is not specified, returns the current frame_num"""
        if time is None:
            time = time()
        return time // self._interval

    def goto(self, frame_num=None, time=None):
        """Resets the simulator to the given frame_num or time"""
        if frame_num is not None:
            self._states = self._states[:frame_num+1]
        elif time is not None:
            frame_num = frame_num(time)
            self._states = self._states[:frame_num+1]
    
    def export_states(self):
        """Returns a serialized (JSON) string representing the internal list of states"""
        return json.dumps(self._states)

    def import_states(self, states):
        """Imports a serialized (JSON) string representing a list of states, and goes to the beggining of it"""
        self._states = json.loads(states)


    
