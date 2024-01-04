import math
from typing import Tuple
from game.utils.raycasts import *
from game.utils.res_loader import load_imageres
from raylib import Vector2Subtract, Vector2Add, Vector2Rotate
from game.utils.game_getter import GAME_GETTER

from game.config import *

PLAYER_SIZE = 40, 40
WEAPON_SIZE = 80, 30


def rotate_point(point, center_x, center_y, angle):
    """Rotate a point counterclockwise by a given angle around a given center."""
    x, y = point.x, point.y
    cx, cy = center_x, center_y

    # Translate the point so that the center of rotation is at the origin
    x -= cx
    y -= cy

    # Perform the rotation
    x_new = x * math.cos(angle) - y * math.sin(angle)
    y_new = x * math.sin(angle) + y * math.cos(angle)

    # Translate the point back
    x_new += cx
    y_new += cy

    return Vector2(x_new, y_new)


class Player:
    _pos: Tuple[int, int] = (0, 0)
    _name: str = 'Player'
    _health: int = 100
    _local: bool = False
    _id: int = 0
    _weapon_angle = 90
    _shoot_timer = 0

    IMAGE_AK_47 = load_imageres("weapon/ak47.png")


    # region getters/setters
    @property
    def player_id(self):
        return self._id

    @property
    def is_local(self):
        return self._local

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, pos: Tuple[int, int]):
        self._pos = pos

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, health: int):
        self._health = health

    @property
    def name(self) -> str:
        return self._name

    # endregion

    def __init__(self, position: Tuple[int, int], name: str, health: int, local: bool, id: int) -> None:
        self._pos = position
        self._name = name
        self._health = health
        self._local = local
        self._id = id

    def draw(self):
        draw_text(self.name, self.position[0] + PLAYER_SIZE[0] // 2 - measure_text(self.name, 16) // 2,
                  self.position[1] - PLAYER_SIZE[1] - 28, 16, RAYWHITE)
        draw_circle_lines(self.position[0] + PLAYER_SIZE[0] // 2, self.position[1] + PLAYER_SIZE[1] // 2,
                          PLAYER_SIZE[0],
                          RAYWHITE)
        draw_rectangle_lines(self.position[0], self.position[1] - PLAYER_SIZE[1] - 10, PLAYER_SIZE[0] + 3, 15 + 3,
                             RAYWHITE)
        draw_rectangle(self.position[0] + 3, self.position[1] - PLAYER_SIZE[1] - 10 + 3,
                       int(self.health / 100 * PLAYER_SIZE[0]) - 3, 15 - 3, GREEN)

        draw_texture_ex(Player.IMAGE_AK_47(), Vector2(
            int(self.position[0] + PLAYER_SIZE[0] // 2),
            int(self.position[1] + PLAYER_SIZE[1] // 2),
        ), math.degrees(self._weapon_angle), 0.1, WHITE)

    def tick(self):
        if self.is_local:
            if is_key_down(KeyboardKey.KEY_A):
                self.position = (self.position[0] - 1, self.position[1])
            elif is_key_down(KeyboardKey.KEY_D):
                self.position = (self.position[0] + 1, self.position[1])
            elif is_key_down(KeyboardKey.KEY_W):
                self.position = (self.position[0], self.position[1] - 1)
            elif is_key_down(KeyboardKey.KEY_S):
                self.position = (self.position[0], self.position[1] + 1)

            mouse_pos = get_mouse_position()
            direction = Vector2Subtract(mouse_pos, get_world_to_screen_2d(self.position, GAME_GETTER["get"]().camera))
            a = math.atan2(direction.y, direction.x)
            self._weapon_angle = a

            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT) and get_time() - self._shoot_timer > 200/1000:
                self._shoot_timer = get_time()
                for player in GAME_GETTER["get"]().players:
                    if player.player_id == self.player_id:
                        continue
                    p = Vector2(
                        int(self.position[0] + PLAYER_SIZE[0] // 2),
                        int(self.position[1] + PLAYER_SIZE[1] // 2),
                    )
                    pp = Vector2Add(p, Vector2Rotate(Vector2(1000, 0), self._weapon_angle))
                    if is_intersecting((p,pp), Rectangle(
                            int(player.position[0] + PLAYER_SIZE[0] // 2) - int(PLAYER_SIZE[0] // 2),
                            int(player.position[1] + PLAYER_SIZE[1] // 2) - int(PLAYER_SIZE[1] // 2),
                            PLAYER_SIZE[0], PLAYER_SIZE[1]
                    )):
                        player.health -= 30
