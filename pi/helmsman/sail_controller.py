import locator
from pi.interval_repeater import IntervalRepeater
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver


class SailController(IntervalRepeater):
    def __init__(self, driver: AbstractBoatDriver, go_fast: bool = True, interval=0.1, **kwargs):
        """
        Args:
            driver: An instance of a boat driver
            go_fast: Whether or not the controller will initally try to maximize speed

        """
        super().__init__(interval=interval, **kwargs)
        self._driver = driver
        self._go_fast = go_fast
        self._start_interval_repeater()

    @classmethod
    def create(cls, config) -> 'SailController':
        """
        Constructs an instance of a SailController
        Args:
            config: a dict that contains optional parameters for the SailController and IntervalRepeater constructors
        """
        return cls(locator.get_driver(), **config)

    def _interval_process(self):
        if self.go_fast:
            self._maximize_speed()
        else:
            self._minimize_speed()

    @property
    def go_fast(self) -> bool:
        return self._go_fast

    @go_fast.setter
    def go_fast(self, new_val: bool):
        self._go_fast = new_val

    def _maximize_speed(self):
        # This is a simple heuristic, can be replaced
        sail_angle = min(abs(self._driver.get_wind_dir_rel()) / 2, 90)
        self._driver.set_sail(sail_angle)

    def _minimize_speed(self):
        # Removes all slack from the mainsheet
        self._driver.set_sail(0)
