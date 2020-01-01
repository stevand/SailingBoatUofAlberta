import unittest
import locator
import pi.control.rudder_controller as rc

config_path = 'test_controllers.json'


class TestRudderController(unittest.TestCase):
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
