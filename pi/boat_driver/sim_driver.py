from .abstract_boat_driver import AbstractBoatDriver
import math

# TODO implement get_wind_dir
class SimDriver(AbstractBoatDriver):
    # get_frame is a callback that returns the most recent frame
    def __init__(self, get_frame, **kwargs):
        super()
        self._get_frame = get_frame

    def get_wind_dir(self):
        pass

    def get_heading(self):
        return self._get_frame().state.theta

    def get_position(self):
        return (self._get_frame().state.x, self._get_frame().state.y)

    def status(self):
        """Returns the status of the boat"""
        return {
            'wind_dir': self.get_wind_dir(),
            'rel_wind_dir': self.get_wind_dir_rel(),
            'heading': self.get_heading(),
            'position': self.get_position(),
            'sail': self.get_sail(),
            'rudder': self.get_rudder()
        }