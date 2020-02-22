from simple_pid import PID
from time import sleep
from pi.navutils import shortest_path
from pi.interval_repeater import IntervalRepeater
from pi.boat_driver import AbstractBoatDriver
import threading
import locator


class RudderController(IntervalRepeater):
    def __init__(self, driver: AbstractBoatDriver, desired_heading=0, interval=0.1, p=1, i=0.01, d=0, **kwargs):
        """
        Starts a PID in a seperate thread that attempts to always reach a desired heading. The thread will close if the program exits.

        Parameters:
        driver: An instance of an AbstractBoatDriver
        desired_heading: The initial desired heading
        interval: The time between pid adjustments in seconds.
        p: Proportional coefficeint of PID
        i: Integral coefficient of PID
        d: Differential coefficient of PID
        """
        super().__init__(interval=interval, **kwargs)
        self._desired_heading = desired_heading
        self._driver = driver
        self._pid = PID(p, i, d, sample_time=interval, output_limits=(-45, 45))
        # will try to bring difference between current and desired heading to 0
        self._pid.setpoint = 0
        self._start_interval_repeater()

    @classmethod
    def create(cls, config) -> 'RudderController':
        """
        Constructs an instance of a RudderController using the locator to get any dependencies.
        Args:
            config: a dict that contains optional parameters for the RudderController and IntervalRepeater constructors
        """
        return cls(locator.get_driver(), **config)

    def _interval_process(self):
        angle_to_desired = shortest_path(
            self._desired_heading, self._driver.get_heading())
        rudder_angle = self._pid(angle_to_desired)
        self._driver.set_rudder(rudder_angle)

    @property
    def desired_heading(self) -> int:
        return self._desired_heading

    @desired_heading.setter
    def desired_heading(self, new_val: int):
        self._desired_heading = new_val
