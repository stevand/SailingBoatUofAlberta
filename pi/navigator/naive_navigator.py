from . import AbstractNavigator
from threading import Thread
from time import sleep
from pi.navutils import dist, dir_to_waypoint
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver
from pi.helmsman import Helmsman
import math

class NaiveNavigator(AbstractNavigator):
    def __init__(self, driver: AbstractBoatDriver, helmsman: Helmsman, **kwargs):
        super().__init__(driver, helmsman,  **kwargs)

    def _navigate_to_curr_waypoint(self):
        if not self.get_waypoint():
            self._helmsman.maximize_speed = False
        else:
            self._helmsman.maximize_speed = True
            heading = dir_to_waypoint(*self._driver.get_position(), *self.get_waypoint())
            self._helmsman.turn(heading)



