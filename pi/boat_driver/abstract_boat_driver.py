import abc
from typing import Dict


class AbstractBoatDriver(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        """Initializes the boat, setting sails and rudder to 0 degrees"""
        self.set_sail(0)
        self.set_rudder(0)
        self.__sail = 0
        self.__rudder = 0

    @classmethod
    def create(cls, config: Dict):
        """
        Creates a new instance of an AbstractBoatDriver.
        Args:
            config: a dict containing any optional parameters for the constructor
        """
        return cls()

    @abc.abstractmethod
    def close(self):
        """Gracefully closes the driver and all serial connections. Call before exiting."""
        pass

    @abc.abstractmethod
    def get_wind_dir(self):
        """Returns the relative direction of the wind [0, 359], with 0/359 pointing straight ahead and 180 pointing straight behind"""
        pass

    @abc.abstractmethod
    def get_heading(self):
        """Returns the heading of the boat [0, 359], with 0 being East, 90 North and 180 being West"""
        pass

    @abc.abstractmethod
    def get_position(self):
        """Returns the gps coordinates of the boat as a tuple (x, y)"""
        pass

    @abc.abstractmethod
    def get_wind_speed(self):
        """Returns the apparent wind speed, as measured from the boat"""
        pass

    @abc.abstractmethod
    def set_sail(self, angle):
        """Tightens/loosens the sheets so that the sails may reach the given angle (0-90) away from the center."""
        if angle < 0 or angle > 90:
            raise ValueError('angle should be in [-45, 45]')
        self.__sail = angle

    @abc.abstractmethod
    def set_rudder(self, angle):
        """Sets the angle of the rudder. 
        Negative values will turn the boat left and positive values will turn the boat right.
        (0 -> -45] points the rudder the farther to the right
        (0 -> 45] points the rudder the farther to the left
        0 points it straight ahead."""
        if abs(angle) > 45:
            raise ValueError('angle should be in [-45, 45]')
        self.__rudder = angle

    def get_sail(self):
        """Returns the angle of the sail (0, 90)"""
        return self.__sail

    def get_rudder(self):
        """Returns the angle of the rudder (-45, 45)"""
        return self.__rudder

    def get_wind_dir_rel(self):
        """
        Gets the wind direction relative to the boat based upon wind vane
        A negative number from (0 -> -180] implies you're on a port tack
        A positive number from (0 ->  180] implies you're on a starboard tack
        """
        wind = self.get_wind_dir()
        if wind > 180:
            wind = -(360-wind)
        return wind

    def get_wind_dir_true(self):
        """
        Gets the true magnetic wind direction calculated by using the boats compass and get_wind_dir_rel()
        """
        return (self.get_wind_dir_rel() + self.get_heading()) % 360

    def status(self):
        """Returns the status of the boat"""
        return {
            'wind_dir': self.get_wind_dir(),
            'wind_speed': self.get_wind_speed(),
            'rel_wind_dir': self.get_wind_dir_rel(),
            'heading': self.get_heading(),
            'position': self.get_position(),
            'sail': self.get_sail(),
            'rudder': self.get_rudder()
        }
