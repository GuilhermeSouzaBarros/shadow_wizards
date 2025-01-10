from abc import ABC, abstractmethod
from pyray import *
from raylib import *
from shapes import *
from imaginary import Imaginary

class Skill(ABC):
    def __init__(self) -> None:
        """
        Atributos essenciais para todas as habilidades
        """
        self.last_activation = 0
        self.is_activated = False
        self.duration = None
        self._cooldown = 0.3
        

    def can_activate(self) -> bool:
        return get_time() - self.last_activation > self._cooldown

    def activate(self, *args) -> None:
        if self.can_activate():
            self.last_activation = get_time()
            self.is_activated = True

    def can_deactivate(self) -> bool:
        if self.duration is None:
            return False
        return get_time() - self.last_activation > self.duration

    def deactivate(self) -> None:
        self.is_activated = False


    @abstractmethod
    def update(self, *args) -> None:
        """
        Atualiza estado da habilidade de acordo 
        com suas características
        """
        pass

    @abstractmethod
    def draw(self, *args) -> None:
        """
        Desenha a habilidade correspondente
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
        self._cooldown = 1
        self.duration = 0.1


    def update(self, *args):
        current_time = get_time()
        if (is_key_pressed(KEY_E) and 
            current_time - self.last_activation > self._cooldown):
            self.activate(*args)
        if current_time - self.last_activation > self.duration:
            self.deactivate() 

    def draw(self, *args):
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
        self.duration = duration
        self._cooldown = cooldown
        self.angle = Imaginary(1, -1)

    def activate(self, player_pos:Vector2, angle:Imaginary):
        """
        Ativa bala de acordo com a posição do player e sua direção
        """
        super().activate()
        self.angle = angle
        self.hitbox.position = player_pos



    def update(self, *args):
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

    def draw(self, *args):
        """
        Desenha bala se ativa
        """
        if self.is_activated:
            self.hitbox.draw(*args)
        


class Gun(Skill):
    def __init__(self, pos:Vector2):
        """
        Herda classe Skill e adiciona os atributos numero de balas e quantidade
        de balas ativadas, além de uma lista de objeto balas
        """
        super().__init__()
        self.tile_size = 10
        self.number_of_bullets = 3
        self.number_of_activated = 0
        self.duration = 2
        self._cooldown = 0.001
        self.speed_multiplier = 1
        self.projectiles = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def activate(self, player_pos:Vector2, angle:Imaginary):
        """
        Se houver balas disponiveis e o tempo de ativação ser cumprido,
        percorre o vetor de balas até achar uma disponivel e atira
        """
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.projectiles:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    self.number_of_activated += 1
                    self.last_activation = get_time()
                    break

    def update(self, player_pos, angle:Imaginary):
        """
        Atualiza estado bas balas e desativa ou ativa dependendo do evento
        """
        for bullet in self.projectiles:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        if is_key_pressed(KEY_E) and self.can_activate():
            self.activate(player_pos, angle)

    def draw(self, *args):
        """
        Desenha todas as balas ativas
        """
        for bullet in self.projectiles:
            if bullet.is_activated:
                bullet.draw(*args, PINK)

class Fireball(Skill):
    def __init__(self, pos:Vector2):
        """
        Herda classe skill. Inicia o tamanho do projétil e 
        inicia um objeto projétil
        """
        super().__init__()
        self.tile_size = 20
        self.duration = 2
        self._cooldown = 3
        self.number_of_bullets = 1
        self.number_of_activated = 0
        self.speed_multiplier = 0.5
        self.projectiles = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def activate(self, player_pos:Vector2, angle:Imaginary):
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.projectiles:
                if not bullet.is_activated:
                    bullet.activate(player_pos, angle)
                    self.number_of_activated += 1
                    self.last_activation = get_time()
                    break


    def update(self, player_pos:Vector2, angle:Imaginary):
        for bullet in self.projectiles:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        if(is_key_pressed(KEY_E)) and self.can_activate():
            self.activate(player_pos, angle)

    def draw(self, *args):
        """
        Se ativa, desenha bola de fogo
        """
        for bullet in self.projectiles:
            if bullet.is_activated:
                bullet.draw(*args, RED)

class Trap(Skill):
    def __init__(self, pos:Vector2, tile_size:Vector2, duration:float, cooldown:float):
        super().__init__()
        self._cooldown = cooldown
        self.hitbox = Rectangle(pos, tile_size)
        self.duration = duration
        self.tile_size = tile_size

    def activate(self, player_pos = None, angle = None):
        """
        Ativa armadilha de acordo com a posição do player
        """
        current_time = get_time()
        if(current_time - self.last_activation > self._cooldown):
            self.hitbox.position = player_pos
            self.last_activation = get_time()
            self.is_activated = True
    
    
    def update(self):
        current_time = get_time()

        if current_time - self.last_activation > self.duration:
            self.deactivate()
    
    def draw(self, *args):
        """
        Desenha armadilha se ativa
        """
        if self.is_activated:
            self.hitbox.draw(*args, YELLOW)

class Traps(Skill):
    def __init__(self, pos:Vector2):
        """
        Herda classe Skill, define o número de armadilhas que 
        o personagem pode colocar, define tempo até ativar a armadilha. 
        Cria lista de objeto Trap para lidar com cada armadilha separadamente
        """
        super().__init__()
        self.number_of_traps = 5
        self.traps_activated = 0
        self.time_to_activate = 1
        self._cooldown = 1
        self.tile_size = Vector2(32, 32)
        self.duration = 5
        self.traps = [Trap(pos, self.tile_size, self.duration, self._cooldown) 
                      for _ in range(self.number_of_traps)]

    def activate(self, player_pos:Vector2):
        """
        Se houver armadilhas disponíveis, coloca uma na posição 
        que o player está
        """
        current_time = get_time()
        if (self.traps_activated < self.number_of_traps and 
            current_time - self.last_activation > self._cooldown):
            for trap in self.traps:
                if not trap.is_activated:
                    trap.activate(player_pos)
                    self.traps_activated += 1
                    self.last_activation = current_time
                    break


    def update(self, player_pos:Vector2, angle:Imaginary):
        current_time = get_time()
        for trap in self.traps:
            if trap.is_activated:
                trap.update()
                if current_time - trap.last_activation > trap.duration:
                    self.traps_activated -= 1

        if is_key_pressed(KEY_E):
            self.activate(player_pos)
                    

    def draw(self, *args):
        """
        Desenha armadilhas
        """
        for trap in self.traps:
            if trap.is_activated:
                trap.draw(*args)

class Intangibility(Skill):
    def __init__(self):
        super().__init__()
        self._cooldown = 5
        self.duration = 3
        self.in_wall = False


    def update(self, player_pos:Vector2, angle:Imaginary):
        if is_key_pressed(KEY_E):
            self.activate()

        current_time = get_time()
        if current_time - self.last_activation > self.duration:
            self.deactivate()


    def draw(self, *args):
        pass

class Laser(Skill):
    def __init__(self, player_pos:Vector2):
        """
        Habilidade de raios
        """
        super().__init__()
        self._cooldown = 1
        self.duration = 3
        self.speed = Vector2(3, 4)
        self.laser_size = Vector2(10, 10)
        self.laser_size_cp = self.laser_size.copy()
        self.hitbox = Rectangle(Vector2(player_pos.x + self.laser_size_cp.x/2, player_pos.y - self.laser_size_cp.y/2), 
                                self.laser_size_cp)
        
    def deactivate(self):
        super().deactivate()
        self.hitbox.size.x = self.laser_size.x
        self.hitbox.size.y = self.laser_size.y

    def can_grow(self):
        pass
        

    def update(self, player_pos:Vector2, angle:Imaginary):
        if is_key_pressed(KEY_E):
            self.activate()
        if self.can_deactivate():
            self.deactivate()
        if self.is_activated:
            player_pos = player_pos.copy()
            self.hitbox.angle = angle.copy()
            size_im_x = Imaginary(self.hitbox.size.x / 2.0, 0.0) * self.hitbox.angle
            player_pos.x += size_im_x.real
            player_pos.y += size_im_x.imaginary

            if self.hitbox.size.x < 1000:
                self.hitbox.size.x += 5
            if self.hitbox.size.y < 10:
                self.hitbox.size.y += 1
            self.hitbox.position = player_pos

    def draw(self, *args):
        if self.is_activated:
            self.hitbox.draw(*args, WHITE)

class SuperSpeed(Skill):
    def __init__(self):
        super().__init__()
        self.speed_multiplier = 6.0
        self.is_activated = True

    def update(self, *args):
        pass

    def draw(self, *args):
        pass



class Shield(Skill):
    def __init__(self):
        super().__init__()
        self._cooldown = 1
        self.duration = 2

    def update(self, player_pos:Vector2, angle:Imaginary):
        if is_key_pressed(KEY_E):
            self.activate()
        if self.can_deactivate():
            self.deactivate()

    def draw(self, *args):
        pass
