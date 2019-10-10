import abc

class AbstractBoatDriver(abc.ABC):
    @abc.abstractmethod
    def close(self):
        """Gracefully closes the driver and all serial connections. Call before exiting."""
        pass

    @abc.abstractmethod
    def get_wind_dir(self):
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
        """Sets the angle of the rudder
        (0 -> -45] points the rudder the farther to the right
        (0 -> 45] points the rudder the farther to the left
        0 points it straight ahead."""
        pass

    def get_sail(self):
        """Returns the angle of the sail (0, 90)"""
        pass

    def get_rudder(self):
        """Returns the angle of the rudder (-45, 45)"""
        pass

    def get_rel_wind_dir(self):
        """
        Gets the wind direction relative to the boat based upon current magnetic wind reading and IMU magnetic reading
        A negative number from (0 -> -180] implies you're on a port tack
        A positive number from (0 ->  180] implies you're on a starboard tack
        """
        # If wind direction is greater then boat direction
        abs_dir = self.get_wind_dir()
        heading = self.get_heading()
        if abs_dir > heading:
            # Get shortest wind angle relative to boat
            if abs_dir > (heading + 180):
                wind_rel = -(360 - abs_dir + heading)
            else:
                wind_rel = abs_dir - heading
        # If boat direction is greater then wind direction
        else:
            # Get shortest wind angle relative to the boat
            if heading > (abs_dir + 180):
                wind_rel = (360 - heading + abs_dir)
            else:
                wind_rel = -(heading - abs_dir)
        return wind_rel

    def status(self):
        """Returns the status of the boat"""
        return {
            'wind_dir': self.get_wind_dir(),
            'rel_wind_dir': self.get_rel_wind_dir(),
            'heading': self.get_heading(),
            'position': self.get_position(),
            'sail': self.get_sail(),
            'rudder': self.get_rudder()
        }