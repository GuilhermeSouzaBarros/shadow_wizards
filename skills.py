from abc import ABC, abstractmethod
from pyray import *
from raylib import *
from shapes import *
from imaginary import Imaginary
from vectors import Vector2, Domain
from lines import *

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


    def update(self, *args) -> None:
        current_time = get_time()
        if (is_key_pressed(KEY_E) and 
            current_time - self.last_activation > self._cooldown):
            self.activate(*args)
        if current_time - self.last_activation > self.duration:
            self.deactivate() 

    def draw(self, *args) -> None:
        pass
            

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
        self._cooldown = 0.5
        self.speed_multiplier = 1
        self.hitboxes = [Projectile(pos, self.tile_size, self.duration, self._cooldown, 
                        self.speed_multiplier) 
                        for _ in range(self.number_of_bullets)]

    def activate(self, player_pos:Vector2, angle:Imaginary) -> None:
        """
        Se houver balas disponiveis e o tempo de ativação ser cumprido,
        percorre o vetor de balas até achar uma disponivel e atira
        """
        if (self.number_of_activated < self.number_of_bullets):
            for bullet in self.hitboxes:
                if not bullet.is_activated and self.can_activate:
                    bullet.activate(player_pos, angle)
                    self.number_of_activated += 1
                    self.last_activation = get_time()
                    break

    def update(self, player_pos, angle:Imaginary, *args) -> None:
        """
        Atualiza estado bas balas e desativa ou ativa dependendo do evento
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        if is_key_pressed(KEY_E) and self.can_activate():
            self.activate(player_pos, angle)

    def apply_effect(self, projectile) -> None:
        projectile.deactivate()
        projectile.is_activated = False
        self.number_of_activated -= 1

    def draw(self, *args) -> None:
        """
        Desenha todas as balas ativas
        """
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.draw(PINK, *args)

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


    def update(self, player_pos:Vector2, angle:Imaginary, args) -> None:
        for bullet in self.hitboxes:
            if bullet.is_activated:
                bullet.update()
                if not bullet.is_activated:
                    self.number_of_activated -= 1
        if(is_key_pressed(KEY_E)) and self.can_activate():
            self.activate(player_pos, angle)

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
                bullet.draw(RED, *args)

class Trap(Skill):
    def __init__(self, pos:Vector2, tile_size:Vector2, duration:float, cooldown:float) -> None:
        super().__init__()
        self._cooldown = cooldown
        self.hitbox = Rectangle(pos, tile_size)
        self.duration = duration
        self.tile_size = tile_size

    def activate(self, player_pos = None, angle = None) -> None:
        """
        Ativa armadilha de acordo com a posição do player
        """
        current_time = get_time()
        if(current_time - self.last_activation > self._cooldown):
            self.hitbox.position = player_pos
            self.last_activation = get_time()
            self.is_activated = True
    
    
    def update(self) -> None:
        current_time = get_time()

        if current_time - self.last_activation > self.duration:
            self.deactivate()
    
    def draw(self, *args) -> None:
        """
        Desenha armadilha se ativa
        """
        if self.is_activated:
            self.hitbox.draw(YELLOW, *args)

class Traps(Skill):
    def __init__(self, pos:Vector2) -> None:
        """
        Herda classe Skill, define o número de armadilhas que 
        o personagem pode colocar, define tempo até ativar a armadilha. 
        Cria lista de objeto Trap para lidar com cada armadilha separadamente
        """
        super().__init__()
        self.number_of_traps = 5
        self.number_of_activated = 0
        self.time_to_activate = 1
        self._cooldown = 1
        self.tile_size = Vector2(32, 32)
        self.duration = 5
        self.hitboxes = [Trap(pos, self.tile_size, self.duration, self._cooldown) 
                      for _ in range(self.number_of_traps)]

    def activate(self, player_pos:Vector2) -> None:
        """
        Se houver armadilhas disponíveis, coloca uma na posição 
        que o player está
        """
        current_time = get_time()
        if (self.number_of_activated < self.number_of_traps and 
            current_time - self.last_activation > self._cooldown):
            for trap in self.hitboxes:
                if not trap.is_activated:
                    trap.activate(player_pos)
                    self.number_of_activated += 1
                    self.last_activation = current_time
                    break

    def apply_effect(self, projectile) -> None:
        projectile.deactivate()
        projectile.is_activated = False
        self.number_of_activated -= 1


    def update(self, player_pos:Vector2, angle:Imaginary, *args) -> None:
        current_time = get_time()
        for trap in self.hitboxes:
            if trap.is_activated:
                trap.update()
                if current_time - trap.last_activation > trap.duration:
                    self.number_of_activated -= 1

        if is_key_pressed(KEY_E):
            self.activate(player_pos)
                    

    def draw(self, *args) -> None:
        """
        Desenha armadilhas
        """
        for trap in self.hitboxes:
            if trap.is_activated:
                trap.draw(*args)

class Intangibility(Skill):
    def __init__(self) -> None:
        super().__init__()
        self._cooldown = 5
        self.duration = 3
        self.in_wall = False


    def update(self, player_pos:Vector2, angle:Imaginary, *args) -> None:
        if is_key_pressed(KEY_E):
            self.activate()

        current_time = get_time()
        if current_time - self.last_activation > self.duration:
            self.deactivate()


    def draw(self, *args) -> None:
        pass

class Laser(Skill):
    def __init__(self, player_pos:Vector2) -> None:
        """
        Habilidade de raios
        """
        super().__init__()
        self._cooldown = 2
        self.duration = 3
        self.laser_size = Vector2(10, 10)
        self.max_size = Vector2(1000, 10)
        self.current_size = self.laser_size.copy()
        self.laser_size_cp = self.laser_size.copy()
        self.reflections = 4
        self.hitboxes = [Line(Vector2(0, 0), player_pos.copy(), Domain(0, float('inf')))]
        
    def deactivate(self) -> None:
        super().deactivate()
        self.hitboxes = [Line(Vector2(0, 0), Vector2(0, 0), Domain(0, float('inf')))]
  
    def map_collision(self, laser:Line, map) -> ColLines:
        """
        Procura colisão do laser no mapa e retorna a colisão mais próxima
        """
        collisions = []
        for row in map.tiles:
            for tile in row:
                if not tile.type:
                    continue
                if (tile.is_destructible and not tile.is_destroyed) or tile.has_collision:
                    col = tile.hitbox.collision_line(laser)
                    if col != "NULL" and col['col'].t_line_1 > 0:
                        collisions.append(col)

        closest_col = min(collisions, key=lambda obj: obj['col'].t_line_1)
        return closest_col

    def update(self, player_pos:Vector2, angle:Imaginary, map) -> None:
        if is_key_pressed(KEY_E):
            self.activate()
        if self.can_deactivate():
            self.deactivate()
        if self.is_activated:
            self.hitboxes = []
            self.hitboxes.append(Line(Vector2(angle.real, angle.imaginary), player_pos.copy(), Domain(0, float('inf'))))
            for i in range(0, self.reflections):
                closest_col = self.map_collision(self.hitboxes[i], map)
                collision_point = closest_col['col'].point
                
                dir = collision_point - self.hitboxes[i].point
                
                self.hitboxes[i] = Line(dir, self.hitboxes[i].point, Domain(0, 1))
                
                new_direction = self.hitboxes[i].reflection_angle(closest_col['rectangle_line'])
                new_direction = Vector2(new_direction.real, new_direction.imaginary)
                if i == self.reflections - 1:
                    continue
                self.hitboxes.append(Line(new_direction, closest_col['col'].point, Domain(0, float('inf'))))
        
    def apply_effect(self, projectile) -> None:
        pass

    def draw(self, *args) -> None:
        if self.is_activated:
            for hitbox in self.hitboxes:
                hitbox.draw(*args, PURPLE)

class SuperSpeed(Skill):
    def __init__(self) -> None:
        super().__init__()
        self.speed_multiplier = 6.0
        self.is_activated = True

    def update(self, *args) -> None:
        pass

    def draw(self, *args) -> None:
        pass



class Shield(Skill):
    def __init__(self):
        super().__init__()
        self._cooldown = 1
        self.duration = 2

    def update(self, player_pos:Vector2, angle:Imaginary, *args) -> None:
        if is_key_pressed(KEY_E):
            self.activate()
        if self.can_deactivate():
            self.deactivate()

    def draw(self, *args) -> None:
        pass
