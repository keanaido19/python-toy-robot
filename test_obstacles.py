"""
UnitTest for Obstacles.
"""
import unittest

from maze import obstacles


class MyTestCase(unittest.TestCase):
    def test_create_obstacles(self):
        obstacles.random.randint = lambda a, b: 1
        obstacles.create_square_obstacle(-100, -200, 100, 200)
        self.assertEqual([((1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                           (2, 1), (3, 1), (4, 1), (5, 1),
                           (2, 5), (3, 5), (4, 5),
                           (5, 2), (5, 3), (5, 4), (5, 5))],
                         obstacles.obstacles)
        obstacles.random.randint = lambda a, b: 0
        obstacles.create_square_obstacle(-100, -200, 100, 200)
        self.assertEqual([], obstacles.obstacles)

    def test_is_position_blocked(self):
        obstacles.random.randint = lambda a, b: 1
        obstacles.create_square_obstacle(-100, -200, 100, 200)
        self.assertTrue(obstacles.is_position_blocked(5, 1))
        self.assertFalse(obstacles.is_position_blocked(2, 4))
        self.assertFalse(obstacles.is_position_blocked(10, 20))

    def test_is_path_blocked(self):
        obstacles.random.randint = lambda a, b: 1
        obstacles.create_square_obstacle(-100, -200, 100, 200)
        self.assertTrue(obstacles.is_path_blocked(4, -100, 4, 100))
        self.assertTrue(obstacles.is_path_blocked(185, 3, -14, 3))
        self.assertTrue(obstacles.is_path_blocked(5, -100, 5, 100))
        self.assertTrue(obstacles.is_path_blocked(185, 1, -14, 1))
        self.assertTrue(obstacles.is_path_blocked(99, 1, 5, 1))
        self.assertFalse(obstacles.is_path_blocked(0, -100, 0, 100))
        self.assertFalse(obstacles.is_path_blocked(185, 7, -14, 7))


if __name__ == '__main__':
    unittest.main()