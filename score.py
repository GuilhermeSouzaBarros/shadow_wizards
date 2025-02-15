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
            TextBox(f"{self.player.character_name}", font, 0.5, WHITE, Vector2(0.125 + size.x * 1/4, position.y), Vector2(0.3 * size.x, size.y), "caracter_name", window_size),
            TextBox(f"{str(self.player.kills).center(5)}/{str(self.player.deaths).center(5)}", font, 0.8, WHITE, Vector2(0.125 + size.x * 3/4, position.y), Vector2(0.3 * size.x, size.y), "player_kd",  window_size),
        ]

    def update(self) -> None:
        self.boxes[1].change_text(f"{str(self.player.kills).center(5)}/{str(self.player.deaths).center(5)}")

    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        for box in self.boxes:
            box.update_scale(window_size)

    def draw(self):
        self.hitbox.draw(color_contrast(color_alpha(self.player.color, 0.5), 0.25), outlines=False)
        for box in self.boxes:
            box.draw()

class TeamInfo(Box):
    def __init__(self, team:list, color:Color, font:Font, position:Vector2, size:Vector2, window_size:Vector2):
        Box.__init__(self, position, size, window_size)
        self.color = color
        self.boxes = []
        num_players = len(team)
        for i, player in enumerate(team):
            self.boxes.append(PlayerInfoBox(player, font, Vector2(0.5, (self.position.y - self.size.y/2) + self.size.y*(0.5+i)/num_players), Vector2(size.x * 0.95, size.y * 0.6 * (1/num_players)), window_size))

    def update(self) -> None:
        for box in self.boxes:
            box.update()

    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        for box in self.boxes:
            box.update_scale(window_size)
    
    def draw(self) -> None:
        self.hitbox.draw(color_alpha(color_brightness(self.color, 0.5), 0.5))
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
        self.team_scores = [0] * self.num_teams
        self.boxes = [
            TextBox("", self.font, 1, WHITE, Vector2(0.25, 0.1625), Vector2(0.125, 0.075), "timer", window_size)
        ]
        
        num_players = len(self.players)
        for team in range(0, self.num_teams):
            self.boxes.append(TextBox("0", self.font, 1, self.team_colors[team], Vector2(0.4 + (self.size.y - 0.4)*(0.5+team)/num_teams, 0.1625),
                                      Vector2((1-0.01625)/num_teams, 0.075), "team_score", window_size))
            team_players = []
            for player in self.players:
                if player.team == team + 1: team_players.append(player)
            if len(team_players):
                self.boxes.append(TeamInfo(team_players, self.team_colors[team], self.font, Vector2(0.5, 0.2 + (self.size.y - 0.075)*(0.5+team)/num_teams), Vector2(0.725, 0.65/num_teams), window_size))
            
        self.time_remaining:float = MATCH_DURATION
    
    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        for player_info in self.boxes:
            player_info.update_scale(window_size)

    def unload(self) -> None:
        unload_font(self.font)

    def encode(self) -> bytes:
        message = pack("d", self.time_remaining)
        for score in self.team_scores:
            message += score.to_bytes(1)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        pointer = 8
        self.update(0, [])
        self.time_remaining = unpack("d", bytes_string[0:8])[0]
        i = 0
        while i < self.num_teams:
            self.team_scores[i] = bytes_string[pointer]
            pointer += 1
            i += 1
        return pointer
    
    @property
    def countdown_over(self) -> bool:
        return self.time_remaining <= 0.0

    def update(self, delta_time:float, score_increase:list) -> None:
        self.time_remaining -= delta_time
        minutes = int(self.time_remaining / 60)
        seconds = int(self.time_remaining) % 60
        self.boxes[0].change_text(f"{minutes}:{seconds:02d}")

        i = 0
        try:
            while i < len(score_increase):
                self.team_scores[i] += score_increase[i]
                i += 1
        except:
            return
        i = 0
        for box in self.boxes:
            if issubclass(box.__class__, TextBox) and box.type == "team_score":
                box.change_text(f"{self.team_scores[i]}")
                i += 1   

        for box in self.boxes:
            box.update()
            
    def draw(self, scaler:float, finish:bool) -> None:
        if not (is_key_down(KEY_TAB) or finish):
            return
        self.hitbox.draw((16, 16, 16, 192))
        for box in self.boxes:
            box.draw()
