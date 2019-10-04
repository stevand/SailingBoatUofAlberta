import abc


class AbstractBoatDriver(abc.ABC):
    @abc.abstractmethod
    def close(self):
        """Gracefully closes the driver and all serial connections. Call before exiting."""
        pass

    @abc.abstractmethod
    def get_wind_direction(self):
        """Returns the direction of the wind [0, 359], with 0 being North and 180 being South"""
        pass

    @abc.abstractmethod
    def get_heading(self):
        """Returns the heading of the boat [0, 359], with 0 being North and 180 being South"""
        pass

    @abc.abstractmethod
    def get_position(self):
        """Returns the gps coordinates of the boat as a tuple (x, y)"""
        pass

    @abc.abstractmethod
    def set_sail(self, angle):
        """Tightens/loosens the sheets so that the sails may reach the given angle (0-90) away from the center"""
        pass

    @abc.abstractmethod
    def set_rudder(self, angle):
        """Sets the angle (-45, 45) where -45 points the rudder the farthest it can go to the right, 45 points the rudder the farthest it can go to the left and 0 points it straight ahead."""
        pass
