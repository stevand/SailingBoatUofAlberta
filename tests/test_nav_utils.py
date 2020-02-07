import unittest
from pi import navutils


class TestNavUtils(unittest.TestCase):
    def test_dir_to_waypoint(self):
        self.assertEqual(navutils.dir_to_waypoint(0, 0, 1, 1), 45,
                         "Direction from (0, 0) to (1, 1) should be 45 degrees")

        self.assertAlmostEqual(navutils.dir_to_waypoint(-1, 1, 3, 4), 36.8699, places=3,
                               msg="Direction from (-1, 1) to (3, 4) should be about 21.8014 degrees")

        self.assertEqual(navutils.dir_to_waypoint(0, 0, -1, -1), 225,
                         "Direction from (0, 0) to (-1, -1) should be 225 degrees")

        self.assertAlmostEqual(navutils.dir_to_waypoint(2, -1, 0, 0), 153.4349, places=3,
                               msg="Direction from (2, -1) to (0, 0) should be about 154.4349 degrees")

    def test_smallest_angle_between(self):
        self.assertEqual(navutils.smallest_angle_between(330, 30), 60,
                         "Smallest angle between 330 and 30 should be 60")

        self.assertEqual(navutils.smallest_angle_between(70, 200), 130,
                         "Smallest angle between 70 and 200 should be 130")

    def test_shortest_path_100_20(self):
        self.assertEqual(navutils.shortest_path(100, 20), 80,
                         'Shortest path to 100 degrees from 20 was not +80')

        self.assertEqual(navutils.shortest_path(10, 100), -90,
                         'Shortest path to 10 from 100 degrees was not -90')

        self.assertEqual(navutils.shortest_path(350, 10), -20,
                         'Shortest path to 350 from 10 degrees was not -20')

        self.assertEqual(navutils.shortest_path(10, 350), 20,
                         'Shortest path to 10 from 350 degrees was not +20')

        self.assertEqual(navutils.shortest_path(10, 200), 170,
                         'Shortest path to 10 from 200 degrees was not 170')

        self.assertEqual(navutils.shortest_path(200, 10), -170,
                         'Shortest path to 200 from 10 degrees was not -170')
