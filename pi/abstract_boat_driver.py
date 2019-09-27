import abc

class AbstractBoatDriver(abc.ABC):
    @abc.abstractmethod
    def wind_direction(self):
        """Returns the direction of the wind [0, 359], with 0 being North and 180 being South"""

    @abc.abstractmethod
    def heading(self):
        """Returns the heading of the boat [0, 359], with 0 being North and 180 being South"""

    @abc.abstractmethod
    def position(self):
        """Returns the gps coordinates of the boat as a tuple (x, y)"""

    @abc.abstractmethod
    def sail(self, angle):
        """Sets the angle of the sail to the given angle"""

    @abc.abstractmethod
    def rudder(self, angle):
        """Sets the angle of the rudder to the given angle"""

    