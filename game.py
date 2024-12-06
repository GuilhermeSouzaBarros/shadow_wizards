from pyray import *
from raylib import *

from vectors import Vector2
from collisions import ColRectangleCircle
from player import Player
from map import Map

class Game:
    def __init__(self) -> None:
        set_config_flags(FLAG_MSAA_4X_HINT)
        init_window(0, 0, "Jogo épico");
        
        full_size = [get_monitor_width(0), get_monitor_height(0)]
        self.window_size = (int(full_size[0] * 0.8), int(full_size[1] * 0.8))
        window_pos = (int(full_size[0] * 0.1), int(full_size[1] * 0.1))

        set_window_size(self.window_size[0], self.window_size[1])
        set_window_position(window_pos[0], window_pos[1])
        set_exit_key(KEY_DELETE)
        set_target_fps(60)

        self.tile = Vector2(self.window_size[0] / 31, self.window_size[1] / 15)
        if self.tile.x > self.tile.y:
            self.tile.x = self.tile.y
        else:
            self.tile.y = self.tile.x

        self.tick = 0.0
        self.close_window = 0
        self.player = Player(self.tile)
        self.map = Map(15, 31, self.tile)
    
    def update(self, delta_time) -> None:
        self.player.update()
        self.update_player_col(delta_time)
        self.player.hitbox.delta_position(delta_time)
        self.close_window = window_should_close()
        print("End update\n")

    def update_player_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile['tipo']):
                    continue
                if (ColRectangleCircle(tile['rectangle'], self.player.hitbox, delta_time).intersection):
                    self.player.hitbox.speed = Vector2(0.0, 0.0)

    def draw(self) -> None:
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw()
        self.player.draw()
        
        end_drawing()
        print(f"End Frame\n\n")