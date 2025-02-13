from pyray import *
from raylib import *

from struct import pack, unpack

from config import *
from vectors import Vector2
from shapes import Rectangle
from menu_info.boxes import Box, TextBox
from player import Player

class PlayerInfoBox(Box):
    def __init__(self, player:Player, font:Font, position:Vector2, size:Vector2, window_size:Vector2):
        Box.__init__(self, position, size, window_size)
        self.player = player
        self.boxes = [
            TextBox(f"{self.player.character_name}", font, 0.8, WHITE, Vector2(0.125 + size.x * 1/6, position.y), Vector2(0.3 * size.x, size.y), "caracter_name", window_size),
            TextBox(f"{self.player.kills}",          font, 0.8, WHITE, Vector2(0.125 + size.x * 3/6, position.y), Vector2(0.3 * size.x, size.y), "player_kills",  window_size),
            TextBox(f"{self.player.deaths}",         font, 0.8, WHITE, Vector2(0.125 + size.x * 5/6, position.y), Vector2(0.3 * size.x, size.y), "player_deaths", window_size),
        ]

    def update(self) -> None:
        self.boxes[1].change_text(f"{self.player.kills}")
        self.boxes[2].change_text(f"{self.player.deaths}")

    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        for box in self.boxes:
            box.update_scale(window_size)

    def draw(self):
        self.hitbox.draw(color_alpha(self.player.color, 0.5), outlines=False)
        for box in self.boxes:
            box.draw()

class Score(Box):
    def __init__(self, window_size:list, players:list, num_teams:int=2):
        window_size = Vector2(window_size[0], window_size[1])
        Box.__init__(self, Vector2(0.5, 0.5), Vector2(0.75, 0.75), window_size)
        self.font = load_font_ex("fonts/PixAntiqua.ttf", 32, None, 250)
        self.players = players
        self.num_teams = num_teams
        self.team_colors = [RED, BLUE, GREEN, GOLD]
        self.boxes = []
        num_players = len(self.players)
        for i, player in enumerate(self.players):
            self.boxes.append(PlayerInfoBox(player, self.font, Vector2(0.5, 0.125 + 0.75 * (0.5+i)/num_players), Vector2(0.75, 0.75/num_players), window_size))
        
        self.time_remaining:float = MATCH_DURATION
    
    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        for player_info in self.boxes:
            player_info.update_scale(window_size)

    def unload(self) -> None:
        unload_font(self.font)

    def encode(self) -> bytes:
        message = pack("d", self.time_remaining)
        #for score in self.final_score:
        #    message += score.to_bytes(1)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        pointer = 8
        self.update(0)
        self.time_remaining = unpack("d", bytes_string[0:8])[0]
        return pointer
    
    @property
    def countdown_over(self) -> bool:
        return self.time_remaining <= 0.0

    def update(self, delta_time:float) -> None:
        self.time_remaining -= delta_time
        for box in self.boxes:
            box.update()

    def draw_countdown(self, text_pos:Vector2, scaler:float) -> None:
        minutes = int(self.time_remaining / 60)
        seconds = int(self.time_remaining) % 60
        countdown_txt = f"{minutes}:{seconds:02d}"
        draw_text_ex(get_font_default(), countdown_txt, text_pos.to_list(), 10 * scaler, 1.0, RAYWHITE)

    def draw(self, scaler:float) -> None:
        if not (is_key_down(KEY_TAB)):
            return
        self.hitbox.draw((16, 16, 16, 128))
        text_pos = Vector2(10 * scaler, 0)
        for player_info in self.boxes:
            player_info.draw()

        self.draw_countdown(text_pos, scaler)