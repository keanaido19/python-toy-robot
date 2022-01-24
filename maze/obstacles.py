import random

obstacles: list[tuple[tuple[int, int]]] = []


def create_square_obstacle() -> None:
    """
    Creates a square obstacle by storing coordinate points for the perimeter
    :return: None
    """
    global obstacles
    obstacles = []
    size = 4
    for _ in range(random.randint(0, 10)):
        random_x = random.randint(-100, 96)
        while random_x in range(-5, 1):
            random_x = random.randint(-100, 96)
        random_y = random.randint(-200, 196)
        while random_y in range(-5, 1):
            random_y = random.randint(-200, 196)
        square_obstacle = [(random_x, random_y)]
        for i in range(1, size + 1):
            square_obstacle.append((random_x, random_y + i))
        for i in range(1, size + 1):
            square_obstacle.append((random_x + i, random_y))
        for i in range(1, size):
            square_obstacle.append((random_x + i, random_y + size))
        for i in range(1, size + 1):
            square_obstacle.append((random_x + size, random_y + i))
        obstacles.append(tuple(square_obstacle))


def is_position_blocked(x: int, y: int) -> bool:
    """
    Returns True if position (x,y) falls inside an obstacle.
    :param int x: x Coordinate
    :param int y: y Coordinate
    :return: Boolean value
    """
    boolean_values = []
    for obstacle in obstacles:
        min_coordinate = obstacle[0]
        max_coordinate = obstacle[-1]
        in_x = x in range(min_coordinate[0], max_coordinate[0] + 1)
        in_y = y in range(min_coordinate[1], max_coordinate[1] + 1)
        boolean_values.append(in_x and in_y)
    return any(boolean_values)


def is_path_blocked(x1: int, y1: int, x2: int, y2: int) -> bool:
    """
    Returns True if there is an obstacle in the line between the coordinates
    (x1, y1) and (x2, y2)
    :param int x1: x Coordinate of position 1
    :param int y1: y Coordinate of position 1
    :param int x2: x Coordinate of position 2
    :param int y2: y Coordinate of position 2
    :return: Boolean value
    """
    for obstacle in obstacles:
        for position in obstacle:
            if x1 == x2:
                step = 1 if y1 <= y2 else -1
                if position[0] == x1 and position[1] in range(y1, y2 + step,
                                                              step):
                    return True
            if y1 == y2:
                step = 1 if x1 <= x2 else -1
                if position[1] == y1 and position[0] in range(x1, x2 + step,
                                                              step):
                    return True
    return False
