from skills.skill import *
from skills.projectile import Projectile

class Fireball(Skill):
    def __init__(self, pos:Vector2) -> None:
        """
        Herda classe skill. Inicia o tamanho do projétil e 
        inicia um objeto projétil self.projectiles
        """
        super().__init__()
        self.tile_size = 20
        self.duration = 2
        self._cooldown = 3
        self.number_of_bullets = 1
        self.number_of_activated = 0
        self.speed_multiplier = 0.5
        self.sprite = load_texture("sprites/fireball.png")
        self.sound = load_sound("sounds/fireball.mp3")
        set_sound_volume(self.sound, 0.5)
        self.hitboxes = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def encode(self) -> bytes:
        actives = 0
        for projectile in self.hitboxes:
            actives += projectile.is_activated
        
        message = actives.to_bytes(1)
        for projectile in self.hitboxes:
            if projectile.is_activated:
                message += projectile.encode()
        return message

    def decode(self, byte_string:bytes) -> int:
        i = int(byte_string[0])
        pointer_offset = 1
        for projectile in self.hitboxes:
            pointer_offset += projectile.decode(byte_string[pointer_offset:], i > 0)
            i -= 1

        return pointer_offset

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.hitboxes:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    play_sound(self.sound)
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


    def draw(self, *args) -> None:
        """
        Se ativa, desenha bola de fogo
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.draw(RED, *args, self.sprite, 1)