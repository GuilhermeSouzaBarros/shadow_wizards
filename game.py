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

        self.rows    = 17
        self.columns = 31

        self.tile_size = Vector2(32, 32)
        self.draw_tile_size = Vector2(self.window_size[0] / self.columns,
                                      self.window_size[1] / self.rows)
        if self.draw_tile_size.x > self.draw_tile_size.y:
            self.draw_tile_size.x = self.draw_tile_size.y
        else:
            self.draw_tile_size.y = self.draw_tile_size.x

        self.tick = 0.0
        self.close_window = 0
        map_pos = Vector2(0, 0)
        escaler = self.draw_tile_size.x / self.tile_size.x
        self.players = [Player(self.tile_size, escaler, map_pos, self.draw_tile_size, GOLD, 1, 1),
                        Player(self.tile_size, escaler, map_pos, self.draw_tile_size, RED, self.rows - 2, self.columns - 2)]
        self.map = Map(self.rows, self.columns, self.tile_size, map_pos, escaler, self.draw_tile_size)
    
    def update(self, delta_time) -> None:
        for i, player in enumerate(self.players):
            player.update(i)
        self.update_players_col(delta_time)
        for player in self.players:
            player.hitbox.delta_position(delta_time)
        self.close_window = window_should_close()

    def update_players_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile['tipo']):
                    continue
                ColRectangleCircle(tile['rectangle'], self.players[0].hitbox, delta_time)
                ColRectangleCircle(tile['rectangle'], self.players[1].hitbox, delta_time)

    def draw(self) -> None:
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw()
        for player in self.players:
            player.draw()
        
        end_drawing()