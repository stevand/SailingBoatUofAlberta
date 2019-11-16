from voter import Voter

# TODO IMPLEMENT
class WaypointVoter(Voter):

    def vote(self, heading):
        pass

    def bearing_to_waypoint(self):
        x1, y1 = self._driver.get_position()
        x2, y2 = self._directive.next_waypoint()
