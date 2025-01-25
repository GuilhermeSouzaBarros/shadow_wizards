from skills.skill import *

class Laser(Skill):
    def __init__(self, player_pos:Vector2) -> None:
        """
        Habilidade de raios
        """
        super().__init__()
        self._cooldown = 1
        self.duration = 1
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

        for tile in map.collision_hitboxes:
            col = tile.collision_line(laser)
            if col != "NULL" and col['col'].t_line_1 != 0:
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

    def update(self, player_pos:Vector2, angle:Imaginary, map) -> None:
        if is_key_pressed(KEY_E):
            activate = self.define_laser(player_pos, angle, map)
            if activate:
                self.activate()
            
        if self.can_deactivate():
            self.deactivate()
            
    def apply_effect(self, projectile) -> None:
        pass

    def draw(self, *args) -> None:
        if self.is_activated:
            for hitbox in self.hitboxes:
                hitbox.draw(*args, PURPLE)