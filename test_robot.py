"""
UnitTest for robot.py
"""
import robot
import unittest
from unittest.mock import patch
from io import StringIO
from test_base import captured_output
from maze import obstacles


class MyTestCase(unittest.TestCase):
    @patch('sys.stdin', StringIO('help\nofF\nfOrWarD 10'))
    def test_get_command(self):
        with captured_output():
            self.assertEqual('help', robot.get_command('TestBot'))
            self.assertEqual('off', robot.get_command('TestBot'))
            self.assertEqual('forward 10', robot.get_command('TestBot'))

    def test_valid_command(self):
        self.assertTrue(robot.valid_command('forward 10'))
        self.assertTrue(robot.valid_command('help'))
        self.assertTrue(robot.valid_command('replay'))
        self.assertFalse(robot.valid_command('forward a'))
        self.assertFalse(robot.valid_command('offf'))
        self.assertFalse(robot.valid_command('jump up'))

    @patch('sys.stdin', StringIO('TestBot\nforward 99\noff\n'))
    def test_forward(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 1
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: Loaded obstacles.
There are some obstacles:
- At position 1,1 (to 5,5)
TestBot: What must I do next?  > TestBot moved forward by 99 steps.
 > TestBot now at position (0,99).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nback 99\noff\n'))
    def test_back(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 1
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: Loaded obstacles.
There are some obstacles:
- At position 1,1 (to 5,5)
TestBot: What must I do next?  > TestBot moved back by 99 steps.
 > TestBot now at position (0,-99).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nright\noff\n'))
    def test_right(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 1
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: Loaded obstacles.
There are some obstacles:
- At position 1,1 (to 5,5)
TestBot: What must I do next?  > TestBot turned right.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nleft\noff\n'))
    def test_left(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot turned left.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nforward 201\noff\n'))
    def test_area1(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next? TestBot: Sorry, I cannot go outside my safe zone.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nback 300\noff\n'))
    def test_area2(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next? TestBot: Sorry, I cannot go outside my safe zone.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nleft\nforward 120\noff\n'))
    def test_area3(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot turned left.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Sorry, I cannot go outside my safe zone.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nright\nback 101\noff\n'))
    def test_area4(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot turned right.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Sorry, I cannot go outside my safe zone.
 > TestBot now at position (0,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nright\nback '
                                 '10\nleft\nforward 10\nreplay\noff\n'))
    def test_replay(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot turned right.
 > TestBot now at position (0,0).
TestBot: What must I do next?  > TestBot moved back by 10 steps.
 > TestBot now at position (-10,0).
TestBot: What must I do next?  > TestBot turned left.
 > TestBot now at position (-10,0).
TestBot: What must I do next?  > TestBot moved forward by 10 steps.
 > TestBot now at position (-10,10).
TestBot: What must I do next?  > TestBot turned right.
 > TestBot now at position (-10,10).
 > TestBot moved back by 10 steps.
 > TestBot now at position (-20,10).
 > TestBot turned left.
 > TestBot now at position (-20,10).
 > TestBot moved forward by 10 steps.
 > TestBot now at position (-20,20).
 > TestBot replayed 4 commands.
 > TestBot now at position (-20,20).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nright\nback 10\nleft\nforward '
                                 '10\nreplay 3-1\noff\n'))
    def test_replay_range(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot turned right.
 > TestBot now at position (0,0).
TestBot: What must I do next?  > TestBot moved back by 10 steps.
 > TestBot now at position (-10,0).
TestBot: What must I do next?  > TestBot turned left.
 > TestBot now at position (-10,0).
TestBot: What must I do next?  > TestBot moved forward by 10 steps.
 > TestBot now at position (-10,10).
TestBot: What must I do next?  > TestBot moved back by 10 steps.
 > TestBot now at position (-10,0).
 > TestBot turned left.
 > TestBot now at position (-10,0).
 > TestBot replayed 2 commands.
 > TestBot now at position (-10,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nmazerun\noff\n'))
    def test_maze_run(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot starting maze run..
 > TestBot moved forward by 199 steps.
 > TestBot now at position (0,199).
TestBot: I am at the top edge.
 > TestBot now at position (0,199).
TestBot: What must I do next? TestBot: Shutting down..""", output)

    @patch('sys.stdin', StringIO('TestBot\nmazerun right\noff\n'))
    def test_maze_run_right(self):
        with captured_output() as (out, err):
            obstacles.random.randint = lambda a, b: 0
            robot.robot_start()
        output = out.getvalue().strip()
        self.assertEqual("""What do you want to name your robot? \
TestBot: Hello kiddo!
TestBot: What must I do next?  > TestBot starting maze run..
 > TestBot turned right.
 > TestBot now at position (0,0).
 > TestBot moved forward by 99 steps.
 > TestBot now at position (99,0).
TestBot: I am at the right edge.
 > TestBot now at position (99,0).
TestBot: What must I do next? TestBot: Shutting down..""", output)


if __name__ == '__main__':
    unittest.main()
