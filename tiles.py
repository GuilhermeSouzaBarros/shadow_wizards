from abc import ABC, abstractmethod
from pyray import *
from raylib import *
from random import randint

import sprite
from vectors import Vector2
from shapes import Rectangle

class Tile(ABC):
    def __init__(self, tile_size:Vector2, type:int , row:int, column:int) -> None:
        """ Inicializa o tile com seu tipo, um booleano para determinar se ele é 
            destrutível ou não, o seu ângulo e seu retângulo correspondente. """
        # Determina o tipo do tile
        self.type = type

        # Controla se o tile é destrutível ou não
        self.is_destructible = self.type >= 3 and self.type <= 6

        self.has_collision = not(self.type == 7 or self.type == 8 or (not self.type))

        self.hitbox = Rectangle(
            Vector2(tile_size * (column + 0.5), tile_size * (row + 0.5)),
            Vector2(tile_size, tile_size)
        )


    @abstractmethod    
    def draw(self, map_offset:list, scaler:float, draw_hitbox:bool) -> None:
        """ Este método é um método abstrato. """            
        raise NotImplementedError


class Floor(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
    
    def draw(self, map_offset:Vector2, scaler:float, draw_hitbox:bool) -> None:
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
        self.hitbox.draw(GRAY, map_offset, scaler, outlines=False)


class Rails(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Floor. """
        super().__init__(tile_size, type, row, column)
        self.is_end = (row == 6 and column == 2) or (row == 8 and column == 22)

    def draw(self, map_offset:Vector2, scaler:float, draw_hitbox:bool) -> None:
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

        self.hitbox.draw(color, map_offset, scaler, outlines=False)

class Border(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto Border. """
        super().__init__(tile_size, type, row, column)

    def draw(self, map_offset:Vector2, scaler:float, draw_hitbox:bool) -> None:
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
        color = BLACK
        self.hitbox.draw(color, map_offset, scaler, outlines=False)


class Barrier(Tile):
    def __init__(self, tile_size: Vector2, type:int, row:int, column:int) -> None:
        """ Inicializa o objeto barreira. """
        super().__init__(tile_size, type, row, column)
        self.is_destroyed = False 
        if self.is_destructible:
            self.sprite = self.build_destructible_barrier()

    def draw(self, map_offset:Vector2, scaler:float, draw_hitbox:bool) -> None:
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
            if draw_hitbox:
                color = BROWN
                self.hitbox.draw(color, map_offset, scaler, outlines=False)
            else:
                self.sprite.draw(self.hitbox, map_offset, scaler)
        elif draw_hitbox:
            # Desenha os obstáculos permanentes do mapa
            color = GREEN
            self.hitbox.draw(color, map_offset, scaler, outlines=False)

    def build_destructible_barrier(self):
        """
        Método: build_destructible_barrier
        Descrição: 
            Constrói os sprites dos tiles destrutíveis do mapa.
        Parâmetros:
            Nenhum.
        Retorno: Nenhum.
        """
        
        # Sprite de cone
        if self.type == 3:
            return sprite.DestructibleTileSprite('sprites/cones.png', 0, self.hitbox.size)
        # Sprite de containers
        if self.type == 4:
            return sprite.DestructibleTileSprite('sprites/containers.png', randint(0, 15), self.hitbox.size)
        # Sprite de veículos
        if self.type == 5:
            return sprite.DestructibleTileSprite('sprites/vehicules.png', randint(0, 19), self.hitbox.size)
        # Sprite de veículos no mesmo sentido
        if self.type == 6:
            return sprite.DestructibleTileSprite('sprites/same_way_vehicules.png', randint(0, 9), self.hitbox.size)   
