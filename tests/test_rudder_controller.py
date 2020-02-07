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

    def test_tries_to_turn_left_100_20(self):
        def get_desired_heading():
            return 100

        self.driver.heading = 20
        rc.start(self.driver, get_desired_heading, is_enabled, interval=.001)
        sleep(0.003)
        self.assertLess(self.driver.get_rudder(), 0,
                           'Boat did not try to turn left when the desired heading was 100 but the current heading was 20')

    def test_tries_to_turn_right_350_10(self):
        def get_desired_heading():
            return 350

        self.driver.heading = 10
        rc.start(self.driver, get_desired_heading, is_enabled, interval=.001)
        sleep(0.003)
        self.assertGreater(self.driver.get_rudder(), 0,
                        'Boat did not try to turn right when the desired heading was 350 but the current heading was 10')
