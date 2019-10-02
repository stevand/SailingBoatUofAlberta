

class Navigator:
    def __init__(self, abstract_driver):
        self._driver = abstract_driver
        # Current side of the boat the wind is coming off of
        self.tack = None
        # Sail tolerance is how close to the wind the boat is able to sail
        self.tolerance = 30
        # Error is the maximum allowed amount of heading error
        self.error = 5
        # Initialize winch to 0 Degrees
        self._driver.sail(0)

    def adjust(self):
        """Adjusts the angle of the sails to maximize velocity on current heading"""
        self._driver.sail(min(abs(self._get_wind_rel() / 2)), 90)

    def turn(self, new_heading):
        """Turns the boat to face the new_heading. Returns -1 if not possible, 1 otherwise"""
        # Get distance between new heading and wind direction
        if abs(self._driver.wind_direction() - new_heading) < self.tolerance:
            return -1
        else:
            # If you need to turn to port
            if new_heading > (self._driver.heading() + 180):
                while abs(self._driver.heading() - new_heading) > self.error:
                    # Turn port
                    self.adjust()
                    pass
            # If you need to turn to starboard
            else:
                while abs(self._driver.heading() - new_heading) > self.error:
                    # Turn starboard
                    self.adjust()
                    pass

    def turn_rel(self, degrees):
        """Turns the boat relative to its current heading
        Starboard turn ranges from (0 -> 180]
        Port turn ranges from (0 -> -180]
        """
        new_heading = (self._driver.heading() + degrees) % 360
        self.turn(new_heading)
        return None

    def _get_wind_rel(self):
        """
        Gets wind relative to the boat based upon current magnetic wind reading and IMU magnetic reading
        A negative number from (0 -> -180] implies your on a port tack
        A positive number from (0 ->  180] implies your on a starboard tack
        """
        # If wind direction is greater then boat direction
        if self._driver.wind_direction() > self._driver.heading():
            # Get shortest wind angle relative to boat
            if self._driver.wind_direction() > ( self._driver.heading() + 180 ):
                wind_rel = -(360 - self._driver.wind_direction() + self._driver.heading())
            else:
                wind_rel = self._driver.wind_direction() - self._driver.heading()
        # If boat direction is greater then wind direction
        else:
            # Get shortest wind angle relative to the boat
            if self._driver.heading() > ( self._driver.wind_direction() + 180):
                wind_rel = (360 - self._driver.heading() + self._driver.wind_direction())
            else:
                wind_rel = -(self._driver.heading() - self._driver.wind_direction())
        if wind_rel > 0:
            self.tack = "STARBOARD"
        else:
            self.tack = "PORT"
        return wind_rel





