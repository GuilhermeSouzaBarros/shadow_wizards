from pyray import *
from raylib import *

from vectors import Vector2
from shapes import Circle

class Player:
    def __init__(self, tile_size:Vector2) -> None:
        pos = Vector2(tile_size.x * 1.5, tile_size.y * 1.5)
        self.hitbox    = Circle(pos, tile_size.x * 0.4)
        self.tile_size = tile_size

    def update(self) -> None:
        speed = self.tile_size.x * 3.0
        if (is_key_down(KEY_LEFT_CONTROL)):
            speed *= 0.1
        vector = Vector2(0.0, 0.0)
        if (is_key_down(KEY_W) or is_key_down(KEY_UP)):
            vector.y -= 1.0
        if (is_key_down(KEY_A) or is_key_down(KEY_LEFT)):
            vector.x -= 1.0
        if (is_key_down(KEY_S) or is_key_down(KEY_DOWN)):
            vector.y += 1.0
        if (is_key_down(KEY_D) or is_key_down(KEY_RIGHT)):
            vector.x += 1.0
        module = vector.module()
        if (module):
            vector.x *= speed / module
            vector.y *= speed / module

        self.hitbox.speed = vector

    def draw(self) -> None:
        draw_circle(int(self.hitbox.position.x), int(self.hitbox.position.y), self.hitbox.radio, GOLD)