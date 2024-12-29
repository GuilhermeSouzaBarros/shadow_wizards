from pyray import *
from raylib import *

from vectors import Vector2
from collisions import ColRectangleCircle
from player import Player
from map import Map
from objectives import Objectives
from score import Score

class Game:
    def __init__(self) -> None:
        set_config_flags(FLAG_MSAA_4X_HINT)
        set_config_flags(FLAG_WINDOW_RESIZABLE)

        init_window(0, 0, "Jogo épico")
        set_target_fps(get_monitor_refresh_rate(get_current_monitor()))

        full_size = [get_monitor_width(0), get_monitor_height(0)]
        self.window_size = [int(full_size[0] * 0.8), int(full_size[1] * 0.8)]
        window_pos = (int(full_size[0] * 0.1), int(full_size[1] * 0.1))

        set_window_size(self.window_size[0], self.window_size[1])
        set_window_position(window_pos[0], window_pos[1])
        
        set_exit_key(KEY_DELETE)
 
        self.draw_tile_size = Vector2(0.0, 0.0)
        self.scaler = 0.0
        self.tick = 0.0
        self.close_window = 0
        map_pos = Vector2(0, 0)
        # *** Fazer tela inicial para seleção do mapa ***
        self.map_id = 4

        self.map = Map(map_pos, self.scaler, self.draw_tile_size, self.map_id)

        self.tile_size = self.map.tile_size

        self.rows = self.map.num_rows
        self.columns = self.map.num_columns

        self.players = [Player(self.tile_size, self.scaler, map_pos,
                               self.draw_tile_size, self.map.map_info['spawn_points']['player_1'][0], self.map.map_info['spawn_points']['player_1'][1],
                               1, self.map_id,
                               "player 1", "sprites/wizard.png", RED),
                        
                        Player(self.tile_size, self.scaler, map_pos,
                               self.draw_tile_size, self.map.map_info['spawn_points']['player_2'][0], self.map.map_info['spawn_points']['player_2'][1],
                               2, self.map_id,
                               "player 2", "sprites/wizard.png", BLUE)]



        self.objectives = Objectives(self.map.map_info['objectives'], self.map_id, self.draw_tile_size, self.tile_size.x, map_pos, self.scaler)
        # Carrega todos os objetivos de acordo com o id do mapa
        self.objectives.load()

        num_teams = len(self.players) if self.map_id == 1 else 2
        self.score = Score(num_teams)

        self.update_draw_scale()

    def update(self, delta_time) -> None:
        for i, player in enumerate(self.players):
            player.update(i)
        self.update_players_col(delta_time)
        self.update_sword_col(delta_time)
        
        score_increase = self.objectives.update(self.players)
        self.score.update(self.players, score_increase)
        
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
        self.update_draw_scale()

    def update_draw_scale(self) -> None:
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
            player.sword.scaler = self.scaler

        self.map.draw_size = self.draw_tile_size
        self.map.scaler = self.scaler
        self.objectives.scaler = self.scaler
    
    def update_players_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile.type):
                    continue
                for player in self.players:
                    info = ColRectangleCircle(tile.rectangle, player.hitbox, delta_time)
                    if info.intersection:
                        if tile.is_destructible:
                            if not tile.is_destroyed:
                                player.col_handle_tile(tile.rectangle, info.lines_col, delta_time)
                        elif tile.has_collision:
                            player.col_handle_tile(tile.rectangle, info.lines_col, delta_time)
        
    def update_sword_col(self, delta_time:float) -> None:
        for player_a in self.players:
            if not (player_a.is_alive and player_a.sword.active):
                continue

            for player_b in self.players:
                if not player_b.is_alive or player_a == player_b:
                    continue

                info = ColRectangleCircle(player_a.sword.hitbox, player_b.hitbox, delta_time)

                if info.intersection:
                    player_a.killed()
                    player_b.died()
                    print(f"{player_a.nick} killed {player_b.nick}")
                    print(f"{player_a.nick}: {player_a.kills} / {player_a.deaths}")
                    print(f"{player_b.nick}: {player_b.kills} / {player_b.deaths}\n")


    def draw(self) -> None:
        if is_window_resized():
            self.update_window()
        if (is_key_pressed(KEY_F11)):
            ToggleFullscreen()
            
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw()
        self.objectives.draw()
        self.score.draw()
        for player in self.players:
            if player.is_alive:
                player.draw()
        
        end_drawing()