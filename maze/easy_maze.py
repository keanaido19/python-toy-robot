import os
from maze import obstacles


def generate_maze() -> None:
    maze = []
    path = os.path.join(os.path.dirname(__file__))
    with open(f'{path}/easy_maze.txt', 'r') as file:
        for line in file.readlines():
            x, y = map(int, line.strip().split(','))
            maze.append((x, y))
    obstacles.obstacles.append(tuple(maze))