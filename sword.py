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

        self.sprite = load_texture("sprites/sword.png")

        player_pos = player_pos.copy()
        sword_size = Vector2(40.0, 10.0)
        self.hitbox = Rectangle(Vector2(player_pos.x + sword_size.x/2, player_pos.y - sword_size.y/2), sword_size)        

    def activate(self, player_pos:Vector2, angle:Imaginary, player_input:dict) -> None:
        current_time = get_time()
        
        if current_time - self.last_activation >= self.cooldown:
            self.active = True
            self.last_activation = current_time
            self.update(player_pos, angle, player_input)
    
    def deactivate(self) -> None:
        self.active = False

    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict) -> None:
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
            if (player_input["sword"]): self.activate(player_pos, angle, player_input)

    def draw(self, map_offset:Vector2, scaler:float, color:Color) -> None:
        if not self.active:
            return
         
        angle = degrees(atan2(self.hitbox.angle.imaginary, self.hitbox.angle.real))

        size_im_x = Imaginary(self.hitbox.size.x/2.0 - 10, 0)*self.hitbox.angle
        size_im_y = Imaginary(0.0, self.hitbox.size.y/2.0 - 2.5)*self.hitbox.angle
        up_left_corner = [self.hitbox.position.x - size_im_x.real - size_im_y.real,
                              self.hitbox.position.y - size_im_x.imaginary - size_im_y.imaginary]
        offset = Vector2(self.hitbox.size.x*0.5, self.hitbox.size.y*0.5)
        pos = [map_offset.x + ((up_left_corner[0])*scaler), 
                map_offset.y + ((up_left_corner[1])*scaler)]
        rectangle_dest = [round(pos[0]), round(pos[1]),
                        round(scaler*(self.hitbox.size.x + offset.x - 10)),
                        round(scaler*(self.hitbox.size.y + offset.y + 10))]
        draw_texture_pro(self.sprite, [0, 0, 32, 32], rectangle_dest, 
                            [round(offset.x*scaler), round(2*offset.y*scaler)], angle, WHITE)
   
