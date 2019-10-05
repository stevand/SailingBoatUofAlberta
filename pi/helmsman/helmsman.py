from helmsman import rudder_controller


class Helmsman:
    def __init__(self, driver):
        self._driver = driver
        # Sail tolerance is how close to the wind the boat is able to sail
        self.tolerance = 30
        # Error is the maximum allowed amount of get_heading error
        self.error = 1
        # Starts rudder controller
        self.desired_heading = 0
        rudder_controller.start_controller(driver, lambda: self.desired_heading)
        # Initialize winch to 0 Degrees
        self._driver.set_sail(0)

    def adjust(self):
        """Adjusts the angle of the sails to maximize velocity on current get_heading"""
        self._driver.set_sail(min(abs(self._driver.get_rel_wind_dir(), 90)))

    def turn(self, new_heading):
        """Turns the boat to face the new_heading. Returns False if the new_heading is in irons, True otherwise"""
        # Get shortest distance between new_heading and wind direction
        wind_dir = self._driver.get_wind_dir()
        high = max(wind_dir, new_heading)
        low = min(wind_dir, new_heading)
        if high > (low + 180):
            diff = abs((low - high) % 360)
        else:
            diff = high - low

        # If new heading is in irons
        if diff < self.tolerance:
            return False

        # Else if new heading is valid
        self.desired_heading = new_heading
        return True

    def turn_rel(self, degrees):
        """Turns the boat relative to its current get_heading
        Starboard turn ranges from (0 -> 180]
        Port turn ranges from (0 -> -180]
        """
        new_heading = (self._driver.get_heading() + degrees) % 360
        self.turn(new_heading)
        return None

    def tack(self):
        """Returns the side of the boat the wind is coming off of """
        if self._driver.get_rel_wind_dir() > 0:
            return "STARBOARD"
        else:
            return "PORT"
