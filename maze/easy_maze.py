from maze import obstacles


def generate_maze() -> None:
    maze = []
    with open('easy_maze.txt', 'r') as file:
        for line in file.readlines():
            x, y = map(int, line.strip().split(','))
            maze.append((x, y))
    obstacles.obstacles.append(tuple(maze))
