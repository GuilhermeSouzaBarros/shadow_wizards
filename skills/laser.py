from skills.skill import *

class Laser(Skill):
    def __init__(self, player_pos:Vector2) -> None:
        """
        Habilidade de raios
        """
        super().__init__()
        self._cooldown = 10
        self.duration = 1
        self.laser_size = Vector2(10, 10)
        self.max_size = Vector2(1000, 10)
        self.current_size = self.laser_size.copy()
        self.laser_size_cp = self.laser_size.copy()
        self.reflections = 4
        self.sound = load_sound("sounds/laser.mp3")
        set_sound_volume(self.sound, 0.5)
        self.hitboxes = [Line(Vector2(0, 0), player_pos.copy(), Domain(0, float('inf')))]
    
    def encode(self) -> bytes:
        message = self.is_activated.to_bytes(1) + len(self.hitboxes).to_bytes(1)
        for line in self.hitboxes:
            message += pack("dddddd", line.direction.x, line.direction.y, line.point.x, line.point.y, line.limit_t.a, line.limit_t.b)
        print(self.hitboxes[0].__str__)  
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        self.is_activated = bytes_string[0]
        self.hitboxes = []
        lines = bytes_string[1]
        pointer = 2
        while pointer < lines * 48:
            data = unpack("dddddd", bytes_string[pointer:pointer+48])
            self.hitboxes.append(Line(Vector2(data[0], data[1]), Vector2(data[2], data[3]), Domain(data[4], data[5])))
            pointer += 48   
        print(self.hitboxes[0].__str__)         
        return pointer
    
    def deactivate(self) -> None:
        super().deactivate()
        self.hitboxes = [Line(Vector2(0, 0), Vector2(0, 0), Domain(0, float('inf')))]
        stop_sound(self.sound)
  
    def map_collision(self, laser:Line, map) -> ColLines:
        """
        Procura colisão do laser no mapa e retorna a colisão mais próxima
        """
        collisions = []

        for tile in map.collision_hitboxes:
            col = tile.collision_line(laser)
            if col and col['col'].t_line_1:
                collisions.append(col)

        if collisions:
            closest_col = min(collisions, key=lambda obj: obj['col'].t_line_1)
            return closest_col
        
        return False

    def define_laser(self, player_pos:Vector2, angle:Imaginary, map) -> bool:
        """
        Define direção do laser e suas reflexões
        """
        self.hitboxes = []
        self.hitboxes.append(Line(Vector2(angle.real, angle.imaginary), player_pos.copy(), Domain(0, float('inf'))))
        for i in range(0, self.reflections):
            closest_col = self.map_collision(self.hitboxes[i], map)

            if closest_col == False:
                return False
            
            collision_point = closest_col['col'].point
            
            dir = collision_point - self.hitboxes[i].point
            
            self.hitboxes[i] = Line(dir, self.hitboxes[i].point, Domain(0, 1))
            
            new_direction = self.hitboxes[i].reflection_angle(closest_col['rectangle_line'])
            new_direction = Vector2(new_direction.real, new_direction.imaginary)
            if i == self.reflections - 1:
                continue
            self.hitboxes.append(Line(new_direction, closest_col['col'].point, Domain(0, float('inf'))))
        return True

    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, map) -> None:
        if self.skill_key(player_pos, angle, 0, player_input):
            activate = self.define_laser(player_pos, angle, map)
            if activate:
                self.activate()
                play_sound(self.sound)
            
        if self.can_deactivate():
            self.deactivate()
            
    def apply_effect(self, projectile) -> None:
        pass

    def draw(self, *args) -> None:
        if self.is_activated:
            for hitbox in self.hitboxes:
                hitbox.draw(*args, PURPLE)