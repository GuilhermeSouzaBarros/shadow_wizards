from pyray import *
from raylib import *

from vectors import Vector2
from collisions import ColRectangleCircle
from player import Player
from map import Map
from objectives import Objectives
from score import Score
from home_screen import HomeScreen

from config import Config

class Game:
    def __init__(self) -> None:
        set_config_flags(FLAG_MSAA_4X_HINT)
        set_config_flags(FLAG_WINDOW_RESIZABLE)

        init_window(0, 0, Config.GAME_TITLE)
        set_target_fps(get_monitor_refresh_rate(get_current_monitor()))

        full_size = [get_monitor_width(0), get_monitor_height(0)]
        self.window_size = [int(full_size[0] * 0.8), int(full_size[1] * 0.8)]
        window_pos = (int(full_size[0] * 0.1), int(full_size[1] * 0.1))

        set_window_size(self.window_size[0], self.window_size[1])
        set_window_position(window_pos[0], window_pos[1])
        
        set_exit_key(KEY_DELETE)
 
        self.tick = 0.0
        self.close_window = 0
        
<<<<<<< HEAD
        self.game_state = Config.STATE_INITIAL_MENU
        self.home_screen = HomeScreen(self.window_size)
=======
        # *** Fazer tela inicial para seleção do mapa ***
        self.map_id = 4
>>>>>>> 472f5406c9dbc9e78ea0f1080233468076f91794

        # *** Serão atualizados na função load_map quando o mapa for escolhido ***
        self.map_id = 0
        self.map = None
        self.tile_size = 0
        self.rows = 0
        self.columns = 0
        self.players = []
        self.objectives = None
        self.score = None

        self.show_hitboxes = False
        self.curr_team_vision = 0 # 0: Both, 1: Team_1, 2: Team_2

        self.map_offset = Vector2(0, 0)
<<<<<<< HEAD
        self.scaler = 0.0
=======
        self.scaler = 1.0
        self.update_draw_scale()
>>>>>>> 472f5406c9dbc9e78ea0f1080233468076f91794

    def update_window(self) -> None: 
        window = get_window_handle()
        new_width = ffi.new('int *', 1)
        new_height = ffi.new('int *', 1)
        glfw_get_window_size(window, new_width, new_height)
        self.window_size[0] = float(ffi.unpack(new_width,  ffi.sizeof(new_width) )[0])
        self.window_size[1] = float(ffi.unpack(new_height, ffi.sizeof(new_height))[0])
        ffi.release(new_width)
        ffi.release(new_height)
        if self.game_state == Config.STATE_PLAY_GAME:
            self.update_draw_scale()
        elif self.game_state == Config.STATE_INITIAL_MENU:
            self.home_screen.update_scale(self.window_size)

    def update_draw_scale(self) -> None:
        draw_tile_size = Vector2(self.window_size[0] / self.columns, self.window_size[1] / self.rows)
        if draw_tile_size.x > draw_tile_size.y:
            self.scaler = draw_tile_size.y / self.tile_size
        else:
            self.scaler = draw_tile_size.x / self.tile_size

    def update_tick(self, delta_time) -> None:
        if self.game_state == Config.STATE_PLAY_GAME:
            for player in self.players:
                player.update()

            self.update_players_col(delta_time)

            for player in self.players:
                player.hitbox.delta_position(delta_time)
                player.sword.update(player.hitbox.position, player.angle, player.player_id)

            self.update_sword_col(delta_time)
            
            score_increase = self.objectives.update(self.players, delta_time)
            self.score.update(self.players, score_increase)

    
    def update_players_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile.type):
                    continue
                for player in self.players:
                    info = ColRectangleCircle(tile.hitbox, player.hitbox, delta_time)
                    if info.intersection:
                        if tile.is_destructible:
                            if not tile.is_destroyed:
                                player.col_handle_tile(tile.hitbox, info.lines_col, delta_time)
                        elif tile.has_collision:
                            player.col_handle_tile(tile.hitbox, info.lines_col, delta_time)
        
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

    def update_frame(self) -> None:
        if (is_key_pressed(KEY_F11)):
            ToggleFullscreen()

        if self.game_state == Config.STATE_INITIAL_MENU:
            play = self.home_screen.update()
            if play:
                self.game_state = Config.STATE_PLAY_GAME
                self.load_map(self.home_screen.selected_map)   
                self.update_draw_scale() 
        elif self.game_state == Config.STATE_PLAY_GAME:
            if (is_key_pressed(KEY_H)):
                self.show_hitboxes = not self.show_hitboxes
                print(f"Hiboxes {self.show_hitboxes}")

            if (is_key_pressed(KEY_V)):
                self.curr_team_vision += 1
                self.curr_team_vision %= 3
                print(f"Visão {self.curr_team_vision}")


        if is_window_resized():
            self.update_window()
        
        self.close_window = window_should_close()

    def draw(self) -> None:
        begin_drawing()
        
        clear_background(GRAY)
        if self.game_state == Config.STATE_INITIAL_MENU:
            self.home_screen.draw()
        elif self.game_state == Config.STATE_PLAY_GAME:
            self.map.draw        (self.map_offset, self.scaler)
            self.objectives.draw (self.map_offset, self.scaler)
            self.score.draw      (self.scaler)
            for player in self.players:
                player.draw  (self.map_offset, self.scaler, self.show_hitboxes)
        
        end_drawing()
    
    def load_map(self, map_id:int) -> None:
        self.map_id = map_id
        self.map = Map(self.map_id)

        self.tile_size = self.map.tile_size

        self.rows = self.map.num_rows
        self.columns = self.map.num_columns

        self.players = [Player(self.tile_size,
                               self.map.map_info['spawn_points']['player_1'][0],
                               self.map.map_info['spawn_points']['player_1'][1],
                               self.map.map_info['spawn_points']['player_1'][2],
                               1, self.map_id,
                               "player 1", "sprites/wizard.png", 
                               self.home_screen.selected_skin),
                        
                        Player(self.tile_size,
                               self.map.map_info['spawn_points']['player_2'][0],
                               self.map.map_info['spawn_points']['player_2'][1],
                               self.map.map_info['spawn_points']['player_2'][2],
                               2, self.map_id,
                               "player 2", "sprites/wizard.png", BLUE)]

        self.objectives = Objectives(self.tile_size, self.map.map_info['objectives'], self.map_id)
        # Carrega todos os objetivos de acordo com o id do mapa
        self.objectives.load()

        num_teams = len(self.players) if self.map_id == 1 else 2
        self.score = Score(num_teams)