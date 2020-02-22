from simple_pid import PID
from time import sleep
from pi.navutils import shortest_path
from pi.interval_repeater import IntervalRepeater
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver
import threading
import locator


def start(driver, get_desired_heading, is_enabled, interval=2, p=5, i=0.01, d=0):
    """
    Starts a PID in a seperate thread that attempts to always reach a desired heading. The thread will close if the program exits.

    Parameters:
        driver: An instance of an AbstractBoatDriver
        get_desired_heading; A method that returns the desired heading
        interval: The time between pid adjustments in seconds. Default is 0.1 seconds
        p: Proportional coefficeint of PID
        i: Integral coefficient of PID
        d: Differential coefficient of PID
    """
    pid = PID(p, i, d, sample_time=interval, output_limits=(-45, 45))
    pid.setpoint = 0
    # thread is created as a daemon so that it will close if the program exits
    control_thread = threading.Thread(target=rudder_controller, daemon=True, args=(
        driver, pid, interval, get_desired_heading, is_enabled))
    control_thread.start()


# TODO ensure the boat never tries to reach the desired_heading by passing through the no-go zone
# Note that we only read the desired heading, and the interval is small, so for our purposes this is threadsafe


def rudder_controller(driver, pid, interval, get_desired_heading, is_enabled):
    while True:
        if is_enabled():
            try:
                output = pid(shortest_path(
                    get_desired_heading(), driver.get_heading()))
                # print('Currently at', driver.get_heading(), 'want to get to', get_desired_heading(), 'by going',
                # shortest_path(get_desired_heading(), driver.get_heading()), 'by setting rudder to', output)
                driver.set_rudder(output)
            except Exception:
                print('rudder_controller could not read from driver')
        sleep(interval)


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
        self._start_interval_repeater

    @classmethod
    def create(cls, config) -> 'RudderController':
        """
        Constructs an instance of a RudderController
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
