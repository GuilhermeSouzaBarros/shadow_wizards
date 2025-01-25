from skills.skill import *

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

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        """
        Ativa bala de acordo com a posição do player e sua direção
        """
        super().activate()
        self.angle = angle
        self.hitbox.position = player_pos



    def update(self, *args) -> None:
        """
        Atualiza posição da bala
        """
        
        if self.can_deactivate():
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
            self.hitbox.draw(*args)
        