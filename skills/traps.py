from skills.skill import *

class Trap():
    def __init__(self, pos:Vector2, tile_size:Vector2, duration:float, cooldown:float) -> None:
        self.is_activated = False
        self._cooldown = cooldown
        self.hitbox = Rec(pos, tile_size)
        self.duration = duration
        self.tile_size = tile_size
        self.current_frame = 0
        self.last_animation = 0
        self.last_activation = 0

    def encode(self) -> bytes:
        return self.is_activated.to_bytes(1) + pack("dd", self.hitbox.position.x, self.hitbox.position.y)
    
    def decode(self, bytes_string:bytes) -> int:
        data = unpack("dd", bytes_string[1:17])
        self.is_activated = bytes_string[0]
        self.hitbox.position = Vector2(data[0], data[1])
        return 17
    
    def activate(self, player_pos = None, angle = None) -> None:
        """
        Ativa armadilha de acordo com a posição do player
        """
        current_time = get_time()
        if(current_time - self.last_activation > self._cooldown):
            self.hitbox.position = player_pos
            self.last_activation = get_time()
            self.is_activated = True
            self.current_frame = 0
            self.last_animation = current_time

    def deactivate(self):
        self.is_activated = False

    def update_time(self):
        if self.is_activated and (get_time() - self.last_animation > 1):
            self.last_animation = get_time()
            self.current_frame += 1

    def update(self) -> None:
        if get_time() - self.last_activation > self.duration:
            self.deactivate()
    
    def draw(self, *args) -> None:
        """
        Desenha armadilha se ativa
        """
        if self.is_activated:
            sprite = args[-1]
            scaler = args[1]
            size_im_x = Imaginary(self.hitbox.size.x/2, 0.0)
            size_im_y = Imaginary(0.0, self.hitbox.size.y/2.0)
            up_left_corner = [self.hitbox.position.x - size_im_x.real - size_im_y.real,
                              self.hitbox.position.y - size_im_x.imaginary - size_im_y.imaginary]
            offset = Vector2(self.hitbox.size.x*0.5, self.hitbox.size.y*0.5)
            pos = [args[0].x + ((up_left_corner[0] + 16)*scaler), 
                   args[0].y + ((up_left_corner[1] + 32)*scaler)]
            rectangle_dest = [round(pos[0]), round(pos[1]),
                            round(scaler*self.hitbox.size.x),
                            round(scaler*self.hitbox.size.y)]
            draw_texture_pro(sprite, [self.current_frame*32, 0, 32, 32], rectangle_dest, 
                             [round(offset.x*scaler), round(2*offset.y*scaler)], 0, WHITE)
     

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
        self.sprite = load_texture("sprites/mine.png")
        self.sound = load_sound("sounds/explosion.mp3")
        set_sound_volume(self.sound, 0.3)
        self.duration = 5
        self.hitboxes = [Trap(pos, self.tile_size, self.duration, self._cooldown) 
                      for _ in range(self.number_of_traps)]

    def encode(self) -> bytes:
        message = "".encode()
        for trap in self.hitboxes:
            message += trap.encode()
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        pointer = 0
        for trap in self.hitboxes:
            pointer += trap.decode(bytes_string[pointer:])
        
        return pointer
    
    def activate(self, player_pos:Vector2, *args) -> None:
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


    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, *args) -> None:
        current_time = get_time()
        for trap in self.hitboxes:
            if trap.is_activated:
                trap.update()
                if current_time - trap.last_activation > trap.duration:
                    self.number_of_activated -= 1

        activate = self.skill_key(player_pos, angle, 1, player_input)
                    

    def draw(self, *args) -> None:
        """
        Desenha armadilhas
        """
        for trap in self.hitboxes:
            if trap.is_activated:
                trap.draw(*args, self.sprite)
