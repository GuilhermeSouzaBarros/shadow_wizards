from pyray import *
from raylib import *

from vectors import Vector2
from collisions import CollisionInfo
from player import Player
from map import Map
from objectives import Objectives
from score import Score

from shapes import Rectangle

class Game:
    def __init__(self, window_size, map_id:int, skin_color:int) -> None:
        self.tick = 0.0
        
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

        # lista de habilidades que afetam outros players
        self.active_skills = ["Fireball", "Gun", "Trap"]

        self.scaler = 1.0

        self.load_map(map_id, skin_color)   
        self.update_draw_scale(window_size) 

        self.show_hitboxes = False
        self.curr_team_vision = 0 # 0: Both, 1: Team_1, 2: Team_2

        self.test_tile = Rectangle(Vector2(0, 0), Vector2(32, 32))


    def update_draw_scale(self, window_size:list) -> None:
        draw_tile_size = Vector2(window_size[0] / self.columns, window_size[1] / self.rows)
        if draw_tile_size.x > draw_tile_size.y:
            self.scaler = draw_tile_size.y / self.tile_size
        else:
            self.scaler = draw_tile_size.x / self.tile_size

    def update_players_col(self, delta_time:float) -> None:
        for row in self.map.tiles:
            for tile in row:
                if (not tile.type):
                    continue
                if (tile.is_destructible and not tile.is_destroyed) or tile.has_collision:
                    for player in self.players:
                        info = CollisionInfo.collision(player.hitbox, tile.hitbox, delta_time, calculate_distance=True)
                        if info.intersection:
                            player.hitbox.speed -= info.distance * (1 / delta_time)

    def update_sword_col(self) -> None:
        for player_a in self.players:
            if not (player_a.is_alive and player_a.sword.active):
                continue

            for player_b in self.players:
                if player_a == player_b or not player_b.is_alive:
                    continue

                info = CollisionInfo.collision(player_a.sword.hitbox, player_b.hitbox)
                if info.intersection:
                    player_a.killed()
                    player_b.died()

    def clear_vision(self) -> None:
        for player in self.players:
            player.in_vision = [player.team]

        for tile_row in self.map.tiles:
            for tile in tile_row:
                tile.in_vision = []
        
        for objective_type in self.objectives.objectives:
            for objective in self.objectives.objectives[objective_type]:
                objective.in_vision = []

    def update_vision(self) -> None:
        for player in self.players:
            if not player.is_alive or (self.curr_team_vision and player.team != self.curr_team_vision):
                continue
            for tile_row in self.map.tiles:
                for tile in tile_row:
                    if player.is_in_vision(tile.hitbox):
                        if player.team not in tile.in_vision:
                            tile.in_vision.append(player.team)
            
            for objective_type in self.objectives.objectives:
                for objective in self.objectives.objectives[objective_type]:
                    if player.is_in_vision(objective.hitbox):
                        if player.team not in objective.in_vision:
                            objective.in_vision.append(player.team)

            for other_player in self.players:
                if other_player == player:
                    continue
                if player.is_in_vision(other_player.hitbox):
                    if player.team not in other_player.in_vision:
                        other_player.in_vision.append(player.team)
        # Not at all finished, just basic distance checking

    def update_tick(self, delta_time) -> None:
        """
        angle = Imaginary(3 ** 0.5, 1, 1)
        print(f"angle to sum: {angle.__str__}")
        for i in range(0, 8):
            print(f"Curr: {self.test_tile.angle.__str__}")
            print(self.test_tile.distance_to_side(Imaginary()).__str__)
            print( )
            self.test_tile.angle *= angle
        1/0
        """
        for player in self.players:
            player.update()

        self.update_players_col(delta_time)

        for player in self.players:
            player.hitbox.delta_position(delta_time)
            player.sword.update(player.hitbox.position, player.angle, player.player_id)
            player.character.skill.update(player.hitbox.position.copy(), player.angle.copy())

        self.update_sword_col()
        
        score_increase = self.objectives.update(self.players, delta_time)
        self.score.update(self.players, score_increase)
    
    def update_frame(self) -> None:
        self.clear_vision()
        self.update_vision()
            
        if (is_key_pressed(KEY_H)):
            self.show_hitboxes = not self.show_hitboxes
            print(f"Hiboxes {self.show_hitboxes}")

        if (is_key_pressed(KEY_V)):
            self.curr_team_vision += 1
            self.curr_team_vision %= 3
            print(f"Visão {self.curr_team_vision}")
        
    def draw(self) -> None:
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw        (self.map_offset, self.scaler, self.curr_team_vision)
        self.objectives.draw (self.map_offset, self.scaler, self.curr_team_vision)
        self.score.draw      (self.scaler)
        for player in self.players:
            player.draw  (self.map_offset, self.scaler, self.curr_team_vision, self.show_hitboxes)

        end_drawing()
    
    def load_map(self, map_id:int, skin_color:int) -> None:
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
                               skin_color),
                        
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