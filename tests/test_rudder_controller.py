import unittest
import locator
import pi.helmsman.rudder_controller as rc
from importlib import reload
from time import sleep

config_path = 'tests/configs/test_controllers.json'


def is_enabled():
    return True


class TestRudderController(unittest.TestCase):
    def setUp(self):
        global locator
        locator = reload(locator)
        locator.load_config(config_path)
        self.driver = locator.get_driver()

    def test_shortest_path_100_20(self):
        self.assertEqual(rc.shortest_path(100, 20), 80,
                         'Shortest path to 100 degrees from 20 was not +80')

    def test_shortest_path_10_100(self):
        self.assertEqual(rc.shortest_path(10, 100), -90,
                         'Shortest path to 10 from 100 degrees was not -90')

    def test_shortest_path_350_10(self):
        self.assertEqual(rc.shortest_path(350, 10), -20,
                         'Shortest path to 350 from 10 degrees was not -20')

    def test_shortest_path_10_350(self):
        self.assertEqual(rc.shortest_path(10, 350), 20,
                         'Shortest path to 10 from 350 degrees was not +20')

    def test_shortest_path_10_200(self):
        self.assertEqual(rc.shortest_path(10, 200), 170,
                         'Shortest path to 10 from 200 degrees was not 170')

    def test_shortest_path_200_10(self):
        self.assertEqual(rc.shortest_path(200, 10), -170,
                         'Shortest path to 200 from 10 degrees was not -170')

    def test_tries_to_turn_right_100_20(self):
        def get_desired_heading():
            return 100

        self.driver.heading = 20
        rc.start(self.driver, get_desired_heading, is_enabled, interval=.001)
        sleep(0.003)
        self.assertGreater(self.driver.get_rudder(), 0,
                           'Boat did not try to turn right when the desired heading was 100 but the current heading was 20')

    def test_tries_to_turn_left_350_10(self):
        def get_desired_heading():
            return 350

        self.driver.heading = 10
        rc.start(self.driver, get_desired_heading, is_enabled, interval=.001)
        sleep(0.003)
        self.assertLess(self.driver.get_rudder(), 0,
                        'Boat did not try to turn left when the desired heading was 350 but the current heading was 10')
