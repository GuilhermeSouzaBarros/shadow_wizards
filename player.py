from pyray import *
from raylib import *

from aux import SMALL_FLOAT
from vectors import Vector2
from lines import ColLines
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
        speed = self.tile_size.x * 4.0
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

    def col_handle_tile(self, tile:Rectangle, lines_col, delta_time:float) -> None:
        rec_lines = tile.to_lines()
        next_pos = self.hitbox.next_position(delta_time)
        rec_side = tile.in_side_region(self.hitbox.position)
        for i, info in enumerate(lines_col):
            if (rec_side and (info['intersections'] == 2 or
                (info['intersections'] and rec_lines[i].is_point_above(self.hitbox.position)))):
                push_dir = Vector2(rec_lines[i].direction.x, rec_lines[i].direction.y)
                push_dir.rotate_90_anti()
                push_dir.to_module(1.0)
                
                distance = Vector2(tile.size.x / 2 + self.hitbox.radius, tile.size.y / 2 + self.hitbox.radius)
                distance.x -= abs(next_pos.x - tile.position.x)
                distance.y -= abs(next_pos.y - tile.position.y)

                self.hitbox.speed.x += (distance.x * push_dir.x / delta_time)
                self.hitbox.speed.y += (distance.y * push_dir.y / delta_time)
                return

        for i, info_0 in enumerate(lines_col):
            if (not info_0['intersections']):
                continue
            for j, info_1 in enumerate(lines_col):
                if (info_0 == info_1 or not info_1['intersections']):
                    continue

                intersection = ColLines(rec_lines[i], rec_lines[j])

                push_dir = Vector2(next_pos.x - intersection.point.x, next_pos.y - intersection.point.y)
                push_dir.to_module(self.hitbox.radius + SMALL_FLOAT)

                next_pos = Vector2(intersection.point.x + push_dir.x, intersection.point.y + push_dir.y)
                
                self.hitbox.speed.x = (next_pos.x - self.hitbox.position.x) / delta_time
                self.hitbox.speed.y = (next_pos.y - self.hitbox.position.y) / delta_time


    def draw(self) -> None:
        draw_circle_v([self.map_pos.x + (self.hitbox.position.x * self.scaler),
                      self.map_pos.y + (self.hitbox.position.y * self.scaler)],
                      self.hitbox.radius * self.scaler, self.color)
        
    