from pyray import *
from raylib import *

from vectors import Vector2
from collisions import CollisionInfo
from gamemodes.obj import Objective
from time import time

class Domination(Objective):
    def __init__(self, tile_size:int, row:int, column:int, radius:float):
        super().__init__(tile_size, row, column, radius, 2)
        self.curr_team = 0        
        self.last_increment:float = 0.0

    def encode(self) -> bytes:
        message = self.curr_team.to_bytes(1)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        self.curr_team = bytes_string[0]
        return 1

    def update_region(self) -> None:
        super().update_region()

    def check_domination(self, players:list) -> int:
        """
        Retorno: 
            0, quando nenhum time estiver dominando a área;
            1, quando o time 1 estiver dominando a área;
            2, quando o time 2 estiver dominando a área.
        """
        teams_inside = []
        for player in players:
            if not player.is_alive:
                continue
            info = CollisionInfo.collision(player.hitbox, self.hitbox)            
            if info.intersection:
                if not (player.team in teams_inside):
                    teams_inside.append(player.team)

        if len(teams_inside) == 1:
            return teams_inside[0]
        return 0
    
    def update(self, players:list, delta_time:float) -> list:
        self.update_region()
        self.curr_team = self.check_domination(players)        

        pts_increase = [0,0]
        if self.curr_team:
            now = time()
            if now - self.last_increment >= 1.0:
                pts_increase[self.curr_team-1] = self.pts_gain
                self.last_increment = now
        return pts_increase

    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool) -> None:
        # Desenha a região de dominação de acordo com o time que está dominando a área

        if self.curr_team == 1:
            # Desenha a área de dominação quando o time 1 está dominando
            color = RED
            
        elif self.curr_team == 2:
            # Desenha a área de dominação quando o time 2 está dominando
            color = BLUE
        else:
            # Desenha a área de dominação quando nenhum time está dominando
            color = WHITE

        pos = [map_offset.x + (self.hitbox.position.x * scaler), map_offset.y + (self.hitbox.position.y * scaler)]
        draw_circle_lines_v(pos, self.hitbox.radius * scaler, color)    

    def unload(self):
        pass