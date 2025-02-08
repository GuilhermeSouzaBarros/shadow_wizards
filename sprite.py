from pyray import *
from raylib import *

from abc import ABC, abstractmethod

from imaginary import Imaginary
from vectors import Vector2
from shapes import Shape, Rectangle, Circle

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
        draw_texture_pro(self.texture, [0, angle * self.size.y, self.size.x, self.size.y], rectangle_dest, (self.offset * scaler).to_list(), 0, self.tint)

class MapSprite(Sprite):
    def __init__(self, path, size=Vector2(0,0), offset=Vector2(0, 0), tint = RAYWHITE):
        super().__init__(path, size, offset, tint)
        

    def draw(self, offset:Vector2=Vector2(0,0), scaler:float=1.0):
        map_pos = [round(offset.x), round(offset.y)]
        draw_texture_ex(self.texture, map_pos, 0.0, scaler, self.tint)

class DestructibleTileSprite(Sprite):
    def __init__(self, path: str, sprite_id:int=1, size=Vector2(0,0), offset=Vector2(0, 0), tint:Color=RAYWHITE):
        super().__init__(path, size, offset, tint)
        self.sprite_id = sprite_id

    def draw(self, hitbox:Rectangle, offset:Vector2=Vector2(0,0), scaler:float=1.0):
        size = [round(hitbox.radius * scaler), round(hitbox.radius * scaler)]
        rectangle_dest = [round(offset.x + (hitbox.position.x - hitbox.size.x * 0.5) * scaler),
                          round(offset.y + (hitbox.position.y - hitbox.size.y * 0.5) * scaler),
                          round(hitbox.size.x * scaler), round(hitbox.size.y * scaler)]
        img_source = [self.sprite_id * self.size.x, 32 * self.size.y, self.size.x, self.size.y]

        draw_texture_pro(self.texture, img_source, rectangle_dest, [round(self.offset.x * scaler), round(self.offset.y * scaler)], 0, self.tint)

class FlagSprite(Sprite):
    def __init__(self, path:str, sprite_id:int, size=Vector2(0,0), offset:Vector2=Vector2(0,0), tint:Color=RAYWHITE):
        super().__init__(path, size, offset, tint)
        self.sprite_id = sprite_id
    
    def draw(self, hitbox:Circle, map_offset:Vector2=Vector2(0,0), scaler:float=1.0):
        radius = Vector2(hitbox.radius, hitbox.radius)
        sprite_pos = (hitbox.position - radius) * scaler + map_offset
        sprite_pos = sprite_pos.to_list()
        
        # Adiciona os tamanhos do sprite
        sprite_pos.append(round(2 * hitbox.radius * scaler))
        sprite_pos.append(round(2 * hitbox.radius * scaler))

        # Calcula a porção da imagem que deve ser utilizada
        img_source = [self.sprite_id * self.size.x, 0, self.size.x, self.size.y]

        draw_texture_pro(self.texture, img_source, sprite_pos, self.offset.to_list(), 0, self.tint)
    

