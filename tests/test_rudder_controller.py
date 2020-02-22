import unittest
import locator
import pi.helmsman.rudder_controller as rc
from pi.helmsman import RudderController
from importlib import reload
from time import sleep

config_path = 'tests/configs/test_controllers.json'


class TestRudderController(unittest.TestCase):
    def setUp(self):
        global locator
        locator = reload(locator)
        locator.load_config(config_path)
        self.driver = locator.get_driver()

    def test_tries_to_turn_left_100_20(self):
        self.driver.heading = 20
        self.rudder_controller = RudderController(self.driver, desired_heading=100, interval=0.001, enabled=True)
        sleep(0.003)
        self.assertLess(self.driver.get_rudder(), 0,
                        'Boat did not try to turn left when the desired heading was 100 but the current heading was 20')

    def test_tries_to_turn_right_350_10(self):
        self.driver.heading = 10
        self.rudder_controller = RudderController(self.driver, desired_heading=350, interval=0.001, enabled=True)
        sleep(0.003)
        self.assertGreater(self.driver.get_rudder(), 0,
                           'Boat did not try to turn right when the desired heading was 350 but the current heading was 10')
