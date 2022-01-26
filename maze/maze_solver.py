from __future__ import annotations
from typing import TypeVar, Callable, Optional
from maze import obstacles
from heapq import heappush, heappop

T = TypeVar('T')

top_edge: int
bottom_edge: int
right_edge: int
left_edge: int
obstacle_coordinates = []


def get_obstacle_coordinates() -> None:
    """
    Unpacks every obstacle coordinate into a list
    :return: None
    """
    global obstacle_coordinates
    for obstacle in obstacles.obstacles:
        for position in obstacle:
            obstacle_coordinates.append(position)


def get_adjacent_coordinates(coordinate: tuple[int, int]) \
        -> list[tuple[int, int]]:
    """
    Returns a list of adjacent non-obstructed coordinates to the given
    coordinate
    :param tuple[int, int] coordinate: x and y coordinate
    :return: A list of adjacent non-obstructed coordinates
    """
    global obstacle_coordinates, top_edge, bottom_edge, right_edge, left_edge
    adjacent_coordinates = []
    if (coordinate[0] + 1, coordinate[1]) not in obstacle_coordinates\
            and (coordinate[0] + 1) <= right_edge:
        adjacent_coordinates.append((coordinate[0] + 1, coordinate[1]))
    if (coordinate[0] - 1, coordinate[1]) not in obstacle_coordinates\
            and (coordinate[0] - 1) >= left_edge:
        adjacent_coordinates.append((coordinate[0] - 1, coordinate[1]))
    if (coordinate[0], coordinate[1] + 1) not in obstacle_coordinates\
            and (coordinate[1] + 1) <= top_edge:
        adjacent_coordinates.append((coordinate[0], coordinate[1] + 1))
    if (coordinate[0], coordinate[1] - 1) not in obstacle_coordinates\
            and (coordinate[1] - 1) >= bottom_edge:
        adjacent_coordinates.append((coordinate[0], coordinate[1] - 1))
    return adjacent_coordinates


def check_top_edge(coordinate: tuple[int, int]) -> bool:
    """
    Checks if the given coordinate is at the top edge of the maze
    :param tuple[int, int] coordinate: x and y coordinate
    :return: Boolean value
    """
    global top_edge
    return coordinate[1] >= top_edge - 1


def check_bottom_edge(coordinate: tuple[int, int]) -> bool:
    """
    Checks if the given coordinate is at the bottom edge of the maze
    :param tuple[int, int] coordinate: x and y coordinate
    :return: Boolean value
    """
    global bottom_edge
    return coordinate[1] <= bottom_edge + 1


def check_right_edge(coordinate: tuple[int, int]) -> bool:
    """
    Checks if the given coordinate is at the right edge of the maze
    :param tuple[int, int] coordinate: x and y coordinate
    :return: Boolean value
    """
    global right_edge
    return coordinate[0] >= right_edge - 1


def check_left_edge(coordinate: tuple[int, int]) -> bool:
    """
    Checks if the given coordinate is at the left edge of the maze
    :param tuple[int, int] coordinate: x and y coordinate
    :return: Boolean value
    """
    global left_edge
    return coordinate[0] <= left_edge + 1


def get_distance_top_edge(coordinate: tuple[int, int]) -> int:
    """
    Returns the distance of the coordinate from the top edge
    :param coordinate: x and y coordinate
    :return: The distance of the coordinate from the top edge
    """
    global top_edge
    return top_edge - coordinate[1]


def get_distance_bottom_edge(coordinate: tuple[int, int]) -> int:
    """
    Returns the distance of the coordinate from the bottom edge
    :param coordinate: x and y coordinate
    :return: The distance of the coordinate from the bottom edge
    """
    global bottom_edge
    return abs(bottom_edge - coordinate[1])


def get_distance_right_edge(coordinate: tuple[int, int]) -> int:
    """
    Returns the distance of the coordinate from the right edge
    :param coordinate: x and y coordinate
    :return: The distance of the coordinate from the right edge
    """
    global right_edge
    return right_edge - coordinate[0]


def get_distance_left_edge(coordinate: tuple[int, int]) -> int:
    """
    Returns the distance of the coordinate from the left edge
    :param coordinate: x and y coordinate
    :return: The distance of the coordinate from the left edge
    """
    global left_edge
    return abs(left_edge - coordinate[0])


class Node:
    """
    A node is a coordinate with additional information that is used for
    additional comparison and calculations
    """
    position: tuple[int, int]
    parent: Optional[Node]
    distance_from_start: int
    distance_to_goal: int

    def __init__(self, position: tuple[int, int], parent: Optional[Node],
                 distance_from_start: int = 0, distance_to_goal: int = 0) \
            -> None:
        """Constructor for Node"""
        self.position = position
        self.parent = parent
        self.distance_from_start = distance_from_start
        self.distance_to_goal = distance_to_goal

    def __lt__(self, other: Node) -> bool:
        """Less than comparison"""
        return (self.distance_from_start + self.distance_to_goal) \
            < (other.distance_from_start + other.distance_to_goal)


def node_to_path(node: Node) -> list[tuple[int, int]]:
    """
    Converts the Node to a path of coordinates based on its parent node
    :param node: Node object
    :return: List of coordinates
    """
    path = [node.position]
    while node.parent is not None:
        node = node.parent
        path.append(node.position)
    path.reverse()
    return path


class PriorityQueue:
    """
    Priority queue data structure where each element has a weight/value that
    defines its priority
    """
    def __init__(self) -> None:
        """Constructor for the PriorityQueue"""
        self._container: list[Node] = []

    @property
    def empty(self) -> bool:
        """
        Checks if list is empty
        :return: Boolean value
        """
        return not self._container

    def append(self, node: Node) -> None:
        """Adds to the list using heappush method"""
        heappush(self._container, node)

    def pop(self) -> Node:
        """pops an element from the list using heappop method"""
        return heappop(self._container)

    def __repr__(self) -> str:
        """
        Representation of the PriorityQueue Class
        :return: String representation of the Class
        """
        return repr(self._container)


def astar(start: tuple[int, int],
          check_completed: Callable[[tuple[int, int]], bool],
          adjacent_coordinates: Callable[[tuple[int, int]], list[tuple[int,
                                                                       int]]],
          distance: Callable[[tuple[int, int]], int]
          ) -> Optional[list[tuple[int, int]]]:
    """
    Astar algorithm that solves a maze by checking adjacent coordinates and
    moving to them provided they have not already been explored-however astar
    using approximation to the goal to pick the next coordinate to go to
    :param tuple[int, int] start: Starting x and y coordinate
    :param Callable[[T], bool] check_completed: Function that checks if maze is
    solved
    :param Callable[[T], list[T]] adjacent_coordinates: Function that returns
    the adjacent coordinates
    :param Callable[[T], int] distance: Function that returns the distance of
    the coordinate from the goal
    :return:
    """
    frontier = PriorityQueue()
    frontier.append(Node(start, None, 0, distance(start)))
    explored = {start: 0}

    while not frontier.empty:
        current_node = frontier.pop()
        current_position = current_node.position

        if check_completed(current_position):
            return node_to_path(current_node)

        for child in adjacent_coordinates(current_position):
            cost_new_node = current_node.distance_from_start + 1

            if child not in explored or explored[child] > cost_new_node:
                explored[child] = cost_new_node
                frontier.append(
                    Node(child, current_node, cost_new_node, distance(child))
                )
    return None


def path_to_robot_commands(path: list[tuple[int, int]],
                           robot_direction: int) -> list[str]:
    """
    Converts a path of coordinates into commands that the robot can execute
    :param list[tuple[int, int]] path: Path of coordinates
    :param int robot_direction: Direction index of the robot
    :return: List of robot commands
    """
    robot_commands: list[str] = []
    for i in range(len(path) - 1):
        current_position: tuple[int, int] = path[i]
        next_position: tuple[int, int] = path[i + 1]
        if current_position[0] == next_position[0]:
            if current_position[1] > next_position[1]:
                if robot_direction == 0:
                    robot_commands.append('back 1')
                elif robot_direction == 1:
                    robot_commands.append('right')
                    robot_commands.append('forward 1')
                    robot_direction = 2
                elif robot_direction == 3:
                    robot_commands.append('left')
                    robot_commands.append('forward 1')
                    robot_direction = 2
                else:
                    robot_commands.append('forward 1')
            else:
                if robot_direction == 0:
                    robot_commands.append('forward 1')
                elif robot_direction == 1:
                    robot_commands.append('left')
                    robot_commands.append('forward 1')
                    robot_direction = 0
                elif robot_direction == 3:
                    robot_commands.append('right')
                    robot_commands.append('forward 1')
                    robot_direction = 0
                else:
                    robot_commands.append('back 1')
        else:
            if current_position[0] < next_position[0]:
                if robot_direction == 0:
                    robot_commands.append('right')
                    robot_commands.append('forward 1')
                    robot_direction = 1
                elif robot_direction == 1:
                    robot_commands.append('forward 1')
                elif robot_direction == 3:
                    robot_commands.append('back 1')
                else:
                    robot_commands.append('left')
                    robot_commands.append('forward 1')
                    robot_direction = 1
            else:
                if robot_direction == 0:
                    robot_commands.append('left')
                    robot_commands.append('forward 1')
                    robot_direction = 3
                elif robot_direction == 1:
                    robot_commands.append('back 1')
                elif robot_direction == 3:
                    robot_commands.append('forward 1')
                else:
                    robot_commands.append('right')
                    robot_commands.append('forward 1')
                    robot_direction = 3
    return robot_commands


def simplify_robot_commands(robot_commands: list[str]) -> list[str]:
    """
    Returns a list of simplified robot commands
    :param robot_commands: List of robot commands
    :return: A list of simplified robot commands
    """
    robot_commands.append('end')
    simplified_robot_command_list: list[str] = []
    for i, _ in enumerate(robot_commands):
        if robot_commands[i] == 'forward 1':
            c = i
            while robot_commands[i] == 'forward 1':
                robot_commands.pop(i)
                c += 1
            simplified_robot_command_list.append(f'forward {c - i}')
        if robot_commands[i] == 'back 1':
            c = i
            while robot_commands[i] == 'back 1':
                robot_commands.pop(i)
                c += 1
            simplified_robot_command_list.append(f'back {c - i}')
        if robot_commands[i] in ['left', 'right']:
            simplified_robot_command_list.append(robot_commands[i])
    return simplified_robot_command_list


def maze_run(start_x: int, start_y: int, start_direction: int,
             llx, lly, urx, ury, goal: str) -> list[str]:
    """
    Handler for the maze solving algorithm
    :param int start_x: Starting x position
    :param int start_y: Starting y position
    :param int start_direction: Starting direction index
    :param int llx: Lower left x coordinate
    :param int lly: Upper x coordinate
    :param int urx: Lower left y coordinate
    :param int ury: Upper y coordinate
    :param str goal: Maze edge we with to arrive at
    :return: List of robot commands
    """
    global top_edge, bottom_edge, right_edge, left_edge
    top_edge = ury
    bottom_edge = lly
    right_edge = urx
    left_edge = llx
    path: list[tuple[int, int]] = []
    get_obstacle_coordinates()
    if goal == 'top':
        path = astar(
            (start_x, start_y), check_top_edge,
            get_adjacent_coordinates, get_distance_top_edge
        )
    elif goal == 'bottom':
        path = astar(
            (start_x, start_y), check_bottom_edge,
            get_adjacent_coordinates, get_distance_bottom_edge
        )
    elif goal == 'right':
        path = astar(
            (start_x, start_y), check_right_edge,
            get_adjacent_coordinates, get_distance_right_edge
        )
    elif goal == 'left':
        path = astar(
            (start_x, start_y), check_left_edge,
            get_adjacent_coordinates, get_distance_left_edge
        )
    robot_commands = path_to_robot_commands(path, start_direction)
    return simplify_robot_commands(robot_commands)
