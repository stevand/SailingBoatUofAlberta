import abc
from pi.boat_driver import AbstractBoatDriver
from pi.helmsman import Helmsman
from threading import Thread
from pi.navutils import dist
from time import sleep
from pi.interval_repeater import IntervalRepeater
from typing import List, Tuple
import locator

Waypoint = Tuple[int, int]

class AbstractNavigator(IntervalRepeater, abc.ABC):
    """
    Abstraction layer built on top of a BoatDriver and (optionally) a Helmsman.
    Should be able to navigate to waypoints that are passed to it.
    """

    def __init__(self, driver: AbstractBoatDriver, helmsman: Helmsman, enabled: bool = True, interval: float = 0.5, waypoint_dist: float = 0.2, **kwargs):
        super().__init__(interval=interval, enabled=enabled)
        self._driver = driver
        self._helmsman = helmsman
        self.__waypoints = []
        self.__last_waypoint = self._driver.get_position()
        self.waypoint_dist = waypoint_dist
        self._start_interval_repeater()

    @classmethod
    def create(cls, config):
        """
        Creates a new instance of an AbstractNaviagor, using the locator to get any dependencies.
        Args:
            config: a dict containing any optional parameters for self.__init__
        """
        return cls(locator.get_driver(), locator.get_helmsman(), **config)

    def _interval_process(self):
        """
        Repeatedly exectuted by IntervalRepeater mixin while enabled
        """
        self._clear_reached_waypoints()
        self._navigate_to_curr_waypoint()

    def _clear_reached_waypoints(self):
        """
        Clears all waypoints that are within waypoint_dist of the boat
        """
        next_waypoint = self.get_waypoint()
        boat_pos = self._driver.get_position()
        while (next_waypoint and dist(boat_pos, next_waypoint) < self.waypoint_dist):
            self.del_waypoint()
            next_waypoint = self.get_waypoint()

    @abc.abstractmethod
    def _navigate_to_curr_waypoint(self):
        """
        This method should contain the navigator's main logic and will be executed at regular intervals while the navigator is enabled.
        The current waypoint can be accessed with self.get_waypoint()
        """
        pass

    def add_waypoint(self, waypoint: Waypoint, i: int = -1) -> int:
        """
        Adds the given waypoint to the current waypoint queue (at the end, by default).
        Args:
            waypoint: The waypoint to add
            i: (optional) The position in the queue that the waypoint should be added
        Returns:
            The new length of the waypoint queue
        """
        if i == -1:
            self.__waypoints.append(waypoint)
        else:
            self.__waypoints.insert(i, waypoint)
        return len(self.__waypoints)

    def del_waypoint(self, i: int = 0) -> int:
        """
        Deletes the i-th waypoint in the waypoint queue
        Args:
            i: The position of the waypoint to delete
        Returns:
            The new length of the waypoint queue
        """
        self.__last_waypoint = self.__waypoints.pop(i)
        return len(self.__waypoints)

    def view_waypoints(self) -> List[Waypoint]:
        """
        Returns a copy of the current waypoint queue in order.
        To edit the waypoint queue, use the add_waypoint and del_waypoint methods
        """
        return [waypoint for waypoint in self.__waypoints]

    def get_waypoint(self, i=0):
        """
        Returns the i-th waypoint, or the next waypoint if i is not specified
        """
        if self.__waypoints:
            return self.__waypoints[i]
        return None

    @property
    def last_waypoint(self) -> Waypoint:
        """
        Returns the last reached waypoint, or the boat's initial location if not waypoint has been reached yet
        """
        return self.__last_waypoint
