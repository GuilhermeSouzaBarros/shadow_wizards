from pyray import *
from raylib import *

from struct import pack, unpack

from config import *
from vectors import Vector2
from shapes import Rectangle
from menu_info.boxes import TextBox
from player import Player

class Score():
    def __init__(self, window_size:list, players:list, num_teams=2):
        self.players = players
        self.objectives_score = [0] * num_teams
        self.kills_score = [0] * num_teams
        self.final_score = [0] * num_teams
        self.num_teams = num_teams
        
        self._font_size = 20
        self.colors = [RED, BLUE, GREEN, GOLD]

        self.time_remaining:float = MATCH_DURATION

        self.background = Rectangle(Vector2(0.2 * window_size[0], 0.2 * window_size[1]), Vector2(0.6 * window_size[0],  0.6 * window_size[1]))
    
    def encode(self) -> bytes:
        message = pack("d", self.time_remaining)
        for score in self.final_score:
            message += score.to_bytes(1)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        pointer = 8
        self.time_remaining = unpack("d", bytes_string[0:8])[0]
        i = 0
        while i < len(self.final_score):
            self.final_score[i] = bytes_string[pointer]
            i += 1
            pointer += 1
        return pointer
    
    @property
    def countdown_over(self) -> bool:
        return self.time_remaining <= 0.0

    def update(self, delta_time:float, players:list, score_increase:list=[]) -> None:
        """
        Função: update
        Descrição:
            Atualiza a pontuação de todos os times no jogo, levando em conta a quantidade de kills do time e a pontuação obtida através dos objetivos.
        Parâmetros:
            players: list - lista com todos os players do jogo;
            score_increase: list - lista com a alteração da pontuação de todos os times após a atualização do estado dos objetivos.
        Retorno:
            Nenhum.
        """
        self.time_remaining -= delta_time

        # Calcula a pontuação obtida através de kills
        for player in players:
            self.kills_score[player.team-1] = player.kills * 5
        
        # Calcula a pontuação obtida através de objetivos do jogo
        for team in range(0, self.num_teams):
            self.objectives_score[team] += score_increase[team % 2]

        # Calcula a pontuação final dos times
        for team in range(0, self.num_teams):
            self.final_score[team] = self.kills_score[team] + self.objectives_score[team]

    def draw_countdown(self, text_pos:Vector2, scaler:float) -> None:
        minutes = int(self.time_remaining / 60)
        seconds = int(self.time_remaining) % 60
        countdown_txt = f"{minutes}:{seconds:02d}"
        draw_text_ex(get_font_default(), countdown_txt, text_pos, self._font_size * scaler, 1.0, RAYWHITE)

    def draw(self, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha o placar do jogo com a pontuação de cada um dos times.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        if not (is_key_down(KEY_TAB)):
            return
        self.background.draw((16, 16, 16, 128))
        text_pos = Vector2(10 * scaler, 0)
        for team in range(1, self.num_teams+1):
            score_txt = f"Team {team}: {self.final_score[team-1]}"
            draw_text_ex(get_font_default(), score_txt, text_pos, self._font_size * scaler, 1.0, self.colors[team-1])
            text_pos.x += 160 * scaler
        

        self.draw_countdown(text_pos, scaler)