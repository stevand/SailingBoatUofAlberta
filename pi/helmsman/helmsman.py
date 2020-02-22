from . import rudder_controller, SailController
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver
import locator


class Helmsman:
    def __init__(self, driver: AbstractBoatDriver, sail_ctrl: SailController = None, **kwargs):
        self._driver = driver
        # Sail tolerance is how close to the wind the boat is able to sail
        self.tolerance = 30
        # Error is the maximum allowed amount of get_heading error
        self.error = 1
        self.desired_heading = 90

        # Starts rudder controller
        self.rudder_controller_enabled = kwargs['rudder_controller']['enabled']
        rudder_controller.start(driver, lambda: self.desired_heading,
                                lambda: self.rudder_controller_enabled, interval=kwargs['rudder_controller']['interval'])

        self._sail_controller = sail_ctrl

    @classmethod
    def create(cls, config) -> 'Helmsman':
        """
        Constructs an instance of a Helmsman.

        config should be a dict with the following entries:
            "sail_controller": a SailController config dict
            "rudder_controller": a RudderController config dict
        """
        return Helmsman(locator.get_driver(), locator.get_sail_controller(), **config)

    def turn(self, new_heading):
        """Turns the boat to face the new_heading. Returns False if the new_heading is in irons, True otherwise"""
        # Get shortest distance between new_heading and wind direction
        wind_dir = self._driver.get_wind_dir()
        high = max(wind_dir, new_heading)
        low = min(wind_dir, new_heading)
        if high > (low + 180):
            diff = 360 - high + low
        else:
            diff = high - low

        # If new heading is in irons
        # if diff < self.tolerance:
        #    return False

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

    def status(self):
        return {
            'tolerance': self.tolerance,
            'desired_heading': self.desired_heading,
            'maximize_speed': self.maximize_speed,
            'rudder_controller': {
                'enabled': self.rudder_controller_enabled
            },
            'sail_controller': {
                'enabled': self.sail_controller_enabled
            }
        }

    @property
    def sail_controller_enabled(self) -> bool:
        return self._sail_controller.enabled

    @sail_controller_enabled.setter
    def sail_controller_enabled(self, new_val: bool):
        self._sail_controller.enabled = new_val

    @property
    def maximize_speed(self) -> bool:
        return self._sail_controller.go_fast

    @maximize_speed.setter
    def maximize_speed(self, new_val: bool):
        self._sail_controller.go_fast = new_val
