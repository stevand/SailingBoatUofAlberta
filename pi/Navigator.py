class Navigator():
    def __init__(self, driver):
        self._driver = driver

    def adjust(self):
        """Adjusts the angle of the sails to maximize velocity on current heading"""

    def turn(self, new_heading):
        """Turns the boat to face the new_heading. Returns -1 if not possible, 1 otherwise"""
    
    def turn_rel(self, degrees):
        """Turns the boat by the given number of degrees clockwise. Returns -1 if not possible, 1 otherwise"""
        absolute = self._driver.heading() + degrees
        return self.turn(absolute)

