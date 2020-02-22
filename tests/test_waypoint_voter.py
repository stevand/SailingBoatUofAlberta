import unittest
import locator
from pi.navigator.poll_navigator.voter import WaypointVoter
from pi.boat_driver import AbstractBoatDriver


locator.load_config('tests/configs/test_voter.json')
driver = locator.get_driver()

class TestWaypointVoter(unittest.TestCase):
    def setUp(self):
        global driver
        #driver will be of type test_driver
        driver.reset()
        self._waypoint = (0, 0)
        get_waypoint = lambda: self._waypoint
        self.voter = WaypointVoter(driver, get_waypoint)

    def test_rejects_waypoints_beyond_90_degrees(self):
        global driver
        driver.position = (0, 0)
        self._waypoint = (1, 1)
        self.assertEqual(self.voter.vote(180), 0, 
        "Did not vote 0 when boat was at (0,0), waypoint was at (1,1) and heading was 180")

        driver.position = (1, 1)
        self._waypoint = (-1, -1)
        self.assertEqual(self.voter.vote(45), 0, 
        "Did not vote 0 when boat was at (1,1), waypoint was at (-1,-1) and heading was 30")


    def test_postive_when_waypoint_within_90_degrees(self):
        driver.position = (0, 0)
        self._waypoint = (0, 1)
        self.assertGreater(self.voter.vote(45), 0, 
        "Voted 0 when boat was at (0,0), waypoint was at (0,1) and heading was 45")

        self.assertGreater(self.voter.vote(135), 0, 
        "Did not vote 0 when boat was at (0,0), waypoint was at (0,1) and heading was 135")

    def test_votes_higher_when_heading_closer_to_straight_line(self):
        driver.position = (0, 0)
        self._waypoint = (0, -1)
        self.assertGreater(self.voter.vote(271), self.voter.vote(300), 
        "Did not vote higher for 271 vs 300 when waypoint was at 270 degrees")

        self._waypoint = (-1, 0)
        self.assertGreater(self.voter.vote(190), self.voter.vote(210), 
        "Did not vote higher for 190 vs 210 when waypoint was at 180 degrees")
    