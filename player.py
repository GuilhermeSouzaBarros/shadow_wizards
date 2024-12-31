from pyray import *
from raylib import *

from math import atan2, degrees

from utils import SMALL_FLOAT
from imaginary import Imaginary
from vectors import Vector2
from lines import ColLines
from shapes import Circle
from sword import Sword


class Player:
    def __init__(self, tile_size:float,
                 start_row:int, start_column:int, start_angle:list,
                 player_id:int, map_id:int,
                 nick:str, sprite:str, color:Color) -> None:
        self.tile_size   = tile_size

        pos = Vector2(tile_size * (start_column + 0.5),
                      tile_size * (start_row    + 0.5))
        self.start_pos = Vector2(
            tile_size * (start_column + 0.5),
            tile_size * (start_row    + 0.5)
        )
        self.start_angle = Imaginary(start_angle[0], start_angle[1])

        self.hitbox      = Circle(pos, tile_size * 0.4)
        self.color       = color
        self.is_alive    = True
        self.respawn     = 2
        self.start_time  = 0
        self.angle       = Imaginary(start_angle[0], start_angle[1])

        self.sword = Sword(pos)
        
        self.kills  = 0
        self.deaths = 0

        self.nick   = nick
        self.sprite = load_texture(sprite)

        self.player_id = player_id
        self.team = player_id if map_id == 1 else (player_id == 2 or player_id == 4) + 1

        self.has_flag = False

        self.in_vision = [self.team]

    def update_angle(self) -> None:
        if (self.player_id == 1):
            if (is_key_down(KEY_W)):
                self.angle.y -= 1.0
            if (is_key_down(KEY_A)):
                self.angle.x -= 1.0
            if (is_key_down(KEY_S)):
                self.angle.y += 1.0
            if (is_key_down(KEY_D)):
                self.angle.x += 1.0

        elif (self.player_id == 2):
            if (is_key_down(KEY_I) or is_key_down(KEY_UP)):
                self.angle.y -= 1.0
            if (is_key_down(KEY_J) or is_key_down(KEY_LEFT)):
                self.angle.x -= 1.0
            if (is_key_down(KEY_K) or is_key_down(KEY_DOWN)):
                self.angle.y += 1.0
            if (is_key_down(KEY_L) or is_key_down(KEY_RIGHT)):
                self.angle.x += 1.0

    def update_player_pos(self) -> None:
        speed = self.tile_size * 4.0
        if (is_key_down(KEY_LEFT_CONTROL)):
            speed *= 0.1
        elif (is_key_down(KEY_LEFT_SHIFT)):
            speed *= 5
        previous_angle = self.angle

        self.angle = Vector2(0.0, 0.0)
        self.update_angle()
        
        if (self.angle.module()):
            self.angle.to_module(1.0)
            self.hitbox.speed.x = self.angle.x * speed
            self.hitbox.speed.y = self.angle.y * speed
            self.angle = Imaginary(self.angle.x, self.angle.y)
        else:
            self.angle = previous_angle
            self.hitbox.speed = Vector2(0, 0)
        

    def update_vision(self) -> None:
        pass

    def update(self) -> None:
        if self.is_alive:
            self.update_player_pos()
                        
        elif (get_time() - self.start_time >= self.respawn):
            self.is_alive = True
            self.hitbox.position = self.start_pos.copy()
            self.angle           = self.start_angle.copy()
        
        self.in_vision = [self.team]

    def killed(self):
        self.kills += 1

    def died(self):
        self.deaths += 1
        self.is_alive = False
        self.has_flag = False
        self.start_time = get_time()
        self.hitbox.speed = Vector2(0, 0)

        self.sword.deactivate()

        
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


    def draw(self, map_offset:Vector2, scaler:float, hitbox:bool) -> None:
        color = self.color
        color = (color[0], color[1], color[2], int(color[3] / (2 - (not self.has_flag and self.is_alive))))
        if (hitbox):
            self.hitbox.draw(map_offset, scaler, color)
        else:
            angle = degrees(atan2(self.angle.imaginary, self.angle.real))
            angle += 360 * (angle < 0.0)
            angle /= 45
            angle = int(angle)
            offset = self.hitbox.radius * 0.5

            pos = [map_offset.x + ((self.hitbox.position.x - self.hitbox.radius) * scaler),
                   map_offset.y + ((self.hitbox.position.y - self.hitbox.radius) * scaler)]
            rectangle_dest = [pos[0], pos[1],
                            scaler * (self.hitbox.radius + offset) * 2,
                            scaler * (self.hitbox.radius + offset) * 2]

            draw_texture_pro(self.sprite, [0, angle * 32, 32, 32], rectangle_dest, [offset * scaler, 2 * offset * scaler], 0, color)

        self.sword.draw(map_offset, scaler, color)
    