import abc

class AbstractNavigator(abc.ABC):
    """
    Abstraction layer built on top of a BoatDriver and (optionally) a Helmsman.
    Should be able to navigate to waypoints that are passed to it.
    """

    @abc.abstractmethod
    def __init__(self, driver, helmsman, enabled=True, **kwargs):
        """
        Initializes the navigator with the given driver and helmsman.
        """
        self._driver = driver
        self._helmsman = helmsman
        self._waypoints = []
        self._enabled = False

    def add_waypoint(self, waypoint, i=-1) -> int:
        """
        Adds the given waypoint to the current waypoint queue (at the end, by default).
        Args:
            waypoint: The waypoint to add
            i: (optional) The position in the queue that the waypoint should be added
        Returns:
            The new length of the waypoint queue
        """
        if i == -1:
            self._waypoints.append(waypoint)
        else:
            self._waypoints.insert(i, waypoint)
        return len(self._waypoints)

    def del_waypoint(self, i) -> int:
        """
        Deletes the i-th waypoint in the waypoint queue
        Args:
            i: The position of the waypoint to delete
        Returns:
            The new length of the waypoint queue
        """
        self._waypoints.pop(i)
        return len(self._waypoints)

    def view_waypoints(self):
        """
        Returns a copy of the current waypoint queue in order.
        To edit the waypoint queue, use the add_waypoint and del_waypoint methods
        """
        return [waypoint for waypoint in self._waypoints]

    def get_waypoint(self, i=0):
        """
        Returns the i-th waypoint, or the next waypoint if i is not specified
        """
        if self._waypoints:
            return self._waypoints[i]
        return None