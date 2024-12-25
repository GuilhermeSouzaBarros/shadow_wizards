from pyray import *
from raylib import *


from collisions import ColRectangleCircle
from shapes import *

class Sword:
    def __init__(self, pos:Vector2, speed:float, size:Vector2, angle:float,
                 scaler:float, map_pos:Vector2) -> None:
        self.size = size
        self.cooldown = 1.0
        self.time_activated = 0.5
        self.active = False
        self.color = BLUE
        self.hitbox = Rectangle(pos, size, angle)
        self.last_activation = 0.0
        self.player_pos = pos
        self.scaler = scaler
        self.map_pos = map_pos
        self.angle = angle
        

    def activate(self):
        current_time = get_time()
        
        if current_time - self.last_activation >= self.cooldown:
            self.active = True
            self.last_activation = current_time
        

    def update(self, player_pos:Vector2, angle:float) -> None:
        current_time = get_time()
        self.player_pos = player_pos
        self.hitbox.position = Vector2(player_pos.x, player_pos.y)
        self.angle = angle
        if current_time - self.last_activation >= self.time_activated:
            self.active = False
        
        
    
    def draw(self, scaler:float) -> None:
        if self.active:
            self.scaler = scaler
            pos = [self.map_pos.x + (self.player_pos.x * self.scaler),
                        self.map_pos.y + (self.player_pos.y * self.scaler)]
            
            draw_rectangle_pro([pos[0], pos[1], (self.hitbox.size.x + 30)*self.scaler, self.hitbox.size.y], [self.size.x/2, self.size.y/2], self.angle, self.color)
        
