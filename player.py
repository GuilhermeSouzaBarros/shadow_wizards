from pyray import *
from raylib import *

from aux import SMALL_FLOAT
from imaginary import Imaginary
from vectors import Vector2
from lines import ColLines
from shapes import Circle
from sword import Sword


class Player:
    def __init__(self, tile_size:Vector2, scaler:float, map_pos:Vector2,
                 draw_size:Vector2, color:Color,
                 start_row:int, start_column:int,
                 nick:str,
                 sprite:str) -> None:
        
        pos = Vector2(tile_size.x * (start_column + 0.5),
                      tile_size.y * (start_row    + 0.5))
        self.start_pos = Vector2(tile_size.x * (start_column + 0.5),
                      tile_size.y * (start_row    + 0.5))
        self.hitbox    = Circle(pos, tile_size.x * 0.4)
        self.tile_size = tile_size
        self.scaler    = scaler
        self.map_pos   = map_pos
        self.draw_size = draw_size
        self.color     = color
        self.is_alive  = True
        self.respawn   = 2
        self.start_time = 0
        self.angle = Imaginary()

        self.sword = Sword(pos, self.map_pos, self.scaler)
        
        self.kills  = 0
        self.deaths = 0

        self.nick   = nick
        self.sprite = load_texture(sprite)

    def update_player_pos(self, player_number:int) -> None:
        speed = self.tile_size.x * 4.0
        if (is_key_down(KEY_LEFT_CONTROL)):
            speed *= 0.1
        elif (is_key_down(KEY_LEFT_SHIFT)):
            speed *= 10
        previous_angle = self.angle
        self.angle = Vector2(0.0, 0.0)

        if (player_number == 0):
            if (is_key_down(KEY_W)):
                self.angle.y -= 1.0
            if (is_key_down(KEY_A)):
                self.angle.x -= 1.0
            if (is_key_down(KEY_S)):
                self.angle.y += 1.0
            if (is_key_down(KEY_D)):
                self.angle.x += 1.0
            if is_key_pressed(KEY_SPACE):
                self.sword.activate()

        elif (player_number == 1):
            if (is_key_down(KEY_I) or is_key_down(KEY_UP)):
                self.angle.y -= 1.0
            if (is_key_down(KEY_J) or is_key_down(KEY_LEFT)):
                self.angle.x -= 1.0
            if (is_key_down(KEY_K) or is_key_down(KEY_DOWN)):
                self.angle.y += 1.0
            if (is_key_down(KEY_L) or is_key_down(KEY_RIGHT)):
                self.angle.x += 1.0
            if is_key_pressed(KEY_ENTER):
                self.sword.activate()
        
        if (self.angle.module()):
            self.angle.to_module(1.0)
            self.hitbox.speed.x = self.angle.x * speed
            self.hitbox.speed.y = self.angle.y * speed
            self.angle = Imaginary(self.angle.x, self.angle.y)
        else:
            self.angle = previous_angle
            self.hitbox.speed = Vector2(0, 0)

    def update(self, player_number:int) -> None:
        if self.is_alive:
            self.update_player_pos(player_number)
            self.sword.update(self.hitbox.position, self.angle)
                        
        elif (get_time() - self.start_time >= self.respawn):
            self.is_alive = True

    def killed(self):
        self.kills += 1

    def died(self):
        self.deaths += 1
        self.is_alive = False
        self.start_time = get_time()
        self.hitbox.position = self.start_pos.copy()

        
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
        offset = self.hitbox.radius * 0.5

        pos = [self.map_pos.x + ((self.hitbox.position.x - self.hitbox.radius) * self.scaler),
               self.map_pos.y + ((self.hitbox.position.y - self.hitbox.radius) * self.scaler)]
        rectangle_dest = [pos[0], pos[1],
                          self.scaler * (self.hitbox.radius + offset) * 2,
                          self.scaler * (self.hitbox.radius + offset) * 2]

        if (self.angle.real == 1.0 and self.angle.imaginary == 0.0):
            draw_texture_pro(self.sprite, [0, 32, 32, 32], rectangle_dest, [offset * self.scaler, 2 * offset * self.scaler], 0, self.color)

        elif (self.angle.real == 0.0 and self.angle.imaginary == 1.0):
            draw_texture_pro(self.sprite, [0, 0, 32, 32], rectangle_dest, [offset * self.scaler, 2 * offset * self.scaler], 0, self.color)

        elif (self.angle.real == -1.0 and self.angle.imaginary == 0.0):
            draw_texture_pro(self.sprite, [0, 96, 32, 32], rectangle_dest, [offset * self.scaler, 2 * offset * self.scaler], 0, self.color)

        elif (self.angle.real == 0.0 and self.angle.imaginary == -1.0):
            draw_texture_pro(self.sprite, [0, 64, 32, 32], rectangle_dest, [offset * self.scaler, 2 * offset * self.scaler], 0, self.color)

        else:

            pos = [self.map_pos.x + ((self.hitbox.position.x) * self.scaler),
                   self.map_pos.y + ((self.hitbox.position.y) * self.scaler)]
            draw_circle_v(pos, self.hitbox.radius * self.scaler, self.color)
        self.sword.draw()
        
    