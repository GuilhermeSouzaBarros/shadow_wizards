from pyray import *
from raylib import *

from vectors import Vector2
from collisions import ColCircleCircle
from gamemodes.obj import Objective
from time import time

class Domination(Objective):
    def __init__(self, tile_size:int, row:int, column:int, radius:float):
        super().__init__(tile_size, row, column, radius, 1)
        self.curr_team = 0        
        self.last_increment:float = 0.0

    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região de dominação.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        super().update_region()

    def check_domination(self, players:list) -> int:
        """
        Função: check_domination
        Descrição:
            Verifica se a área de dominação está sendo dominada por algum time.
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno: 
            0, quando nenhum time estiver dominando a área;
            1, quando o time 1 estiver dominando a área;
            2, quando o time 2 estiver dominando a área.
        """
        teams_inside = []
        collision_check = ColCircleCircle()
        for player in players:
            if not player.is_alive:
                continue
            collision = collision_check.check_collision(player.hitbox, self.hitbox)            
            if collision:
                if not (player.team in teams_inside):
                    teams_inside.append(player.team)

        if len(teams_inside) == 1:
            return teams_inside[0]
        return 0
    
    def update(self, **kwargs) -> list:
        """
        Função: update
        Descrição:
            Atualiza a região de dominação e verifica se algum time está dominando a região. Caso algum time estiver dominando, retorna a alteração da pontuação do time de acordo com o tempo de dominação.
        Parâmetros:
            players: list - uma lista com todos os jogadores do jogo.
        Retorno:
            Retorna uma lista com o acréscimo de pontos de cada time após a verificação.
        """
        self.update_region()
        self.curr_team = self.check_domination(kwargs['players'])        

        pts_increase = [0,0]
        if self.curr_team:
            now = time()
            if now - self.last_increment >= 1.0:
                pts_increase[self.curr_team-1] = self.pts_gain
                self.last_increment = now
        return pts_increase

    def draw(self, map_offset:Vector2, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha a área de dominação do jogo de acordo com o time que estiver dominando a área.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        if self.curr_team == 1:
            # Desenha a área de dominação quando o time 1 está dominando
            color = RED
            
        elif self.curr_team == 2:
            # Desenha a área de dominação quando o time 2 está dominando
            color = BLUE
        else:
            # Desenha a área de dominação quando nenhum time está dominando
            color = YELLOW

        pos = [map_offset.x + (self.hitbox.position.x * scaler), map_offset.y + (self.hitbox.position.y * scaler)]
        draw_circle_lines_v(pos, self.hitbox.radius * scaler, color)    
