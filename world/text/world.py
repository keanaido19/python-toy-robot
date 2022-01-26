from maze import obstacles

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positions given the current direction,
    and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def check_object(steps):
    """
    Checks the new x and y positions are obstructed given the current
    direction, and specific nr of steps
    :param steps:
    :return: True if the position is not obstructed, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    return any([obstacles.is_path_blocked(position_x, position_y, new_x, new_y),
                obstacles.is_position_blocked(new_x, new_y)])


def generate_obstacles() -> None:
    """
    Generates random square obstacles
    :return: None
    """
    obstacles.create_square_obstacle(min_x, min_y, max_x, max_y)


def get_obstacle_coordinates() -> list[tuple[int, int]]:
    """
    Unpacks every obstacle coordinate into a list
    :return: A list of all obstacle coordinates
    """
    obstacle_coordinates: list[tuple[int, int]] = []
    for obstacle in obstacles.obstacles:
        for position in obstacle:
            obstacle_coordinates.append(position)
    return obstacle_coordinates


def print_square_obstacles() -> None:
    """
    Prints out the position of the square obstacles
    :return: None
    """
    print('There are some obstacles:')
    for obstacle in obstacles.obstacles:
        min_position = obstacle[0]
        max_position = obstacle[-1]
        print(f'- At position {min_position[0]},{min_position[1]}'
              f' (to {max_position[0]},{max_position[1]})')


def print_simple_maze_obstacles() -> None:
    """
    Prints out the position of the square obstacles in the simple maze
    :return: None
    """
    print('There are some obstacles:')
    obstacle_coordinates: list[tuple[int, int]] = get_obstacle_coordinates()
    for i in range(0, len(obstacle_coordinates), 16):
        min_position = obstacle_coordinates[i]
        max_position = obstacle_coordinates[i + 15]
        print(f'- At position {min_position[0]},{min_position[1]}'
              f' (to {max_position[0]},{max_position[1]})')


def print_maze_obstacles() -> None:
    """
    Prints out the position of the obstacles in the maze
    :return: None
    """
    print('There are some obstacles:')
    obstacle_coordinates: list[tuple[int, int]] = get_obstacle_coordinates()
    for obstacle_position in obstacle_coordinates:
        print(f'- At position ({obstacle_position[0]},{obstacle_position[1]})')


def setup_text_world(robot_name: str) -> None:
    """
    Creates the standard text world for the robot
    :param str robot_name: Name of the robot
    :return: None
    """
    generate_obstacles()
    if obstacles.obstacles:
        print(f'{robot_name}: Loaded obstacles.')
        print_square_obstacles()


def setup_text_simple_maze(robot_name: str) -> None:
    """
    Creates the simple maze text world for the robot
    :param str robot_name: Name of the robot
    :return: None
    """
    import maze.simple_maze as imported_maze
    print(f'{robot_name}: Loaded simple_maze.')
    imported_maze.generate_maze()
    print_simple_maze_obstacles()


def setup_text_easy_maze(robot_name: str) -> None:
    """
    Creates the easy maze text world for the robot
    :param str robot_name: Name of the robot
    :return: None
    """
    import maze.easy_maze as imported_maze
    print(f'{robot_name}: Loaded easy_maze.')
    imported_maze.generate_maze()
    print_maze_obstacles()


def setup_text_medium_maze(robot_name: str) -> None:
    """
    Creates the medium maze text world for the robot
    :param str robot_name: Name of the robot
    :return: None
    """
    import maze.medium_maze as imported_maze
    print(f'{robot_name}: Loaded medium_maze.')
    imported_maze.generate_maze()
    print_maze_obstacles()


def setup_text_extreme_maze(robot_name: str) -> None:
    """
    Creates the extreme maze text world for the robot
    :param str robot_name: Name of the robot
    :return: None
    """
    import maze.extreme_maze as imported_maze
    print(f'{robot_name}: Loaded extreme_maze.')
    imported_maze.generate_maze()
    print_maze_obstacles()


def setup_world(commandline_argument: list[str], robot_name: str) -> None:
    """
    Imports the correct modules for the robot world
    :param list[str] commandline_argument: Commandline arguments
    :param str robot_name: Name of the robot
    :return: None
    """
    if len(commandline_argument) == 2:
        if commandline_argument[0] == 'TEXT':
            if commandline_argument[1] == 'SIMPLE_MAZE':
                setup_text_simple_maze(robot_name)
            elif commandline_argument[1] == 'EASY_MAZE':
                setup_text_easy_maze(robot_name)
            elif commandline_argument[1] == 'MEDIUM_MAZE':
                setup_text_medium_maze(robot_name)
            elif commandline_argument[1] == 'EXTREME_MAZE':
                setup_text_extreme_maze(robot_name)
    elif len(commandline_argument) == 1:
        if commandline_argument[0] == 'SIMPLE_MAZE':
            setup_text_simple_maze(robot_name)
        elif commandline_argument[0] == 'EASY_MAZE':
            setup_text_easy_maze(robot_name)
        elif commandline_argument[0] == 'MEDIUM_MAZE':
            setup_text_medium_maze(robot_name)
        elif commandline_argument[0] == 'EXTREME_MAZE':
            setup_text_extreme_maze(robot_name)
        elif commandline_argument[0] == 'TEXT':
            setup_text_world(robot_name)
        else:
            setup_text_world(robot_name)
    else:
        setup_text_world(robot_name)
