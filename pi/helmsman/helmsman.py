class Helmsman:
    def __init__(self, driver):
        self._driver = driver
        # Current side of the boat the wind is coming off of
        self.tack = None
        # Sail tolerance is how close to the wind the boat is able to sail
        self.tolerance = 30
        # Error is the maximum allowed amount of get_heading error
        self.error = 1
        # Initialize winch to 0 Degrees
        self._driver.set_sail(0)

    def adjust(self):
        """Adjusts the angle of the sails to maximize velocity on current get_heading"""
        self._driver.set_sail(min(abs(self._driver.get_rel_wind_dir(), 90)))

    def turn(self, new_heading):
        """Turns the boat to face the new_heading. Returns -1 if not possible, 1 otherwise"""
        # Get distance between new get_heading and wind direction
        if abs(self._driver.get_rel_wind_dir) < self.tolerance:
            return -1

        # If you need to turn to port
        if new_heading > (self._driver.get_heading() + 180):
            while abs(self._driver.get_heading() - new_heading) > self.error:
                # Turn port
                self.adjust()
                pass
        # If you need to turn to starboard
        else:
            while abs(self._driver.get_heading() - new_heading) > self.error:
                # Turn starboard
                self.adjust()
                pass

    def turn_rel(self, degrees):
        """Turns the boat relative to its current get_heading
        Starboard turn ranges from (0 -> 180]
        Port turn ranges from (0 -> -180]
        """
        new_heading = (self._driver.get_heading() + degrees) % 360
        self.turn(new_heading)
        return None

    def tack():
        if wind_rel > 0:
            return "STARBOARD"
        else:
            return "PORT"





