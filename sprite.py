from pyray import *
from raylib import *

from abc import ABC, abstractmethod

from imaginary import Imaginary
from vectors import Vector2
from shapes import Shape

class Sprite(ABC):
    def __init__(self, path:str, size:Vector2, offset:Vector2, tint:Color):
        self.texture = load_texture(path)
        self.size = size
        self.offset = offset
        self.tint = tint
    
    @abstractmethod
    def draw(self, shape:Shape, offset:Vector2=Vector2(0, 0), scaler:float=1):
        raise NotImplementedError
    
class CharacterSprite(Sprite):
    def __init__(self, path:str, size:Vector2, offset:Vector2, tint:Color):
        Sprite.__init__(self, path, size, offset, tint)

    def draw(self, hitbox:Shape, angle:Imaginary, offset:Vector2=Vector2(0, 0), scaler:float=1):
        angle = round(angle.to_degree() / 45)
        size = [hitbox.radius * scaler, hitbox.radius * scaler]
        rectangle_dest = [round(offset.x + hitbox.position.x * scaler - size[0]),
                          round(offset.y + hitbox.position.y * scaler - size[1]),
                          round(2 * size[0]), round(2 * size[1])]
        draw_texture_pro(self.texture, [0, angle * 32, 32, 32], rectangle_dest, (self.offset * scaler).to_list(), 0, self.tint)
