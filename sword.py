from pyray import *
from raylib import *

from imaginary import Imaginary
from vectors import Vector2
from shapes import *

class Sword:
    def __init__(self, player_pos:Vector2) -> None:
        self.cooldown = 1.0
        self.time_activated = 0.5
        self.last_activation = 0.0
        self.active = False

        player_pos = player_pos.copy()
        sword_size = Vector2(40.0, 10.0)
        self.hitbox = Rectangle(Vector2(player_pos.x + sword_size.x/2, player_pos.y - sword_size.y/2), sword_size)

        self.color = BLUE
        

    def activate(self, player_pos:Vector2, angle:Imaginary, player_id:int) -> None:
        current_time = get_time()
        
        if current_time - self.last_activation >= self.cooldown:
            self.active = True
            self.last_activation = current_time
            self.update(player_pos, angle, player_id)
    
    def deactivate(self) -> None:
        self.active = False

    def update(self, player_pos:Vector2, angle:Imaginary, player_id:int) -> None:
        if self.active:
            current_time = get_time()

            # Push sword half of x size in facing direction
            player_pos = player_pos.copy()
            self.hitbox.angle = angle.copy()
            size_im_x = Imaginary(self.hitbox.size.x / 2.0, 0.0) * self.hitbox.angle
            player_pos.x += size_im_x.real
            player_pos.y += size_im_x.imaginary
            self.hitbox.position = player_pos

            if current_time - self.last_activation >= self.time_activated:
                self.deactivate()
        else:
            if ((player_id == 1 and is_key_pressed(KEY_SPACE)) or
                (player_id == 2 and is_key_pressed(KEY_ENTER))):
                self.activate(player_pos, angle, player_id)

    def draw(self, map_offset:Vector2, scaler:float, color:Color) -> None:
        if not self.active:
            return
        self.hitbox.draw (map_offset, scaler, color)
