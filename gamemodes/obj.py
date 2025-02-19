from pyray import *
from raylib import *

from abc import ABC, abstractmethod

from vectors import Vector2
from shapes import Circle

class Objective(ABC):
    def __init__(self, tile_size:int, row:int, column:int, radius:float, pts_gain:int=1):
        self.radius = radius
        self.tile_size = tile_size
        self.row = row
        self.column = column
        self.hitbox = Circle(Vector2(tile_size * (column + 0.5), tile_size * (row + 0.5)), radius)

        self.pts_gain = pts_gain # Acréscimo de pontos do time com a conquista do objetivo

    def update_region(self) -> None:
        position = Vector2(self.tile_size * (self.column + 0.5), self.tile_size * (self.row + 0.5))
        self.hitbox = Circle(position, self.radius)

    @abstractmethod
    def encode(self) -> bytes:
        """ Este método é um método abstrato. """
        raise NotImplementedError
    
    @abstractmethod
    def decode(self, bytes_string:bytes) -> int:
        """ Este método é um método abstrato. """
        raise NotImplementedError
    
    @abstractmethod
    def update(self, **kwargs) -> list:
        """ Este método é um método abstrato. """
        raise NotImplementedError

    @abstractmethod
    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool) -> None:
        """ Este método é um método abstrato. """
        raise NotImplementedError
    
    def unload(self):
        raise NotImplementedError