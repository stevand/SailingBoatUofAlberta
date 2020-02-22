import unittest
import locator
from pi.helmsman import SailController
from importlib import reload
from time import sleep

config_path = 'tests/configs/test_controllers.json'

class TestRudderController(unittest.TestCase):
    def setUp(self):
        global locator
        locator = reload(locator)
        locator.load_config(config_path)
        self.driver = locator.get_driver()

    def test_create_instance(self):
        sail_config = locator.get_config()['helmsman']['sail_controller']
        sc = SailController.create(sail_config)
        self.assertIsInstance(sc, SailController)

if __name__ == '__main__':
    unittest.main()