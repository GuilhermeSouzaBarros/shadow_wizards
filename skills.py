from abc import ABC, abstractmethod
from pyray import *
from raylib import *
from shapes import Circle
from imaginary import Imaginary

class Skill(ABC):
    def __init__(self) -> None:
        """
        Atributos essenciais para todas as habilidades
        """
        self.last_activation = 0
        self.is_activated = False
        self.skill_duration = None
        self.cooldown = 3
        

    @abstractmethod
    def activate(self, player_pos:Vector2 = None, angle:Imaginary = None):
        """
        Função abstrata usada para ativar  habilidades
        """
        pass

    def deactivate(self):
        if self.skill_duration is not None:
            if get_time() - self.last_activation >= self.skill_duration:
                self.is_activated = False

    @abstractmethod
    def draw(self, map_offset=None, scaler=None):
        """
        Função abstrata que desenha a habilidade correspondente
        """
        pass

    

class Dash(Skill):
    def __init__(self) -> None:
        """
        Herda Skill. Atributo speed_multiplicator é usado para dar um impuslo
        no player caso a skill dash seja usada
        """
        super().__init__()
        self.speed_multiplier = 20.0
        self.cooldown = 1
        self.skill_duration = 0.1
        
        
    def activate(self, player_pos:Vector2):
        """
        Impulsiona personagem
        """
        if (get_time() - self.last_activation > self.cooldown 
            and not self.is_activated):
            self.last_activation = get_time()
            self.is_activated = True


    def update(self, pos, angle):
        current_time = get_time()
        if (is_key_pressed(KEY_E) and 
            current_time - self.last_activation > self.cooldown):
            self.activate(pos)
        if current_time - self.last_activation > self.skill_duration:
            self.deactivate() 

    def draw(self, map_scaler, scaler):
        pass
            

class Projectile(Skill):
    def __init__(self, pos:Vector2, tile_size:float, duration:float, cooldown:float, 
                 speed: float):
        """
        Herda classe Skill
        """
        super().__init__()
        self.tile_size = tile_size
        self.speed_multiplier = speed
        self.hitbox = Circle(pos, tile_size*0.4)
        self.skill_duration = duration
        self.cooldown = cooldown
        self.angle = Imaginary(1, 0)

    def activate(self, player_pos:Vector2, angle:Imaginary):
        """
        Ativa bala de acordo com a posição do player e sua direção
        """
        current_time = get_time()

        if(current_time - self.last_activation > self.cooldown):
            self.angle = angle
            self.hitbox.position = player_pos
            self.last_activation = get_time()
            self.is_activated = True

    def deactivate(self):
        self.is_activated = False

    def update(self):
        """
        Atualiza posição da bala
        """
        current_time = get_time()
        if current_time - self.last_activation > self.skill_duration:
            self.deactivate()
        else:
            speed = self.tile_size*self.speed_multiplier

            delta_time = current_time - self.last_activation

            self.hitbox.position.x += speed * self.angle.real * delta_time
            self.hitbox.position.y += speed * self.angle.imaginary * delta_time

    def draw(self, map_offset:Vector2, scaler:float, color):
        """
        Desenha bala se ativa
        """
        if self.is_activated:
            self.hitbox.draw(map_offset, scaler, color)
        


class Gun(Skill):
    def __init__(self, pos:Vector2):
        """
        Herda classe Skill e adiciona os atributos numero de balas e quantidade
        de balas ativadas, além de uma lista de objeto balas
        """
        super().__init__()
        self.tile_size = 10
        self.number_of_bullets = 3
        self.bullets_activated = 0
        self.skill_duration = 2
        self.cooldown = 2
        self.speed_multiplier = 1
        self.bullets = [Projectile(pos, self.tile_size, self.skill_duration, self.cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def activate(self, player_pos:Vector2, angle:Imaginary):
        """
        Se houver balas disponiveis e o tempo de ativação ser cumprido,
        percorre o vetor de balas até achar uma disponivel e atira
        """
        if (self.bullets_activated < self.number_of_bullets and
            get_time() - self.last_activation > self.cooldown):
            for bullet in self.bullets:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    self.bullets_activated += 1
                    break

    def deactivate(self):
        self.bullets_activated -= 1

    def update(self, player_pos, angle:Imaginary):
        for bullet in self.bullets:
            if bullet.is_activated:
                bullet.update()
                current_time = get_time()
                if current_time - bullet.last_activation > bullet.skill_duration:
                    self.deactivate()
        if is_key_pressed(KEY_E):
            self.activate(player_pos, angle)

    def draw(self, map_offset, scaler):
        """
        Desenha todas as balas ativas
        """
        for bullet in self.bullets:
            if bullet.is_activated:
                bullet.draw(map_offset, scaler, PINK)

class Fireball(Skill):
    def __init__(self, pos:Vector2):
        """
        Herda classe skill. Inicia o tamanho do projétil e 
        inicia um objeto projétil
        """
        super().__init__()
        self.tile_size = 20
        self.angle = Imaginary(1, 0)
        self.skill_duration = 2
        self.cooldown = 3
        self.speed_multiplier = 0.5
        self.projectile = Projectile(pos, self.tile_size, self.skill_duration, 
                                     self.cooldown, self.speed_multiplier)

    def activate(self, player_pos:Vector2):
        current_time = get_time()
        if(not self.is_activated and current_time - self.last_activation 
           > self.cooldown):
            self.projectile.activate(player_pos, self.angle)
            self.last_activation = get_time()
            self.is_activated = True
            
    def deactivate(self):
        self.is_activated = False
        self.projectile.deactivate()

    def update(self, player_pos:Vector2, angle:Imaginary):
        if(is_key_pressed(KEY_E)):
            self.activate(player_pos)
            self.angle = angle
        if get_time() - self.last_activation > self.skill_duration:
            self.deactivate()
        if self.projectile.is_activated:
            self.projectile.update()
            

    def draw(self, map_offset, scaler):
        """
        Se ativa, desenha bola de fogo
        """
        if self.is_activated:
            self.projectile.draw(map_offset, scaler, RED)

class Trap(Skill):
    def __init__(self):
        """
        Herda classe Skill, define o número de armadilhas que 
        o personagem pode colocar, define tempo até ativar a armadilha
        """
        super().__init__()
        self.number_of_traps = 3
        self.traps_activated = 0
        self.time_to_activate = 1
        self.cooldown = 1
        self.traps_pos = []

    def activate(self, player_pos:Vector2):
        """
        Se houver armadilhas disponíveis, coloca uma na posição 
        que o player está
        """
        current_time = get_time()
        if (self.traps_activated < self.number_of_traps and 
            current_time - self.last_activation > self.cooldown):
            self.traps_activated += 1
            self.traps_pos.append(player_pos)



    def draw(self):
        """
        Desenha armadilhas
        """
        pass

class SuperSpeed(Skill):
    def __init__(self):
        super().__init__()
        self.speed_multiplicator = 7.0

    def activate(self):
        pass



    def draw(self):
        pass



class Parry(Skill):
    def __init__(self):
        super().__init__()
        self.cooldown = 1

    def activate(self):
        if(not self.is_activated and 
           get_time() - self.last_activation > self.cooldown):
            self.is_activated = True
            self.last_activation = get_time()



    def draw(self):
        pass

