from abc import ABC, abstractmethod
from pyray import *
from raylib import *

from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle

class Tile(ABC):
    def __init__(self, tile_size:Vector2, type:int , row:int, column:int) -> None:
        """ Inicializa o tile com seu tipo, um booleano para determinar se ele é 
            destrutível ou não, o seu ângulo e seu retângulo correspondente. """
        # Determina o tipo do tile
        self.type = type

        # Controla se o tile é destrutível ou não
        self.is_destructible = self.type == 1

        self.has_collision = not(self.type == 7 or self.type == 8 or (not self.type % 5))

        self.angle = Vector2(1, 0)
        self.angle.to_module(1.0)
        self.rectangle = Rectangle(
                            Vector2(tile_size.x * (column + 0.5),
                                    tile_size.y * (row + 0.5)),
                                    tile_size,
                                    Imaginary(self.angle.x, self.angle.y))

    @abstractmethod    
    def draw(self, pos:list, draw_size: list) -> None:
        """ Este método é um método abstrato. """            
        raise NotImplementedError

class Floor(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
    
    def draw(self, pos:list, draw_size: list) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha o tile de chão do mapa.
        Parâmetros:
            pos: list - uma lista com a posição do tile;
            draw_size: list - uma lista com o tamanho que deverá ser desenhado o tile.
        Retorno:
            Nenhum.     
        """
        pass

class Rails(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
        self.is_end = (row == 6 and column == 2) or (row == 8 and column == 22)

    def draw(self, pos, draw_size) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles de trilhos do mapa.
        Parâmetros:
            pos: list - uma lista com a posição do tile;
            draw_size: list - uma lista com o tamanho que deverá ser desenhado o tile.
        Retorno:
            Nenhum.     
        """
        # Desenha os trilhos de fim
        if self.is_end:
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], MAGENTA)
        else:
            # Desenha os trilhos do carrinho
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], PURPLE)

class Border(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Border. """
        super().__init__(tile_size, type, row, column)

    def draw(self, pos, draw_size) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles de borda do mapa.
        Parâmetros:
            pos: list - uma lista com a posição do tile;
            draw_size: list - uma lista com o tamanho que deverá ser desenhado o tile.
        Retorno:
            Nenhum.     
        """
        # Caso a borda seja a mesma para ambos, remover as condições
        
        if self.type == 4:
            # Desenha as bordas superiores do mapa
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], BLACK)
        else:
            # Desenha as bordas laterais do mapa
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], BLUE)

class Barrier(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto barreira. """
        super().__init__(tile_size, type, row, column)
        self.is_destroyed = False 

    def draw(self, pos:list, draw_size: list) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles barreira, caso a mesma ainda esteja de pé.
        Parâmetros:
            pos: list - uma lista com a posição do tile;
            draw_size: list - uma lista com o tamanho que deverá ser desenhado o tile.
        Retorno:
            Nenhum.     
        """  
        if self.is_destructible:
            if not self.is_destroyed:
                # Desenha os tiles destrutíveis
                draw_rectangle_v(pos, [draw_size.x, draw_size.y], BROWN)
        else:
            # Desenha os obstáculos permanentes do mapa
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], GREEN)

class SpawnPoint(Tile):
    def __init__(self, tile_size: Vector2, type:int, i:int, j:int):
        super().__init__(tile_size, type, i, j)
        
        # Controla qual a qual player o spawn point corresponde
        self.player_spawn_id = type/5  

    def draw(self, pos:list, draw_size: list):
        """ 
        Função: draw
        Descrição:
            Desenha o spawn point do player correspondente.
        Parâmetros:
            pos: list - uma lista com a posição do tile;
            draw_size: list - uma lista com o tamanho que deverá ser desenhado o tile.
        Retorno:
            Nenhum.    
        """
        if self.player_spawn_id == 1:
            # Desenha o spawn point do player 1
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], ORANGE)
        elif self.player_spawn_id == 2:
            # Desenha o spawn point do player 2
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], ORANGE)
        elif self.player_spawn_id == 3:
            # Desenha o spawn point do player 3
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], ORANGE)
        else:
            # Desenha o spawn point do player 4
            draw_rectangle_v(pos, [draw_size.x, draw_size.y], ORANGE)