import json
from . frame import Frame
from .euler_sim2 import EulerSimulator

class SimulatorInterface():
    """A class that facilitates the stateful encapsulation of a simulator. It enables easy backwards/forwards traversal and importing/exporting of a simulation."""

    def __init__(self, simulator, interval, start_state):
        """Initializes the interface with the given simulator and time interval between frames (in ms)"""
        self._start_state = start_state
        self._frames = []
        self._sim = simulator
        self._interval = interval

    def set_interval(self, interval):
        """Sets the interval between frames to a new value"""
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

    def current_frame(self):
        """Returns the current frame"""
        if self._frames:
            return self._frames[-1]
        return self._start_state

    def frame_generator(self):
        """Returns a generator that yields all frames in sequential order"""
        i = 0
        while True:
            if (i >= len(self.frames())): 
                i = 0
            yield self.frames()[i]
            i +=1
    
    def export_frames(self):
        """Returns a serialized (JSON) string representing the internal list of frames"""
        return json.dumps([frame.tojson() for frame in self.frames()])

    def import_frame(self, frame_data):
        """Imports and appends the frame represented by a serialized (JSON) string"""
        self._frames.append(Frame.fromjson(frame_data, EulerSimulator))

    def import_frames(self, data):
        """Imports a list of frames from a string containing a serialized (JSON) representation of frame history."""
        frames = json.loads(data)
        for frame in frames:
            self.import_frame(frame)


    
