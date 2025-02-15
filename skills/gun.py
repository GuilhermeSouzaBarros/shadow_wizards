from skills.skill import *
from skills.projectile import Projectile

class Gun(Skill):
    def __init__(self, pos:Vector2) -> None:
        """
        Herda classe Skill e adiciona os atributos numero de balas e quantidade
        de balas ativadas, além de uma lista de objeto balas
        """
        super().__init__()
        self.tile_size = 10
        self.number_of_bullets = 3
        self.number_of_activated = 0
        self.duration = 2
        self._cooldown = 1
        self.speed_multiplier = 1
        self.sprite = load_texture("sprites/bullet.png")
        self.sound = load_sound("sounds/gun-shot.mp3")
        set_sound_volume(self.sound, 0.3)
        self.hitboxes = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def encode(self) -> bytes:
        message = self.number_of_activated.to_bytes(1)
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
        """
        Se houver balas disponiveis e o tempo de ativação ser cumprido,
        percorre o vetor de balas até achar uma disponivel e atira
        """
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.hitboxes:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    play_sound(self.sound)
                    self.number_of_activated += 1
                    self.last_activation = get_time()
                    break

    def deactivate(self) -> None:
        self.is_activated = False
        for bullet in self.hitboxes:
            bullet.deactivate()

    def update(self, player_pos, angle:Imaginary, player_input:dict, *args) -> None:
        """
        Atualiza estado bas balas e desativa ou ativa dependendo do evento
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        activate = self.skill_key(player_pos, angle, 1, player_input)


    def draw(self, *args) -> None:
        """
        Desenha todas as balas ativas
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.draw(RED, *args, self.sprite, 1)