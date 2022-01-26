import random

obstacles: list[tuple[tuple[int, int]]] = []


def create_square_obstacle(
        llx: int,
        lly: int,
        urx: int,
        ury: int,
        size: int = 5,
        amount: int = 10
) -> None:
    """
    Creates a square obstacle by storing coordinate points for the perimeter
    :param int llx: Lower left x coordinate
    :param int lly: Upper x coordinate
    :param int urx: Lower left y coordinate
    :param int ury: Upper y coordinate
    :param int size: Size of the obstacle
    :param int amount: Amount of square obstacles that can be created
    :return: None
    """
    global obstacles
    obstacles = []
    for _ in range(random.randint(0, amount)):
        random_x, random_y = get_random_coordinates(llx, lly, urx, ury, size)
        if random_x == random_y == 0:
            continue
        square_obstacle = [(random_x, random_y)]
        for i in range(1, size):
            square_obstacle.append((random_x, random_y + i))
        for i in range(1, size):
            square_obstacle.append((random_x + i, random_y))
        for i in range(1, size - 1):
            square_obstacle.append((random_x + i, random_y + size - 1))
        for i in range(1, size):
            square_obstacle.append((random_x + size - 1, random_y + i))
        obstacles.append(tuple(square_obstacle))


def get_random_coordinates(
        llx: int,
        lly: int,
        urx: int,
        ury: int,
        size: int = 5
) -> tuple[int, int]:
    """
    Returns a set of cartesian coordinates
    :param int llx: Lower left x coordinate
    :param int lly: Upper x coordinate
    :param int urx: Lower left y coordinate
    :param int ury: Upper y coordinate
    :param int size: Size of the obstacle
    :return: x coordinate and y coordinate
    """
    counter = 0
    while True:
        if counter == 10:
            return 0, 0
        random_x = get_random_x_coordinate(llx, urx, size)
        random_y = get_random_y_coordinate(lly, ury, size)
        if not is_invalid_coordinates(random_x, random_y, size):
            return random_x, random_y
        counter += 1


def is_invalid_coordinates(x_coordinate: int, y_coordinate: int, size: int) \
        -> bool:
    """
    Checks is given coordinates are invalid
    :param int x_coordinate: x coordinate
    :param int y_coordinate: y coordinate
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    global obstacles
    boolean_values = []
    if check_coordinates_overlap_origin(x_coordinate, y_coordinate, size):
        return True
    if obstacles:
        for obstacle in obstacles:
            boolean_values.append(
                check_x_coordinate_overlap(x_coordinate, obstacle, size) and
                check_y_coordinate_overlap(y_coordinate, obstacle, size))
    return any(boolean_values)


def check_x_coordinate_overlap(x_coordinate: int,
                               obstacle: tuple[tuple[int, int]], size: int) \
        -> bool:
    """
    Checks if the x coordinate overlaps with an existing obstacle
    :param int x_coordinate: x coordinate
    :param tuple[tuple[int, int]] obstacle: An obstacle
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    return obstacle[0][0] - (size - 1) <= x_coordinate <= obstacle[0][0] + (
        size - 1)


def check_y_coordinate_overlap(y_coordinate: int,
                               obstacle: tuple[tuple[int, int]], size: int) \
        -> bool:
    """
    Checks if the y coordinate overlaps with an existing obstacle
    :param int y_coordinate: y coordinate
    :param tuple[tuple[int, int]] obstacle: An obstacle
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    return obstacle[0][1] - size <= y_coordinate <= obstacle[0][1] + (
        size - 1)


def check_coordinates_overlap_origin(x_coordinate: int, y_coordinate: int,
                                     size: int) -> bool:
    """
    Checks if the x and y coordinate of the obstacle will overlap with the
    origin point
    :param int x_coordinate: x coordinate
    :param int y_coordinate: y coordinate
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    return check_x_coordinate_overlap_origin(x_coordinate, size) and \
        check_y_coordinate_overlap_origin(y_coordinate, size)


def check_x_coordinate_overlap_origin(x_coordinate: int, size: int) -> bool:
    """
    Checks if the x coordinate of the obstacle will overlap with the origin
    point
    :param int x_coordinate: x coordinate
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    return x_coordinate in range(-(size - 1), 1)


def check_y_coordinate_overlap_origin(y_coordinate: int, size: int) -> bool:
    """
    Checks if the y coordinate of the obstacle will overlap with the origin
    point
    :param int y_coordinate: y coordinate
    :param int size: Size of the obstacle
    :return: Boolean value
    """
    return y_coordinate in range(-(size - 1), 1)


def get_random_x_coordinate(llx: int, urx: int, size: int) -> int:
    """
    Returns a random x coordinate based on the area limit and the size of the
    obstacle
    :param int llx: Lower left x coordinate
    :param int urx: Upper right x coordinate
    :param int size: Size of the obstacle
    :return: Random x coordinate
    """
    return random.randint(llx, urx - size - 1)


def get_random_y_coordinate(lly: int, ury: int, size: int) -> int:
    """
    Returns a random x coordinate based on the area limit and the size of the
    obstacle
    :param int lly: Lower left y coordinate
    :param int ury: Upper right y coordinate
    :param int size: Size of the obstacle
    :return: Random x coordinate
    """
    return random.randint(lly, ury - size - 1)


def is_position_blocked(x: int, y: int) -> bool:
    """
    Returns True if position (x,y) falls on an obstacle
    :param int x: x Coordinate
    :param int y: y Coordinate
    :return: Boolean value
    """
    boolean_values = [(x, y) in obstacle for obstacle in obstacles]
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
