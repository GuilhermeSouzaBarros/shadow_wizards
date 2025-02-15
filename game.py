from pyray import *
from raylib import *

from sockets.server import Server
from sockets.client import Client

from config import GAME_TICK
from vectors import Vector2
from collisions import CollisionInfo
from player import Player
from map import Map
from objectives import Objectives
from score import Score
from shapes import ColCircleLine
from sounds import Music

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
        self.map = Map(map_id)
        self.players = []
        for player_id in characters_id:
            self.players.append(Player(self.map.tile_size,
                                self.map.map_info['spawn_points'][f'player_{player_id}'][0],
                                self.map.map_info['spawn_points'][f'player_{player_id}'][1],
                                self.map.map_info['spawn_points'][f'player_{player_id}'][2],
                                player_id, characters_id[player_id], map_id, f"player {player_id}"))
        self.num_teams = len(self.players) if map_id == 1 else 2
        self.objectives = Objectives(self.map.tile_size, self.map.map_info['objectives'], map_id)
        self.score = Score(window_size, self.players, self.num_teams)
        self.map_offset = None
        self.scaler = None
        self.show_hitboxes = False
        self.finish = False
        self.end = False

        # lista de habilidades que afetam outros players
        self.active_skills = ["Fireball", "Gun", "Trap"]

        self.music = Music()

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
        self.score.update_scale(Vector2(window_size[0], window_size[1]))

    def encode_input(self) -> bytes:
        message = "i".encode()
        keys = [[KEY_UP, KEY_W], [KEY_LEFT, KEY_A], [KEY_DOWN, KEY_S], [KEY_RIGHT, KEY_D], [KEY_X, KEY_L], [KEY_C, KEY_K]]
        for key in keys:
            message += (is_key_down(key[0]) or is_key_down(key[1])).to_bytes(1)
        return message

    def decode_input(self, player:tuple, input:bytes) -> None:
        for i, key in enumerate(self.players_input[player]):
            self.players_input[player][key] = bool(input[i])

    def encode_game(self) -> bytes:
        message = "g".encode()
        for player in self.players:
            message += player.encode()
        message += self.objectives.encode()
        message += self.score.encode()
        message += self.finish.to_bytes(1)
        return message

    def decode_game(self, game:bytes) -> None:
        pointer = 0
        for player in self.players:
            pointer += player.decode(game[pointer:])
        pointer += self.objectives.decode(game[pointer:])
        pointer += self.score.decode(game[pointer:])
        self.finish = game[pointer]

    def update_players_col(self, delta_time:float) -> None:
        for player in self.players:  
            tiles = self.map.team_collision_tiles[player.team - 1]
            if (player.skill_name == "Intangibility" and player.skill.is_activated):
                tiles = self.map.team_border_tiles[player.team - 1]
            
            for tile in tiles:
                info = CollisionInfo.collision(player.hitbox, tile, delta_time, calculate_distance=True)
                if info.intersection:
                    player.hitbox.speed -= info.distance / delta_time

    def update_sword_col(self) -> None:
        for player_a in self.players:
            if not (player_a.is_alive and player_a.sword.active):
                continue

            for player_b in self.players:
                if player_a == player_b or not player_b.is_alive or player_a.team == player_b.team:
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
                if player_a == player_b or player_a.team == player_b.team or not player_b.is_alive:
                    continue

                if player_b.skill_name == "Shield" and player_b.skill.is_activated:
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
                        if info.intersection and hitbox.is_activated:
                            if skill_name == "Traps":
                                play_sound(player_a.skill.sound)
                            player_a.killed()
                            player_b.died()
                            hitbox.deactivate()
                            player_a.skill.number_of_activated -= 1
                            
                    else:
                        if not player_a.skill.is_activated:
                            continue
                        info = ColCircleLine(player_b.hitbox, hitbox, delta_time)
                        if info.did_intersect and player_b.is_alive:
                            player_a.killed()
                            player_b.died()
                            player_a.skill.apply_effect(hitbox)
                    
    def update_skill_col(self, delta_time:float) -> None:    
        for player in self.players:
            for tile in self.map.team_collision_tiles[player.team - 1]:
                if not (player.skill_name in ["Gun", "Fireball"]):
                    continue
                for projectile in player.skill.hitboxes:
                    info = CollisionInfo.collision(projectile.hitbox, tile, delta_time, calculate_distance=True)
                    if info.intersection and projectile.is_activated:
                        projectile.deactivate()
                        player.skill.number_of_activated -= 1
    
    def server_receive_input(self) -> None:
        if self.finish:
            return
        self.server.update(loop=True)
        while True:
            try:
                input_bytes = self.server.get_queue.get_nowait()
            except:
                break
            if input_bytes[0] in self.server.clients_addresses:
                self.decode_input(input_bytes[0], input_bytes[1][1:])

        for player in self.players:
            for player_addr in self.server_addr_id:
                if self.server_addr_id[player_addr] == player.player_id:
                    player.update(self.players_input[player_addr])
                    break

    def update_tick(self, delta_time) -> None:
        self.tick -= GAME_TICK
        self.server_receive_input()

        self.update_players_col(delta_time)
        self.update_skill_player_col(delta_time)
        self.update_skill_col(delta_time)
        for player in self.players:
            player.hitbox.delta_position(delta_time)
            if (player.hitbox.position.x <= 0 or player.hitbox.position.y <= 0 or
                player.hitbox.position.x >= 25 * 32 or player.hitbox.position.y >= 15 * 32):
                #Fail safe if player gets out of map
                player.hitbox.position = player.start_pos.copy()
                player.angle           = player.start_angle.copy()

            for player_addr in self.server_addr_id:
                if self.server_addr_id[player_addr] == player.player_id:
                    if player.is_alive:
                        player.skill.update(player.hitbox.position.copy(), player.angle.copy(), self.players_input[player_addr], self.map, player.team)
                        player.sword.update(player.hitbox.position, player.angle, self.players_input[player_addr])
                    break

        self.update_sword_col()
        
        score_increase = self.objectives.update(self.players, delta_time)
        self.score.update(delta_time, score_increase)
        self.finish = self.score.countdown_over or (100 in self.score.team_scores)

        self.server.send_queue.put(self.encode_game())
    
    def update_client(self) -> None:
        self.client.send_queue.put(self.encode_input())
        self.client.update(loop=True)
        if self.server: return
        while True:
            try:
                game_state = self.client.get_queue.get_nowait()
                self.decode_game(game_state[1:])
            except:
                break

    def update_frame(self) -> None:
        self.music.update()
        if (is_key_pressed(KEY_H)):
            self.show_hitboxes = not self.show_hitboxes
            print(f"Hiboxes {self.show_hitboxes}")

        skill_frames = ["Traps", "Fireball"]
        for player in self.players:
            if player.skill_name not in skill_frames:
                return
            for hitbox in player.skill.hitboxes:
                hitbox.update_time()

        if (is_key_pressed(KEY_ESCAPE) and self.finish):
            if self.server:
                self.server.process_get.kill()
                self.server.process_send.kill()
            if self.client:
                self.client.process_get.kill()
                self.client.process_send.kill()
            self.end = True

    def draw(self) -> None:
        begin_drawing()
        
        clear_background(BLACK)
        if not self.finish:
            self.map.draw        (self.map_offset, self.scaler, self.show_hitboxes)
            self.objectives.draw (self.map_offset, self.scaler, self.show_hitboxes)
            for player in self.players:
                player.draw  (self.map_offset, self.scaler, self.show_hitboxes)
        self.score.draw      (self.scaler, self.finish)

        end_drawing()
    
    def unload(self) -> None:
        for player in self.players:
            unload_texture(player.sprite)
            unload_texture(player.sword.sprite)
            unload_sound(player.sword.sound)

            skill_sounds = ["Fireball", "Traps", "Gun", "Laser"]
            if(player.skill_name in skill_sounds):
                unload_sound(player.skill.sound)

            skill_sprites = ["Fireball", "Traps", "Gun", "Shield"]
            if(player.skill_name in skill_sprites):
                unload_texture(player.skill.sprite)
        if self.server:
            self.server.close()
        if self.client:
            self.client.close()
        unload_texture(self.map.map_sprite.texture)
        self.objectives.unload()
        self.music.unload()
        self.score.unload()
        print("Game unloaded")
