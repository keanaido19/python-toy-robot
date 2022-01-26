from __future__ import annotations
from typing import TypeVar, Callable, Generic, Optional
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
    return coordinate[1] >= right_edge - 1


def check_left_edge(coordinate: tuple[int, int]) -> bool:
    """
    Checks if the given coordinate is at the left edge of the maze
    :param tuple[int, int] coordinate: x and y coordinate
    :return: Boolean value
    """
    global left_edge
    return coordinate[1] <= left_edge + 1


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


def node_to_path(node: Node) -> list[T]:
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
        self._container: list[T] = []

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


def astar(start: tuple[int, int], check_completed: Callable[[T], bool],
          adjacent_coordinates: Callable[[T], list[T]],
          distance: Callable[[T], int]) -> Optional[list[tuple[int, int]]]:
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


from maze import medium_maze


medium_maze.generate_maze()
get_obstacle_coordinates()
bottom_edge, top_edge = -200, 200
left_edge, right_edge = -100, 100


def maze_run(start_x: int, start_y: int, llx, lly, urx, ury, goal: str = 'top'):
    global top_edge, bottom_edge, right_edge, left_edge
    top_edge = ury
    bottom_edge = lly
    right_edge = urx
    left_edge = llx
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
