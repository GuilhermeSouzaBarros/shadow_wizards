from abc import ABC, abstractmethod
from pyray import *
from raylib import *

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

        self.hitbox = Rectangle(
            Vector2(tile_size * (column + 0.5), tile_size * (row + 0.5)),
            Vector2(tile_size, tile_size)
        )

        self.in_vision = []

    @abstractmethod    
    def draw(self, map_offset:list, scaler:float, vision:int) -> None:
        """ Este método é um método abstrato. """            
        raise NotImplementedError


class Floor(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
    
    def draw(self, map_offset:Vector2, scaler:float, vision:int) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha o tile de chão do mapa.
        Parâmetros:
            map_offset:Vector2 - posição do pixel do canto superior esquerdo do mapa.
            scaler:float - transforma as coordenadas do jogo para as de desenho.
        Retorno:
            Nenhum.     
        """
        if (not vision and len(self.in_vision)) or vision in self.in_vision:
            color = color_brightness(GRAY, 0)
        else:
            color = color_brightness(GRAY, -0.5)

        self.hitbox.draw(map_offset, scaler, color, outlines=False)


class Rails(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
        self.is_end = (row == 6 and column == 2) or (row == 8 and column == 22)

    def draw(self, map_offset:Vector2, scaler:float, vision:int) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles de trilhos do mapa.
        Parâmetros:
            map_offset:Vector2 - posição do pixel do canto superior esquerdo do mapa.
            scaler:float - transforma as coordenadas do jogo para as de desenho.
        Retorno:
            Nenhum.     
        """
        # Desenha os trilhos de fim
        if self.is_end:
            color = MAGENTA
        else:
            color = PURPLE

        self.hitbox.draw(map_offset, scaler, color, outlines=False)

class Border(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Border. """
        super().__init__(tile_size, type, row, column)

    def draw(self, map_offset:Vector2, scaler:float, vision:int) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles de borda do mapa.
        Parâmetros:
            map_offset:Vector2 - posição do pixel do canto superior esquerdo do mapa.
            scaler:float - transforma as coordenadas do jogo para as de desenho.
        Retorno:
            Nenhum.     
        """
        # Caso a borda seja a mesma para ambos, remover as condições
        
        if self.type == 4:
            color = BLACK
        else:
            color = BLUE
        self.hitbox.draw(map_offset, scaler, color, outlines=False)


class Barrier(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto barreira. """
        super().__init__(tile_size, type, row, column)
        self.is_destroyed = False 

    def draw(self, map_offset:Vector2, scaler:float, vision:int) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha os tiles barreira, caso a mesma ainda esteja de pé.
        Parâmetros:
            map_offset:Vector2 - posição do pixel do canto superior esquerdo do mapa.
            scaler:float - transforma as coordenadas do jogo para as de desenho.
        Retorno:
            Nenhum.     
        """  
        if self.is_destroyed:
            return
        
        if self.is_destructible:
            # Desenha os tiles destrutíveis
            color = BROWN
        else:
            # Desenha os obstáculos permanentes do mapa
            color = GREEN

        self.hitbox.draw(map_offset, scaler, color, outlines=False)


class SpawnPoint(Tile):
    def __init__(self, tile_size: Vector2, type:int, i:int, j:int):
        super().__init__(tile_size, type, i, j)
        
        # Controla qual a qual player o spawn point corresponde
        self.player_spawn_id = type/5  

    def draw(self, map_offset:Vector2, scaler:float, vision:int):
        """ 
        Função: draw
        Descrição:
            Desenha o spawn point do player correspondente.
        Parâmetros:
            map_offset:Vector2 - posição do pixel do canto superior esquerdo do mapa.
            scaler:float - transforma as coordenadas do jogo para as de desenho.
        Retorno:
            Nenhum.    
        """
        self.hitbox.draw(map_offset, scaler, ORANGE)
