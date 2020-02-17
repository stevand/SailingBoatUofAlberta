import unittest
import locator
from pi.navigator.poll_navigator.voter import ChannelVoter
from pi.boat_driver.abstract_boat_driver import AbstractBoatDriver


locator.load_config('tests/configs/test_voter.json')
driver = locator.get_driver()

class TestWaypointVoter(unittest.TestCase):
    def setUp(self):
        global driver
        #driver will be of type test_driver
        driver.reset()
        self._path = ((0, 0), (1, 0))
        get_path = lambda: self._path
        self.voter = ChannelVoter(driver, get_path, channel_width=1)

    def test_has_no_preference_within_channel(self):
        self._path = ((0, 0), (1, 0))
        driver.position = (0.5, 0.5)

        for heading in range(0, 360, 10):
            self.assertEqual(self.voter.vote(heading), 1,
            'Did not give max vote for heading of {} when in channel'.format(heading))

    def test_has_preference_outside_channel(self):
        self._path = ((0, 0), (1, 0))
        driver.position = (0, 1.1) #just outside channel_width of 1

        for heading in [330, 0, 45, 90, 140, 180, 200]:
            self.assertEqual(self.voter.vote(heading), 0,
            'Voted for heading of {} when directly above and outside channel'.format(heading))

        for heading in [270, 300, 240]:
            self.assertEqual(self.voter.vote(heading), 1,
            'Did not give max vote for heading of {} when directly above and outside channel'.format(heading))

    
