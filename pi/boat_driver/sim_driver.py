from .abstract_boat_driver import AbstractBoatDriver

class SimDriver(AbstractBoatDriver):
    # get_frame is a callback that returns the most recent frame
    def __init__(self, get_frame=None, **kwargs):
        super()
        self.get_frame = get_frame

    def get_wind_dir(self):
        return 0 # simulator currently can only have wind coming from due north

    def get_heading(self):
        return self.get_frame().state.theta

    def get_position(self):
        return (self.get_frame().state.x, self.get_frame().state.y)

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