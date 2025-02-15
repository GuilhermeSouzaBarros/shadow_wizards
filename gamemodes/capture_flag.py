from pyray import *
from raylib import *

from struct import pack, unpack

from vectors import Vector2
from collisions import CollisionInfo
from gamemodes.obj import Objective
from sprite import FlagSprite

class Flag(Objective):
    def __init__(self, tile_size:int, row:int,column:int, radius:float, team:int):
        super().__init__(tile_size, row, column, radius)
        self.taken = False
        self.team = team

        self.sprite = FlagSprite('sprites/bag.png', self.team-1, Vector2(12, 12))

    def encode(self) -> bytes:
        return pack("dd?", self.hitbox.position.x, self.hitbox.position.y, self.taken)
    
    def decode(self, bytes_string:bytes) -> int:
        data = unpack("dd?", bytes_string[0:17])
        self.taken = data[2]
        pos = Vector2(data[0], data[1])
        self.hitbox.position = pos
        return 17

    def check_taken(self, players: list) -> None:
        self.taken = False
        for player in players:
            if player.team == self.team or not player.is_alive:
                continue

            info = CollisionInfo.collision(player.hitbox, self.hitbox)
            if info.intersection:
                self.taken = True
                player.has_flag = True
                break
            else:
                player.has_flag = False


    def update(self, players:list, delta_time:float, **kwargs) -> list:
        self.check_taken(players)
        if self.taken:
            for player in players:
                if not player.has_flag or player.team == self.team:
                    continue
                self.hitbox.position = player.hitbox.position.copy()
        else:
            self.update_region()
        return [0, 0]
    
    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool) -> None:
        if self.team == 1:
            color = RED
        elif self.team == 2:
            color = BLUE

        if show_hitboxes:
            self.hitbox.draw(color, map_offset, scaler)
        else:
            self.sprite.draw(self.hitbox, map_offset, scaler)
    
    def unload(self):
        unload_texture(self.sprite.texture)

class CapturePoint(Objective):
    def __init__(self, tile_size:int, row:int, column:int, radius:float, team:int):
        super().__init__(tile_size, row, column, radius, 25)
        self.team = team

    def encode(self) -> bytes:
        return "".encode()
    
    def decode(self, bytes_string:bytes) -> int:
        return 0
    
    def check_flag_capture(self, players:list, flag:Flag) -> int:
        """ 
        Retorno:
            0, quando a bandeira não foi capturada por nenhum jogador;
            1, quando a bandeira foi capturada pelo time 1;
            2, quando a bandeira foi capturada pelo time 2.
        """
        for player in players:
            if not player.has_flag or self.team != player.team:
                continue
            info = CollisionInfo.collision(player.hitbox, self.hitbox)
            if info.intersection:
                player.has_flag = False
                flag.update_region()
                return player.team
        return 0

    def update_region(self) -> None:
        super().update_region()

    def update(self, players:list, delta_time:float, **kwargs) -> list:
        self.update_region()
        
        for flag in kwargs['flags']:
            if flag.team == self.team:
                continue
            capture = self.check_flag_capture(players, flag)
        return [(capture == 1) * self.pts_gain, (capture == 2) * self.pts_gain]

    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool) -> None:
        if self.team == 1:    
            # Desenha o ponto de captura do time 1 
            color = RED
        else:
            # Desenha o ponto de captura do time 2
            color = BLUE

        # Calcula a posição em que a região de captura deverá ser desenhada.
        pos = [map_offset.x + (self.hitbox.position.x * scaler), map_offset.y + (self.hitbox.position.y * scaler)]
        draw_circle_lines_v(pos, self.hitbox.radius * scaler, color)

    def unload(self):
        pass