from skills.skill import *
from skills.projectile import Projectile

class Fireball(Skill):
    def __init__(self, pos:Vector2) -> None:
        """
        Herda classe skill. Inicia o tamanho do projétil e 
        inicia um objeto projétilself.projectiles
        """
        super().__init__()
        self.tile_size = 20
        self.duration = 2
        self._cooldown = 3
        self.number_of_bullets = 1
        self.number_of_activated = 0
        self.speed_multiplier = 0.5
        self.sprite = load_texture("sprites/fireball.png")
        self.hitboxes = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.hitboxes:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    self.number_of_activated += 1
                    self.last_activation = get_time()
                    break


    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, *args) -> None:
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        activate = self.skill_key(player_pos, angle, 1, player_input)

    def apply_effect(self, projectile) -> None:
        projectile.deactivate()
        projectile.is_activated = False
        self.number_of_activated -= 1

    def draw(self, *args) -> None:
        """
        Se ativa, desenha bola de fogo
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.draw(RED, *args, self.sprite, 1)