from pyray import *
from raylib import *
import struct

from sockets.server import Server
from sockets.client import Client

from vectors import Vector2
from collisions import CollisionInfo
from player import Player
from map import Map
from objectives import Objectives
from score import Score
from shapes import ColCircleLine

class Game:
    def __init__(self, server:Server, client:Client, window_size, map_id:int, server_addr_id:dict, characters_id:dict) -> None:
        self.tick = 0.0
        self.server = server
        self.client = client

        self.server_addr_id = server_addr_id
        self.players_input = {}
        for addr in self.server_addr_id:
            self.players_input.update(
                {addr: {"up": False, "left": False, "down": False, "right": False,
                        "ability": False, "sword": False}})
    
        # *** Serão atualizados na função load_map quando o mapa for escolhido ***
        self.map_id = map_id
        self.map = None
        self.players = []
        self.objectives = None
        self.score = None
        self.map_offset = None
        self.scaler = None
        self.show_hitboxes = False
        self.end = False

        # lista de habilidades que afetam outros players
        self.active_skills = ["Fireball", "Gun", "Trap"]

        self.load_map(characters_id)   
        self.update_draw_scale(window_size) 

    def update_draw_scale(self, window_size:list) -> None:
        draw_tile_size = Vector2(window_size[0] / self.map.num_columns,
                                 window_size[1] / self.map.num_rows)
        if draw_tile_size.x > draw_tile_size.y:
            self.scaler = draw_tile_size.y / self.map.tile_size
            self.map_offset = Vector2((window_size[0] - self.map.num_columns * draw_tile_size.y) / 2, 0)
        else:
            self.scaler = draw_tile_size.x / self.map.tile_size
            self.map_offset = Vector2(0, (window_size[1] - self.map.num_rows * draw_tile_size.x) / 2)

    def load_map(self, players_id:list) -> None:
        self.map = Map(self.map_id)
        
        for player_id in players_id:
            self.players.append(Player(self.map.tile_size,
                                self.map.map_info['spawn_points'][f'player_{player_id}'][0],
                                self.map.map_info['spawn_points'][f'player_{player_id}'][1],
                                self.map.map_info['spawn_points'][f'player_{player_id}'][2],
                                player_id, players_id[player_id], self.map_id, f"player {player_id}"))

        self.objectives = Objectives(self.map.tile_size, self.map.map_info['objectives'], self.map_id)
        # Carrega todos os objetivos de acordo com o id do mapa
        self.objectives.load()

        num_teams = len(self.players) if self.map_id == 1 else 2
        self.score = Score(num_teams)

    def encode_input(self) -> bytes:
        message = "i".encode()
        keys = [KEY_UP, KEY_LEFT, KEY_DOWN, KEY_RIGHT, KEY_X, KEY_C]
        for key in keys:
            message += (is_key_down(key)).to_bytes(1)
        return message

    def decode_input(self, player:tuple, input:bytes) -> None:
        for i, key in enumerate(self.players_input[player]):
            self.players_input[player][key] = bool(input[i])

    def encode_game(self) -> bytes:
        message = "g".encode()
        for player in self.players:
            message += player.encode()
        return message

    def decode_game(self, game:bytes):
        pointer = 0
        for player in self.players:
            pointer += player.decode(game[pointer:])

    def update_players_col(self, delta_time:float) -> None:
        for tile in self.map.collision_hitboxes:
            for player in self.players:
                if (player.skill_name == "Intangibility" and player.skill.is_activated):
                    for border in self.map.borders:
                        info = CollisionInfo.collision(player.hitbox, border.hitbox, delta_time, calculate_distance=True)
                        if info.intersection:
                            player.hitbox.speed -= info.distance / delta_time
                    continue
                        
                info = CollisionInfo.collision(player.hitbox, tile, delta_time, calculate_distance=True)
                if info.intersection:
                    player.hitbox.speed -= info.distance / delta_time

    def update_sword_col(self) -> None:
        for player_a in self.players:
            if not (player_a.is_alive and player_a.sword.active):
                continue

            for player_b in self.players:
                if player_a == player_b or not player_b.is_alive:
                    continue
                
                if player_b.skill_name == "Shield" and player_b.skill.is_activated:
                    continue
                info = CollisionInfo.collision(player_a.sword.hitbox, player_b.hitbox)
                if info.intersection:
                    player_a.killed()
                    player_b.died()

    def update_skill_player_col(self, delta_time:float) -> None:
        for player_a in self.players:
            for player_b in self.players:
                if player_a == player_b:
                    continue
                
                projectiles = ["Gun", "Fireball", "Traps", "Laser"]
                skill_name = player_a.skill_name
                if not skill_name in projectiles:
                    continue

                for hitbox in player_a.skill.hitboxes:
                    if skill_name != "Laser":
                        if not hitbox.is_activated:
                            continue
                        info = CollisionInfo.collision(player_b.hitbox, hitbox.hitbox, delta_time)
                        if info.intersection:
                            player_a.killed()
                            player_b.died()
                            player_a.skill.apply_effect(hitbox)
                    else:
                        if not player_a.skill.is_activated:
                            continue
                        info = ColCircleLine(player_b.hitbox, hitbox, delta_time)
                        if info.did_intersect and player_b.is_alive:
                            player_a.killed()
                            player_b.died()
                            player_a.skill.apply_effect(hitbox)
                    
    def update_skill_col(self, delta_time:float) -> None:
        for tile in self.map.collision_hitboxes:
            for player in self.players:
                projectiles = ["Gun", "Fireball"]
                if not (player.skill_name in projectiles):
                    continue
                for projectile in player.skill.hitboxes:
                    info = CollisionInfo.collision(projectile.hitbox, tile, delta_time, calculate_distance=True)
                    if info.intersection:
                        player.skill.apply_effect(projectile)
        
    def update_tick(self, delta_time) -> None:
        self.server.update(loop=True)
        while True:
            try:
                input_bytes = self.server.get_queue.get_nowait()
            except:
                break
            self.decode_input(input_bytes[0], input_bytes[1][1:])

        for player in self.players:
            for player_addr in self.server_addr_id:
                if self.server_addr_id[player_addr] == player.player_id:
                    player.update(self.players_input[player_addr])
                    break

        self.update_players_col(delta_time)
        self.update_skill_player_col(delta_time)
        self.update_skill_col(delta_time)
        for player in self.players:
            player.hitbox.delta_position(delta_time)
            for player_addr in self.server_addr_id:
                if self.server_addr_id[player_addr] == player.player_id:
                    player.skill.update(player.hitbox.position.copy(), player.angle.copy(), self.map)
                    player.sword.update(player.hitbox.position, player.angle, self.players_input[player_addr])
                    break

        self.update_sword_col()
        
        score_increase = self.objectives.update(self.players, delta_time)
        self.score.update(delta_time, self.players, score_increase)

        self.end = self.score.countdown_over

        self.server.send_queue.put(self.encode_game())
    
    def update_client(self) -> None:
        self.client.send_queue.put(self.encode_input())
        self.client.update(loop=True)
        if self.server: return
        while True:
            try:
                game_state = self.client.get_queue.get_nowait()
            except:
                break
            if (chr(game_state[0]) == "g"):
                self.decode_game(game_state[1:])

    def update_frame(self) -> None:
        if (is_key_pressed(KEY_H)):
            self.show_hitboxes = not self.show_hitboxes
            print(f"Hiboxes {self.show_hitboxes}")

        if (is_key_pressed(KEY_ESCAPE)):
            self.end = True
        
    def draw(self) -> None:
        begin_drawing()
        
        clear_background(GRAY)
        self.map.draw        (self.map_offset, self.scaler)
        self.objectives.draw (self.map_offset, self.scaler)
        self.score.draw      (self.scaler)
        for player in self.players:
            player.draw  (self.map_offset, self.scaler, self.show_hitboxes)

        end_drawing()
    
    def unload(self) -> None:
        for player in self.players:
            unload_texture(player.sprite)
        print("Game unloaded")
