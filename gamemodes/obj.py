from pyray import *
from raylib import *

from abc import ABC, abstractmethod

from shapes import Circle

class Objective(ABC):
    def __init__(self, tile_size:int, map_pos:Vector2, row:int, column:int, radius:float, scaler:float=0.0, pts_gain:int=1):
        self.radius = radius        
        self.map_pos = map_pos
        self.tile_size = tile_size
        self.row = row
        self.column = column
        self.scaler = scaler
        self.region = Circle(Vector2(self.tile_size * (self.column + 0.5), self.tile_size * (self.row + 0.5)), self.radius * self.scaler)

        self.pts_gain = pts_gain # Acréscimo de pontos do time com a conquista do objetivo

    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região do objetivo.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        position = Vector2(self.tile_size * (self.column + 0.5), self.tile_size * (self.row + 0.5))
        self.region = Circle(position, self.radius * 0.5)

    @abstractmethod
    def update(self, players:list=[]) -> list:
        """ Este método é um método abstrato. """
        raise NotImplementedError

    @abstractmethod
    def draw(self) -> None:
        """ Este método é um método abstrato. """
        raise NotImplementedError