from . import Voter
from pi import navutils


class WaypointVoter(Voter):
    def __init__(self, driver, get_waypoint):
        """
        Votes based on how closely a given heading adheres to the straight-line path towards the current waypoint.
        Args:
            driver: An instance of a BoatDriver
            get_waypoint: a function that returns the current waypoint
        """
        super().__init__(driver)
        self._get_waypoint = get_waypoint

    def vote(self, heading):
        optimal = navutils.dir_to_waypoint(
            *self._driver.get_position(), *self._get_waypoint())
        diff = navutils.smallest_angle_between(optimal, heading)
        return max(1 - diff / 90, 0)
