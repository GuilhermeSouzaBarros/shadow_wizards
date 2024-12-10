from pyray import *
from raylib import *

from vectors import Vector2
from collisions import ColRectangleCircle
from player import Player
from map import Map

class Game:
    def __init__(self) -> None:
        set_config_flags(FLAG_MSAA_4X_HINT)
        set_config_flags(FLAG_WINDOW_RESIZABLE)
        init_window(0, 0, "Jogo épico");
        
        full_size = [get_monitor_width(0), get_monitor_height(0)]
        self.window_size = [int(full_size[0] * 0.8), int(full_size[1] * 0.8)]
        window_pos = (int(full_size[0] * 0.1), int(full_size[1] * 0.1))

        set_window_size(self.window_size[0], self.window_size[1])
        set_window_position(window_pos[0], window_pos[1])
        set_exit_key(KEY_DELETE)
        set_target_fps(60)

        self.rows    = 17
        self.columns = 31

        self.tile_size = Vector2(32, 32)

        self.draw_tile_size = Vector2(0.0, 0.0)
        self.scaler = 0.0
        self.tick = 0.0
        self.close_window = 0
        map_pos = Vector2(0, 0)
        
        self.players = [Player(self.tile_size, self.scaler, map_pos, self.draw_tile_size, GOLD, 1, 1),
                        Player(self.tile_size, self.scaler, map_pos, self.draw_tile_size, RED, self.rows - 2, self.columns - 2)]
        self.map = Map(self.rows, self.columns, self.tile_size, map_pos, self.scaler, self.draw_tile_size)
        self.update_draw_escale()

    def update(self, delta_time) -> None:
        for i, player in enumerate(self.players):
            player.update(i)
        self.update_players_col(delta_time)
        for player in self.players:
            player.hitbox.delta_position(delta_time)
        self.close_window = window_should_close()

    def update_window(self) -> None: 
        window = get_window_handle()
        new_width = ffi.new('int *', 1)
        new_height = ffi.new('int *', 1)
        glfw_get_window_size(window, new_width, new_height)
        self.window_size[0] = float(ffi.unpack(new_width, ffi.sizeof(new_width))[0])
        self.window_size[1] = float(ffi.unpack(new_height, ffi.sizeof(new_width))[0])
        ffi.release(new_width)
        ffi.release(new_height)
        self.update_draw_escale()

    def update_draw_escale(self) -> None:
        self.draw_tile_size.x = self.window_size[0] / self.columns
        self.draw_tile_size.y = self.window_size[1] / self.rows
        if self.draw_tile_size.x > self.draw_tile_size.y:
            self.draw_tile_size.x = self.draw_tile_size.y
        else:
            self.draw_tile_size.y = self.draw_tile_size.x
        self.scaler = self.draw_tile_size.x / self.tile_size.x

        for player in self.players:
            player.draw_size = self.draw_tile_size
            player.scaler = self.scaler
        self.map.draw_size = self.draw_tile_size
        self.map.scaler = self.scaler

    
    def update_players_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile['tipo']):
                    continue
                ColRectangleCircle(tile['rectangle'], self.players[0].hitbox, delta_time)
                ColRectangleCircle(tile['rectangle'], self.players[1].hitbox, delta_time)

    def draw(self) -> None:
        if is_window_resized():
            self.update_window()
        if (is_key_pressed(KEY_F11)):
            ToggleFullscreen()
            
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw()
        for player in self.players:
            player.draw()
        
        end_drawing()