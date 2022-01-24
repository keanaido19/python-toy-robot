from maze import obstacles
import turtle

# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100


def show_position(robot_name) -> None:
    """
    Updates the position of the robot on the turtle screen
    :param robot_name: Name of the robot
    :return: None
    """
    if current_direction_index == 0:
        robot.setheading(90)
    elif current_direction_index == 1:
        robot.setheading(0)
    elif current_direction_index == 2:
        robot.setheading(270)
    else:
        robot.setheading(180)
    robot.goto(position_x, position_y)


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
    Update the current x and y positions given the current direction, and specific nr of steps
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


def create_turtle_screen() -> None:
    """
    Creates a turtle screen and sets the screen size
    :return: None
    """
    turtle.Screen().setup(max_x * 2 + max_x // 2, max_y * 2 + max_y // 2)


def draw_world_boundary() -> None:
    """
    Draws a boundary based on the world area limit variables
    :return: None
    """
    shape = turtle.Shape('compound')
    poly1 = ((-min_y, min_x), (-min_y, max_x), (-max_y, max_x), (-max_y, min_x))
    shape.addcomponent(poly=poly1, fill='', outline='red')
    turtle.register_shape('boundary', shape)
    turtle.Turtle(shape='boundary')


def draw_obstacles() -> None:
    """
    Draws obstacles on turtle screen
    :return: None
    """
    obstacles.create_square_obstacle()
    pen = turtle.Turtle()
    pen.fillcolor('red')
    pen.hideturtle()
    pen.speed('fastest')
    for obstacle in obstacles.obstacles:
        pen.penup()
        for position in obstacle:
            pen.goto(*position)
            pen.pendown()


create_turtle_screen()
draw_world_boundary()
draw_obstacles()
robot = turtle.Turtle()
robot.penup()
robot.speed('fastest')
robot.setheading(90)



