from . import Voter
from shapely.geometry import LineString, Point
from shapely.ops import nearest_points
from pi.navutils import smallest_angle_between, dir_to_waypoint


class ChannelVoter(Voter):
    def __init__(self, driver, get_path, channel_width=1):
        """
        Initializes the channel voter with the given driver and method that returns the current path (start, end)
        """
        super().__init__(driver)
        self._get_path = get_path
        self._channel_width = channel_width

    def vote(self, heading):
        start, end = self._get_path()
        boat = Point(self._driver.get_position())
        path = LineString([start, end])
        # closest point on the path to the boat
        nearest = nearest_points(boat, path)[1]

        # votes max when boat is within channel_width of the past
        if boat.distance(path) < self._channel_width:
            return 1

        # if outside of channel, votes for headings within 45 degrees of the line perpendicular to the path
        if smallest_angle_between(heading, dir_to_waypoint(*self._driver.get_position(), nearest.x, nearest.y)) < 45:
            return 1
        else:
            return 0
