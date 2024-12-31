from pyray import *
from raylib import *

class Score():
    def __init__(self, num_teams=2):
        self.objejctives_score = [0] * num_teams
        self.kills_score = [0] * num_teams
        self.final_score = [0] * num_teams
        self.num_teams = num_teams
        
        self._font_size = 20
        self.colors = [RED, BLUE, GREEN, GOLD]

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
        self.draw_score(scaler) 

    def draw_score(self, scaler:float) -> None:
        """
        Função: draw_score
        Descrição:
            Desenha a pontuação de cada um dos times.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        text_pos = Vector2(10 * scaler, 0)
        for team in range(1, self.num_teams+1):
            score_txt = f"Team {team}: {self.final_score[team-1]}"
            draw_text_ex(get_font_default(), score_txt, text_pos, self._font_size * scaler, 1.0, self.colors[team-1])
            text_pos.x += 160 * scaler

    def countdown(self) -> None:
        pass

    def update(self, players:list, score_increase:list=[]) -> None:
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
        # Calcula a pontuação obtida através de kills
        for player in players:
            self.kills_score[player.team-1] = player.kills * 5
        
        # Calcula a pontuação obtida através de objetivos do jogo
        for team in range(0, len(score_increase)):
            self.objejctives_score[team] += score_increase[team]
        
        # Calcula a pontuação dinal dos times
        for team in range(0, self.num_teams):
            self.final_score[team] = self.kills_score[team] + self.objejctives_score[team]
