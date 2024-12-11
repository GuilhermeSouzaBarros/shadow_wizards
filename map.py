from pyray import *
from raylib import *

from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle

class Map:
    def __init__(self, rows:int, columns:int, tile_size:Vector2,
                 map_pos:Vector2, scaler:float, draw_size:float) -> None:
        self.tile_size = tile_size
        self.rows      = rows
        self.columns   = columns
        self.tiles     = []
        self.map_pos   = map_pos
        self.scaler   = scaler
        self.draw_size = draw_size
        angle = Vector2(1, 0)
        angle.to_module(1.0)
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                tile = {'rectangle': Rectangle(
                            Vector2(self.tile_size.x * (j + 0.5),
                                    self.tile_size.y * (i + 0.5)),
                                    self.tile_size,
                                    Imaginary(angle.x, angle.y)),
                                    'tipo': 0}
                
                if (i == 0        or j == 0           or
                    i == rows - 1 or j == columns - 1 or
                    not (i % 2    or j % 2)):
                    tile['tipo'] = 1;
                row.append(tile)
            self.tiles.append(row)
    
    def draw(self) -> None:
        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if (not self.tiles[i][j]['tipo']):
                    continue
                tile = self.tiles[i][j]['rectangle']
                pos = [self.map_pos.x + (tile.position.x - tile.size.x/2) * self.scaler,
                       self.map_pos.y + (tile.position.y - tile.size.y/2)* self.scaler]
                draw_rectangle_v(pos, [self.draw_size.x, self.draw_size.y], GREEN)