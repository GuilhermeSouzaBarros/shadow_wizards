from skills.skill import *

class Trap(Skill):
    def __init__(self, pos:Vector2, tile_size:Vector2, duration:float, cooldown:float) -> None:
        super().__init__()
        self._cooldown = cooldown
        self.hitbox = Rec(pos, tile_size)
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