from typing import Tuple

from pyray import *


def is_intersecting(l: Tuple[Vector2, Vector2], rectangle: Rectangle):
    rectangle_lines = [
        (Vector2(rectangle.x, rectangle.y), Vector2(rectangle.x + rectangle.width, rectangle.y)),  # Top line
        (Vector2(rectangle.x, rectangle.y), Vector2(rectangle.x, rectangle.y + rectangle.height)),  # Left line
        (Vector2(rectangle.x + rectangle.width, rectangle.y), Vector2(rectangle.x + rectangle.width, rectangle.y + rectangle.height)),
        (Vector2(rectangle.x, rectangle.y + rectangle.height), Vector2(rectangle.x + rectangle.width, rectangle.y + rectangle.height))
    ]

    for line in rectangle_lines:
        if check_collision_lines(l[0], l[1], line[0], line[1], None):
            return True

    return False
