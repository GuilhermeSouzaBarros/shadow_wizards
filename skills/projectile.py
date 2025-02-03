from skills.skill import *
from math import atan2, degrees

class Projectile(Skill):
    def __init__(self, pos:Vector2, tile_size:float, duration:float, cooldown:float, 
                 speed: float) -> None:
        """
        Herda classe Skill
        """
        super().__init__()
        self.tile_size = tile_size
        self.speed_multiplier = speed
        self.hitbox = Circle(pos, tile_size*0.4)
        self.duration = duration
        self._cooldown = cooldown
        self.angle = Imaginary(1, -1)
        self.current_frame = 0
        self.animation_time = 0.2
        self.last_animation = 0

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        """
        Ativa bala de acordo com a posição do player e sua direção
        """
        super().activate()
        self.angle = angle
        self.hitbox.position = player_pos
        self.current_frame_frame = 0
        self.last_animation = get_time()



    def update(self, *args) -> None:
        """
        Atualiza posição da bala
        """
        
        if self.can_deactivate():
            self.deactivate()
        if self.is_activated:
            if get_time() - self.last_animation >= self.animation_time:
                self.last_animation = get_time()
                self.current_frame += 1
                
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
                                 [round(offset*scaler), round(2*offset*scaler)], angle, PINK)
           
        