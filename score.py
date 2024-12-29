from pyray import *
from raylib import *

class Score():
    def __init__(self, num_teams=2):
        self.objejctives_score = [0] * num_teams
        self.kills_score = [0] * num_teams
        self.final_score = [0] * num_teams
        self.num_teams = num_teams
        
        self._font_size = 20

    def draw(self) -> None:
        """
        Função: draw
        Descrição:
            Desenha a pontuação de todos os times do jogo.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        # Posição inicial do placar
        x_print = 10
        y_print = 10

        for team in range(1, self.num_teams + 1):
            score_txt = f'Team {team}: {self.final_score[team-1]}'
            draw_text(score_txt, x_print, y_print, self._font_size, RAYWHITE)
            
            # Faz com que a pontuação do próximo time seja escrita mais à direita
            x_print += 160  

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
