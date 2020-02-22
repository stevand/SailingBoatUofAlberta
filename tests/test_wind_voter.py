import unittest
import locator
from pi.navigator.poll_navigator.voter import WindVoter
from pi.boat_driver import AbstractBoatDriver


locator.load_config('tests/configs/test_voter.json')
driver = locator.get_driver()
wind_voter = WindVoter(driver)


class TestWindVoter(unittest.TestCase):
    def setUp(self):
        global driver
        #driver will be of type test_driver
        driver.reset()

    def test_heading_100_wind_200(self):
        global driver, wind_voter
        driver.wind_dir = 200

        self.assertGreater(wind_voter.vote(100), 0, 
        "Voted 0 when candidate heading was 100 and wind_dir was 200")
    
    def test_heading_60_wind_300(self):
        global driver, wind_voter
        driver.wind_dir = 300

        self.assertGreater(wind_voter.vote(60), 0, 
        "Voted 0 when candidate heading was 60 and wind_dir was 300")

    def test_heading_30_wind_0(self):
        global driver, wind_voter
        driver.wind_dir = 0

        self.assertEqual(wind_voter.vote(30), 0, 
        "Did not vote 0 when candidate heading was 30 and wind_dir was 0")

    def test_heading_330_wind_0(self):
        global driver, wind_voter
        driver.wind_dir = 0

        self.assertEqual(wind_voter.vote(330), 0, 
        "Did not vote 0 when candidate heading was 330 and wind_dir was 0")

    def test_heading_110_wind_90(self):
        global driver, wind_voter
        driver.wind_dir = 90

        self.assertEqual(wind_voter.vote(110), 0, 
        "Did not vote 0 when candidate heading was 110 and wind_dir was 90")