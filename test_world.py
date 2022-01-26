"""
UnitTest for Text World.
"""
import unittest

from test_base import captured_output
from world.text import world


class MyTestCase(unittest.TestCase):
    def test_show_position(self):
        world.position_x = 10
        world.position_y = 50
        with captured_output() as (out, err):
            world.show_position('TestBot')
            output = out.getvalue().strip()
        self.assertEqual('> TestBot now at position (10,50).', output)

    def test_is_position_allowed(self):
        return_value = world.is_position_allowed(89, -199)
        self.assertTrue(return_value)
        return_value = world.is_position_allowed(-101, 5)
        self.assertFalse(return_value)

    def test_update_position(self):
        world.position_x = 20
        world.position_y = 4
        world.current_direction_index = 0
        return_value = world.update_position(40)
        self.assertTrue(return_value)
        self.assertEqual((20, 44), (world.position_x, world.position_y))

        world.current_direction_index = 1
        return_value = world.update_position(90)
        self.assertFalse(return_value)
        self.assertEqual((20, 44), (world.position_x, world.position_y))

        world.current_direction_index = 2
        return_value = world.update_position(70)
        self.assertTrue(return_value)
        self.assertEqual((20, -26), (world.position_x, world.position_y))

        world.current_direction_index = 3
        return_value = world.update_position(-250)
        self.assertFalse(return_value)
        self.assertEqual((20, -26), (world.position_x, world.position_y))


if __name__ == '__main__':
    unittest.main()
