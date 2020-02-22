from . import AbstractBoatDriver
from math import pi
import locator

class SimDriver(AbstractBoatDriver):
    # get_frame is a callback that returns the most recent frame
    def __init__(self, get_frame=None, **kwargs):
        super().__init__(**kwargs)
        self.get_frame = get_frame

    @classmethod
    def create(cls, config):
        return SimDriver(get_frame=locator.get_sim_interface().current_frame, **config)

    def get_wind_dir_true(self):
        return 90

    def get_wind_dir(self):
        return (self.get_heading() - 90) % 360 # simulator currently can only have wind coming from due north

    def get_heading(self):
        return self.get_frame().state.theta / pi * 180 % 360

    def get_position(self):
        return self.get_frame().state.x, self.get_frame().state.y

    def close(self):
        pass

    def get_wind_speed(self):
        return self.get_frame().env.V

    def set_rudder(self, angle):
        super().set_rudder(angle)

    def set_sail(self, angle):
        super().set_sail(angle)

    def status(self):
        """Returns the status of the boat"""
        return {
            'wind_dir': self.get_wind_dir(),
            'rel_wind_dir': self.get_wind_dir_rel(),
            'true_wind_dir': self.get_wind_dir_true(),
            'heading': self.get_heading(),
            'position': self.get_position(),
            'sail': self.get_sail(),
            'rudder': self.get_rudder()
        }