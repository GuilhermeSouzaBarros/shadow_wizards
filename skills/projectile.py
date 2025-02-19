from skills.skill import *
from math import atan2, degrees
from struct import pack, unpack

class Projectile():
    def __init__(self, pos:Vector2, tile_size:float, duration:float, cooldown:float, 
                 speed: float) -> None:
        """
        Herda classe Skill
        """
        self.last_activation = 0
        self.is_activated = False
        self.tile_size = tile_size
        self.speed_multiplier = speed
        self.hitbox = Circle(pos, tile_size*0.4)
        self.duration = duration
        self._cooldown = cooldown
        self.angle = Imaginary(1, -1)
        self.current_frame = 0
        self.last_animation = 0

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        """
        Ativa bala de acordo com a posição do player e sua direção
        """
        current_time = get_time()
        self.last_activation = current_time
        self.is_activated = True
        self.angle = angle
        self.hitbox.position = player_pos
        self.current_frame_frame = 0
        self.last_animation = current_time

    def deactivate(self):
        self.is_activated = False

    def encode(self) -> bytes:
        message = "".encode()
        if self.is_activated:
            message += pack("dddd", self.hitbox.position.x, self.hitbox.position.y,
                        self.angle.real, self.angle.imaginary)
        return message

    def decode(self, byte_string:bytes, activated:bool) -> int:
        pointer_offset = 0
        self.is_activated = activated
        if activated:
            data = unpack("dddd", byte_string[pointer_offset:pointer_offset+32])
            self.hitbox.position.x = data[0]
            self.hitbox.position.y = data[1]
            self.angle.real = data[2]
            self.angle.imaginary = data[3]
            pointer_offset += 32

        return pointer_offset
    
    def update_time(self):
        if self.is_activated and (get_time() - self.last_animation > 0.2):
            self.last_animation = get_time()
            self.current_frame += 1

    def update(self, *args) -> None:
        """
        Atualiza posição da bala
        """
        
        if get_time() - self.last_activation > self.duration:
            self.deactivate()
        if self.is_activated:
                
            speed = self.tile_size*self.speed_multiplier

            delta_time = get_time() - self.last_activation

            self.hitbox.position.x += speed * self.angle.real * delta_time
            self.hitbox.position.y += speed * self.angle.imaginary * delta_time

    def draw(self, *args) -> None:
        """
        Desenha bala se ativa
        """
        if self.is_activated:
            if not args[-1]:
                self.hitbox.draw(args[0], args[1], args[2])
            if args[-1]:
                angle = degrees(atan2(self.angle.imaginary, self.angle.real))
                offset = self.hitbox.radius*0.5
                scaler = args[2]
                pos = [args[1].x + ((self.hitbox.position.x) * scaler),
                    args[1].y + ((self.hitbox.position.y) * scaler)]
                
                rectangle_dest = [round(pos[0]), round(pos[1]),
                            round(scaler * (self.hitbox.radius + offset) * 2),
                            round(scaler * (self.hitbox.radius + offset) * 2)]
                draw_texture_pro(args[-2], [self.current_frame*32, 0, 32, 32], rectangle_dest, 
                                 [round(offset*scaler), round(2*offset*scaler)], angle, WHITE)
           
        