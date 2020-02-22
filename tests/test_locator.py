import unittest
from importlib import reload
from pi.boat_driver import TestDriver, SimDriver
from pi.helmsman import RudderController
from sim.sim_interface import SimulatorInterface
import json
import locator

config_paths = [
    'tests/configs/test_locator0.json',
    'tests/configs/test_locator1.json',
    'tests/configs/test_locator2.json'
]

class TestLocator(unittest.TestCase):
    def setUp(self):
        global locator
        # locator is reset between every test so that a new config can be loaded
        locator = reload(locator)

    def test_load_configs_testing(self):
        """
        Tests that configs are properly loaded for a testing configuration
        """
        global locator, config_paths
        locator.load_config(config_paths[0])

        self.assertEqual(locator.config['routines'], ['debug'])
        self.assertEqual(locator.config['driver'],
        {
            'type': 'TestDriver',
            'kwargs': {
                'verbose': False
            }
        })

    def test_load_configs_simulation(self):
        """
        Tests that configs are properly loaded for a simulation configuration
        """
        global locator, config_paths
        locator.load_config(config_paths[1])

        self.assertEqual(locator.config['routines'], ['simulate'])
        self.assertEqual(locator.config['driver'],
        {
            'type': 'SimDriver',
            'kwargs': {
                "arg": "val"
            }
        })
    
    def test_get_driver_test_class(self):
        """
        Tests that get_driver returns a testing_driver when configured to use such a driver.
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        self.assertIsInstance(locator.get_driver(), TestDriver,
        'get_driver did not return a test_driver when it was expected to.')
        self.assertNotIsInstance(locator.get_driver(), SimDriver,
        'get_driver returned a sim_driver when it was expect to return a test_driver')

    def test_get_driver_sim_class(self):
        """
        Tests that get_driver returns a sim_driver when configured to use such a driver
        """
        global locator, config_paths
        locator.load_config(config_paths[1])
        self.assertNotIsInstance(locator.get_driver(), TestDriver,
        'get_driver returned a test_driver when it was expect to return a sim_driver')
        self.assertIsInstance(locator.get_driver(), SimDriver,
        'get_driver did not return a sim_driver when it was expected to.')

    def test_get_driver_returns_singleton(self):
        """
        Tests that get_driver returns only a single instance of the driver, regardless of how many times it's called
        """
        global locator, config_paths
        locator.load_config(config_paths[1])       
        driver1 = locator.get_driver()
        driver2 = locator.get_driver()
        
        self.assertIsNotNone(driver1, 'get_driver returned None on first invokation')
        self.assertIsNotNone(driver2, 'get_driver returned None on second invokation')
        self.assertEqual(driver1, driver2, 
        'first and second invokations of get_driver returned different drivers')


    def test_get_driver_test_class_usable(self):
        """
        Tests that the driver returned by get_driver is usabled when configured to use a test_driver
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        
        driver = locator.get_driver()
        try:
            driver.get_wind_dir()
            driver.get_sail()
        except Exception:
            self.fail('Could not call get_wind_dir and get_sail on driver from get_driver')

    def test_get_helmsman_driver_not_instantiated(self):
        """
        Tests that get_helsman will return properly even when get_driver hasn't been called
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        helmsman = locator.get_helmsman()
       
        self.assertIsNotNone(helmsman, 'get_helmsman returns None when get_driver not called')
    
    def test_get_helsman_returns_singleton(self):
        """
        Tests that get_helsman returns only a single instance of the helmsman, regardless of how many times it is called.
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        helmsman1 = locator.get_helmsman()
        helmsman2 = locator.get_helmsman()
       
        self.assertEqual(helmsman1, helmsman2,
        'Two subsequent calls of get_helmsman return different instances.')

    def test_get_helsman_correct_attributes(self):
        """
        Tests that get_helsman returns a helmsman whose rudder/sail controllers are enabled/disabled according to the configuration file.
        """
        global locator, config_paths
        locator.load_config(config_paths[1])

        helmsman = locator.get_helmsman()
        self.assertEqual(helmsman.rudder_controller_enabled, False,
        'helmsman has enabled rudder controller when it should be disabled')
        self.assertEqual(helmsman.sail_controller_enabled, True,
        'helsman has disabled sail_controller when it should be enabled')

    def test_get_server_runnable(self):
        """
        Tests that get_server_runnable returns a method that can be called to start the flask_server
        """
        global locator, config_paths
        locator.load_config(config_paths[2])

        self.assertIsNotNone(locator.get_server_runnable())

    def test_get_sim_interface(self):
        """
        Tests that get_sim_interface returns an instance of SimulatorInterface
        """
        global locator, config_paths
        locator.load_config(config_paths[1])

        self.assertIsInstance(locator.get_sim_interface(), SimulatorInterface,
        'get_sim_interface did not return a SimulatorInterface')

    def test_get_sim_interface_returns_singleton(self):
        """
        Tests that get_sim_interface returns only a single instance of the sim_interface, regardless of how many times it is called.
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        sim_interface1 = locator.get_sim_interface()
        sim_interface2 = locator.get_sim_interface()
       
        self.assertEqual(sim_interface1, sim_interface2,
        'Two subsequent calls of get_sim_interface returned different instances.')

    def test_get_sail_controller_returns_singleton(self):
        """
        Tests that get_sim_sail_controller returns only a single instance of the sail_controller, regardless of how many times it is called.
        """
        global locator, config_paths
        locator.load_config(config_paths[0])
        sc1 = locator.get_sail_controller()
        sc2 = locator.get_sail_controller()
       
        self.assertEqual(sc1, sc2,
        'Two subsequent calls of get_sail_controller returned different instances.')

    def test_get_rudder_controller(self):
        global locator, config_paths
        locator.load_config(config_paths[0])
        rc = locator.get_rudder_controller()
        self.assertIsInstance(rc, RudderController)

if __name__ == '__main__':
    unittest.main()