from pyray import *
from raylib import *

from imaginary import Imaginary
from vectors import Vector2
from shapes import *

class Sword:
    def __init__(self, pos:Vector2, map_pos:Vector2, scaler:float) -> None:
        self.cooldown = 1.0
        self.time_activated = 0.5
        self.last_activation = 0.0
        self.active = False

        self.scaler = scaler
        self.map_pos = map_pos

        pos = pos.copy()
        sword_size = Vector2(40.0, 10.0)
        self.hitbox = Rectangle(Vector2(pos.x + sword_size.x/2, pos.y - sword_size.y/2), sword_size)

        self.color = BLUE
        

    def activate(self) -> None:
        current_time = get_time()
        
        if current_time - self.last_activation >= self.cooldown:
            self.active = True
            self.last_activation = current_time
    

    def update(self, player_pos:Vector2, angle:Imaginary) -> None:
        current_time = get_time()

        # Push sword half x size in facing direction
        size_im_x = Imaginary(self.hitbox.size.x / 2.0, 0.0) * self.hitbox.angle
        self.hitbox.position.x = player_pos.x + size_im_x.real
        self.hitbox.position.y = player_pos.y + size_im_x.imaginary

        self.hitbox.angle = angle.copy()
        if current_time - self.last_activation >= self.time_activated:
            self.active = False
        

    def draw(self) -> None:
        if not self.active:
            return
        self.hitbox.draw(self.map_pos, self.scaler, self.color)
        self.hitbox.draw_lines(self.map_pos, self.scaler, BLACK)
