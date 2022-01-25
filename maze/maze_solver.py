from typing import TypeVar, Callable
from maze import obstacles
from collections import deque

T = TypeVar('T')

coordinates = []


def get_obstacle_coordinates() -> None:
    """
    Unpacks every obstacle coordinate into a list
    :return: None
    """
    global coordinates
    for obstacle in obstacles.obstacles:
        for position in obstacle:
            coordinates.append(position)


def bfs(start: tuple[int, int], goal_test: Callable[[T], bool], neighbours:
        Callable[[T], list[T]]):
    # frontier is where we've yet to go
    frontier = deque()
    frontier.append(start)
    # explored is where we've been
    explored = {start}

    # keep going while there is more to explore
    while frontier:
        current_node = frontier.popleft()
        # if we found the goal, we're done
        if goal_test(current_node):
            return 'yay'
        # check where we can go next and haven't explored
        for child in neighbours(current_node):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.append(child)
    return None  # went through everything and never found goal


def get_adjacent_coordinates(coordinate: tuple[int, int]) -> list[tuple[int,
                                                                        int]]:
    """
    Returns a list of adjacent non-obstructed coordinates to the given
    coordinate
    :param tuple[int, int] coordinate: x and y coordinate
    :return: A list of adjacent non-obstructed coordinates
    """
    global coordinates
    adjacent_coordinates = []
    if (coordinate[0] + 1, coordinate[1]) not in coordinates:
        adjacent_coordinates.append((coordinate[0] + 1, coordinate[1]))
    if (coordinate[0] - 1, coordinate[1]) not in coordinates:
        adjacent_coordinates.append((coordinate[0] - 1, coordinate[1]))
    if (coordinate[0], coordinate[1] + 1) not in coordinates:
        adjacent_coordinates.append((coordinate[0], coordinate[1] + 1))
    if (coordinate[0], coordinate[1] - 1) not in coordinates:
        adjacent_coordinates.append((coordinate[0], coordinate[1] - 1))
    return adjacent_coordinates


def check_top_edge(coordinate: tuple[int, int]) -> bool:
    return coordinate[1] >= 199


from maze import extreme_maze


extreme_maze.generate_maze()
get_obstacle_coordinates()

print(bfs((0, 0), check_top_edge, get_adjacent_coordinates))
