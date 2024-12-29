from pyray import *
from raylib import *

from gamemodes.domination import Domination
from gamemodes.capture_flag import CapturePoint, Flag
from gamemodes.payload import Cart

class Objectives:
    def __init__(self, map_objectives:dict, map_id:int, draw_size:Vector2, tile_size:float, map_pos:Vector2, scaler:float=0.0):
        self.objectives = []
        self.scaler = scaler

        self.draw_size = draw_size
        self.map_objectives = map_objectives
        self.map_id = map_id
        self.tile_size = tile_size
        self.map_pos = map_pos

    def load(self) -> None:
        """
        Função: load
        Descrição:
            Carrega todos os objetivos de acordo com o modo de jogo determinado pelo map_id.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        if self.map_id == 2:
            self.load_cart() 
        elif self.map_id == 3:
            self.load_flags()            
            self.load_capture_points()
        elif self.map_id == 4:
            self.load_domination()

    def draw(self) -> None:
        """
        Função: draw
        Descrição:
            Desenha todos os objetivos da partida.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum:
        """
        for objective in self.objectives:
            objective.draw()

    def update(self, players:list) -> list:
        """
        Função: update
        Descrição:
            Atualiza a região dos objetivos, calcula e retorna o incremento da pontuação de cada time.
        Parâmetros:
            players: list - uma lista com todos os jogadores da partida
        Retorno:
            Uma lista com o incremento da pontuação de cada time.
        """
        final_score_inc = [0, 0]
        for objective in self.objectives:
            objective.scaler = self.scaler
            score_inc = objective.update(players)
            
            for team_idx in range(0, len(score_inc)):
                final_score_inc[team_idx] += score_inc[team_idx] 
        return final_score_inc

    def load_cart(self) -> None:
        # *** CORRIGIR ***
        
        # Carrega o carrinho
        path = self.map_objectives['cart']['path']
        row = self.map_objectives['cart']['start']['row']
        column = self.map_objectives['cart']['start']['column']
        path_idx = self.map_objectives['cart']['start']['path_idx']
        region_radius = self.map_objectives['cart']['region_radius']

        self.objectives.append(Cart(path, path_idx, region_radius, self.draw_size, self.tile_size, self.map_pos, row, column, self.scaler))

    def load_flags(self) -> None:
        """
        Função: load_flag
        Descrição:
            Carrega a bandeira e a adiciona à lista de objetivos.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        column = self.map_objectives['flags']['team_1']['column']
        row = self.map_objectives['flags']['team_1']['row']
        radius = self.map_objectives['flags']['team_1']['radius']
        self.objectives.append(Flag(self.tile_size, self.map_pos, row, column, radius, 1, self.scaler))

        column = self.map_objectives['flags']['team_2']['column']
        row = self.map_objectives['flags']['team_2']['row']
        radius = self.map_objectives['flags']['team_2']['radius']
        self.objectives.append(Flag(self.tile_size, self.map_pos, row, column, radius, 2, self.scaler))


    def load_capture_points(self) -> None:
        """
        Função: load_capture_points
        Descrição:
            Carrega a área de captura de ambos os times e as adiciona à lista de objetivos.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        # Carrega o ponto de captura do time 1
        column = self.map_objectives['capture_points']['team_1']['column']
        row = self.map_objectives['capture_points']['team_1']['row']
        radius = self.map_objectives['capture_points']['team_1']['radius']
        self.objectives.append(CapturePoint(self.tile_size, self.map_pos, row, column, radius, 1, self.scaler))
        
        # Carrega o ponto de captura do time 2
        column = self.map_objectives['capture_points']['team_2']['column']
        row = self.map_objectives['capture_points']['team_2']['row']
        radius = self.map_objectives['capture_points']['team_2']['radius']
        self.objectives.append(CapturePoint(self.tile_size, self.map_pos, row, column, radius, 2, self.scaler))

    def load_domination(self) -> None:
        """
        Função: load_domination
        Descrição:
            Carrega a área de dominação e a adiciona à lista de objetivos.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        column = self.map_objectives['zone']['column']
        row = self.map_objectives['zone']['row']
        radius = self.map_objectives['zone']['radius']
        self.objectives.append(Domination(self.tile_size, self.map_pos, row, column, radius))

        