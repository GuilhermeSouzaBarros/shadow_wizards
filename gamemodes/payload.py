from pyray import *
from raylib import *

from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle, Circle
from collisions import ColCircleCircle

from time import time

class Cart:
    def __init__(self, path:list, path_idx:int, region_radius:int, draw_size:Vector2, tile_size:float, map_pos:float, row:int, column:int, scaler:float=0.0):
        self.scaler = scaler

        self.region_radius = region_radius
        self.tile_size = tile_size
        self.map_pos = map_pos
        self.draw_size = draw_size


        self.angle = Vector2(1, 0)
        self.angle.to_module(1.0)
        self.rectangle = Rectangle(
                            Vector2(tile_size * (column + 0.5),
                                    tile_size * (row + 0.5)),
                                    Vector2(tile_size, tile_size),
                                    Imaginary(self.angle.x, self.angle.y))
        self.region = Circle(
                            Vector2(tile_size * (column + 0.5), 
                                    tile_size * (row + 0.5)), 
                                    region_radius * self.scaler)
        self.path = path
        self.path_idx = path_idx
        self.delta_pos = Vector2(0, 0)

        self.row = row
        self.column = column

        self.curr_team = 0
        self.last_increment:float = 0.0
    
    def update(self, players:list) -> list:
        pass

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
        self.region = Circle(self.rectangle.position, self.region_radius * 0.5)
        

    def draw(self) -> None:
        self.draw_region()
        self.draw_cart()

    def draw_cart(self) -> None:
        pos = [self.map_pos.x + (self.rectangle.position.x - self.rectangle.size.x/2) * self.scaler,
               self.map_pos.y + (self.rectangle.position.y - self.rectangle.size.y/2) * self.scaler]
        draw_rectangle_v(pos, [self.draw_size.x, self.draw_size.y], BLACK)

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
        pos = [self.map_pos.x + (self.region.position.x * self.scaler), self.map_pos.y + (self.region.position.y * self.scaler)]
        if self.curr_team == 1:
            # Desenha a região do carrinho quando o time 1 estiver movimentando
            draw_circle_lines_v(pos, self.region.radius * self.scaler, BLUE)
            
        elif self.curr_team == 2:
            # Desenha a região do carrinho quando o time 2 estiver movimentando
            draw_circle_lines_v(pos, self.region.radius * self.scaler, RED)
        else:
            # Desenha a região do carrinho quando nenhum time estiver movimentando
            draw_circle_lines_v(pos, self.region.radius * self.scaler, YELLOW) 

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