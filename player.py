from pyray import *
from raylib import *

from vectors import Vector2
from shapes import Circle

class Player:
    def __init__(self, tile_size:Vector2, scaler:float, map_pos:Vector2,
                 draw_size:Vector2, color:Color,
                 start_row:int, start_column:int) -> None:
        pos = Vector2(tile_size.x * (start_column + 0.5),
                      tile_size.y * (start_row    + 0.5))
        self.hitbox    = Circle(pos, tile_size.x * 0.4)
        self.tile_size = tile_size
        self.scaler    = scaler
        self.map_pos   = map_pos
        self.draw_size = draw_size
        self.color     = color

    def update(self, player_number:int) -> None:
        speed = self.tile_size.x * 6.0
        if (is_key_down(KEY_LEFT_CONTROL)):
            speed *= 0.1
        vector = Vector2(0.0, 0.0)

        if (player_number == 0):
            if (is_key_down(KEY_W)):
                vector.y -= 1.0
            if (is_key_down(KEY_A)):
                vector.x -= 1.0
            if (is_key_down(KEY_S)):
                vector.y += 1.0
            if (is_key_down(KEY_D)):
                vector.x += 1.0
        elif (player_number == 1):
            if (is_key_down(KEY_I) or is_key_down(KEY_UP)):
                vector.y -= 1.0
            if (is_key_down(KEY_J) or is_key_down(KEY_LEFT)):
                vector.x -= 1.0
            if (is_key_down(KEY_K) or is_key_down(KEY_DOWN)):
                vector.y += 1.0
            if (is_key_down(KEY_L) or is_key_down(KEY_RIGHT)):
                vector.x += 1.0
        module = vector.module()
        if (module):
            vector.x *= speed / module
            vector.y *= speed / module

        self.hitbox.speed = vector

    def draw(self) -> None:
        draw_circle_v([self.map_pos.x + (self.hitbox.position.x * self.scaler),
                      self.map_pos.y + (self.hitbox.position.y * self.scaler)],
                      self.hitbox.radius * self.scaler, self.color)
        