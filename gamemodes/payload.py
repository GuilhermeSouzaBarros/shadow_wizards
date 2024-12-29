from pyray import *
from raylib import *

from utils import sign_of
from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle, Circle
from collisions import ColCircleCircle

class Cart:
    def __init__(self, path:list, path_start:int, region_radius:int, draw_size:Vector2, tile_size:float, map_pos:float, scaler:float=1.0):
        self.map_pos = map_pos
        self.draw_size = draw_size
        self.scaler = scaler

        self.region_radius = region_radius
        self.tile_size = tile_size

        row    = path[path_start][0]
        column = path[path_start][1]
        self.hitbox = Rectangle(
                            Vector2(tile_size * (column + 0.5),
                                    tile_size * (row + 0.5)),
                                    Vector2(tile_size, tile_size),
                                    Imaginary())
        self.region = Circle(
                            Vector2(tile_size * (column + 0.5), 
                                    tile_size * (row + 0.5)), 
                                    tile_size * region_radius)
        
        self.path         = path
        self.path_start   = path_start
        self.current_line = [path_start, path_start + 1]
        self.speed        = 2 # in tiles per second, keep it simple

        self.color = WHITE
        self.curr_team = 0
        self.end_push  = 0
        self.winning_team = 0
    
    def update(self, players:list, delta_time:float) -> list:
        self.hitbox.speed = Vector2(0, 0)
        if self.end_push:
            return
        team_push = self.check_domination(players)
        if self.curr_team != team_push:
            print(f"Current team pushing: {team_push}\n")
            self.curr_team = team_push

        if not team_push:
            self.color = WHITE
            return

        elif team_push == 1:
            self.color = RED
            to_point_in_line = 1

        elif team_push == 2:
            self.color = BLUE
            to_point_in_line = 0
        
        next_point_pos = Vector2((self.path[self.current_line[to_point_in_line]][1] + 0.5) * self.tile_size,
                                 (self.path[self.current_line[to_point_in_line]][0] + 0.5) * self.tile_size)
        distance = next_point_pos - self.hitbox.position

        delta_pos = self.speed * self.tile_size * delta_time
        if (abs(distance.x) > delta_pos or abs(distance.y) > delta_pos) :
            self.hitbox.speed.x = sign_of(distance.x) * self.speed * self.tile_size
            self.hitbox.speed.y = sign_of(distance.y) * self.speed * self.tile_size
        else:
            self.hitbox.speed.x = distance.x / delta_time
            self.hitbox.speed.y = distance.y / delta_time
            
            next_point = -1 + 2 * to_point_in_line
            self.current_line[0] += next_point
            self.current_line[1] += next_point

            if self.current_line[0] == -1 or self.current_line[1] == len(self.path):
                self.end_push = 1
                self.winning_team = self.curr_team
                print(f"Push ended, team {self.curr_team} won")
    
        self.hitbox.delta_position(delta_time)
        self.region.position = self.hitbox.position.copy()


    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região do carrinho.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        self.region = Circle(self.rectangle.position, self.region_radius)
        

    def draw(self) -> None:
        self.draw_cart()
        self.draw_region()

    def draw_cart(self) -> None:
        self.hitbox.draw(self.map_pos, self.scaler, self.color)
        self.hitbox.draw_lines(self.map_pos, self.scaler, BLACK)

    def draw_region(self) -> None:
        """
        Função: draw
        Descrição:
            Desenha a região de movimentação do carrinho de acordo com o time que estiver movimentando o carrinho.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        pos = [self.map_pos.x + (self.region.position.x * self.scaler),
               self.map_pos.y + (self.region.position.y * self.scaler)]
        draw_circle_lines_v(pos, self.region.radius * self.scaler, self.color)
            

    def check_domination(self, players:list) -> int:
        """
        Função: check_domination
        Descrição:
            Verifica se o carrinho está sendo movimentado por algum time.
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno: 
            0, quando nenhum time estiver movimentando o carrinho;
            1, quando o time 1 estiver movimentando o carrinho;
            2, quando o time 2 estiver movimentando o carrinho.
        """
        teams_inside = []
        collision_check = ColCircleCircle()
        for player in players:
            
            collision = collision_check.check_collision(player.hitbox, self.region, self.scaler)            
            if collision:
                if not (player.team in teams_inside):
                    teams_inside.append(player.team)

        if len(teams_inside) == 1:
            return teams_inside[0]
        return 0