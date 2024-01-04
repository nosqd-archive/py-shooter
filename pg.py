from pyray import *
import math

from raylib import Vector2Subtract, Vector2Add, Vector2Rotate


class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.angle = 0


class Bullet:
    def __init__(self, position, angle):
        self.position = position
        self.velocity = Vector2(math.cos(angle), math.sin(angle))


class Game:
    def __init__(self):
        self.player = Player(400, 300)
        self.bullets = []

    def update(self):
        # Обработка ввода пользователя
        if is_key_pressed(KeyboardKey.KEY_LEFT):
            self.player.angle -= 0.1
        elif is_key_pressed(KeyboardKey.KEY_RIGHT):
            self.player.angle += 0.1

        # Создание пули
        if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos = Vector2(get_mouse_x(), get_mouse_y())
            direction = Vector2Subtract(mouse_pos, self.player.position)
            self.bullets.append(Bullet(self.player.position, math.atan2(direction.y, direction.x)))

        for bullet in self.bullets:
            bullet.position = Vector2(bullet.position.x+bullet.velocity.x, bullet.position.y+bullet.velocity.y)
    # def draw(self):
    #     # Рисуем игрока и его линию
    #     begin_drawing()
    #     clear_background(BLACK)
    #     draw_circle_v(self.player.position, 50, WHITE)
    #     draw_line(int(self.player.position.x), int(self.player.position.y),
    #               int(self.player.position.x + math.cos(self.player.angle) * 100),
    #               int(self.player.position.y + math.sin(self.player.angle) * 100),
    #               RED)
    #
    #     # Рисуем пули
    #     for bullet in self.bullets:
    #         draw_circle_v(bullet.position, 5, YELLOW)
    #
    #     end_drawing()

    def draw(self):
        # Рисуем игрока
        begin_drawing()
        clear_background(BLACK)
        draw_circle_v(self.player.position, 50, WHITE)

        # Вычисляем вектор от игрока до мыши
        mouse_pos = get_mouse_position()
        direction = Vector2Subtract(mouse_pos, self.player.position)
        angle_difference = math.atan2(direction.y, direction.x) - self.player.angle
        rotated_line_end = Vector2Add(self.player.position,
                                      Vector2Rotate(Vector2(20, 0), self.player.angle + angle_difference))
        a = math.atan2(direction.y, direction.x)
        normalized_line = (
            math.cos(a),
            math.sin(a)
        )


        draw_text(f"Line: {int(normalized_line[0]*1000)/1000} {int(normalized_line[1]*1000)/1000} ", 5, 5, 16, RAYWHITE)
        draw_line(50, 50, int(50+(normalized_line[0]*10)), int(50*(normalized_line[1]*10)), RAYWHITE)
        # Рисуем линию
        draw_line(int(self.player.position.x), int(self.player.position.y),
                         int(rotated_line_end.x), int(rotated_line_end.y),
                         RED)

        # Рисуем пули
        for bullet in self.bullets:
            draw_circle_v(bullet.position, 5, YELLOW)

        end_drawing()


game = Game()
init_window(800, 600, "game")
while not window_should_close():
    game.update()
    game.draw()
