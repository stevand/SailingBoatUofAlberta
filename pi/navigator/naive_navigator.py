from . import AbstractNavigator
from threading import Thread
from time import sleep
import math

def dist(loc1, loc2):
    """Finds the distance between loc1 and loc2"""
    return ((loc2[0]-loc1[0])**2 + (loc2[1]-loc1[1])**2)**0.5

def angle_between(loc1, loc2):
    """Finds the angle to turn the boat at loc1 to reach loc2"""
    theta = math.atan2(loc2[1]-loc1[1], loc2[0]-loc1[0])
    # converting to boat driver's polar system
    # TODO change driver to use normal angles
    return (-1 * math.degrees(theta) + 90) % 360


def navigate(interval, get_waypoint, driver, helmsman, is_enabled, waypoint_dist, waypoint_reached):
    while True:
        if is_enabled():
            next_waypoint = get_waypoint()
            boat = driver.get_position()
            while next_waypoint and dist(boat, next_waypoint) < waypoint_dist:
                waypoint_reached()
                next_waypoint = get_waypoint()

            if next_waypoint:
                helmsman.maximize_speed = True
                goto = angle_between(boat, next_waypoint)
                helmsman.turn(goto)
                #print(goto, helmsman.desired_heading)
            else:
                helmsman.maximize_speed = False
        sleep(interval)


class NaiveNavigator(AbstractNavigator):
    def __init__(self, driver, helmsman, interval=0.3, waypoint_dist=0.4, **kwargs):
        super().__init__(driver, helmsman=helmsman, **kwargs)

        # interval is time between updating helmsman direction
        self.interval = interval
        # waypoint_dist is the distance at which the boat is considered to have reached the waypoint
        self.waypoint_dist = waypoint_dist


        thread = Thread(target=navigate, daemon=True,
            args=[interval, self.get_waypoint, driver, helmsman, lambda: self._enabled, waypoint_dist, self.del_waypoint])
        thread.start()

