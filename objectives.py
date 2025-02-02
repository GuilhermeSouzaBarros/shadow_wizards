from pyray import *
from raylib import *

from gamemodes.domination import Domination
from gamemodes.capture_flag import CapturePoint, Flag
from gamemodes.payload import Cart

class Objectives:
    def __init__(self, tile_size:int, map_objectives:dict, map_id:int):
        self.tile_size = tile_size
        self.objectives = {}

        self.map_objectives = map_objectives
        self.map_id = map_id

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

    def update(self, players:list, delta_time:float) -> list:
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
        for objective_type in self.objectives:
            for objective in self.objectives[objective_type]:
                if 'flags' not in self.objectives:
                    final_score_inc = objective.update(players=players, delta_time=delta_time)
                else:
                    final_score_inc = objective.update(players=players, delta_time=delta_time, flags=self.objectives['flags'])
        return final_score_inc

    def draw(self, map_offset:Vector2, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha todos os objetivos da partida.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum:
        """
        for objective_type in self.objectives:
            for objective in self.objectives[objective_type]:
                objective.draw(map_offset, scaler)

    def load_cart(self) -> None:
        # load payload path
        path          = self.map_objectives['cart']['path']
        path_start    = self.map_objectives['cart']['start']
        region_radius = self.map_objectives['cart']['region_radius']

        self.objectives.update({'carts': [Cart(path, path_start, region_radius, self.tile_size)]})

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
        self.objectives.update({'flags': []})
        column = self.map_objectives['flags']['team_1']['column']
        row = self.map_objectives['flags']['team_1']['row']
        radius = self.map_objectives['flags']['team_1']['radius']
        self.objectives['flags'].append(Flag(self.tile_size, row, column, radius, 1))

        column = self.map_objectives['flags']['team_2']['column']
        row = self.map_objectives['flags']['team_2']['row']
        radius = self.map_objectives['flags']['team_2']['radius']
        self.objectives['flags'].append(Flag(self.tile_size, row, column, radius, 2))


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
        self.objectives.update({'capture_points': []})
        # Carrega o ponto de captura do time 1
        column = self.map_objectives['capture_points']['team_1']['column']
        row = self.map_objectives['capture_points']['team_1']['row']
        radius = self.map_objectives['capture_points']['team_1']['radius']
        self.objectives['capture_points'].append(CapturePoint(self.tile_size, row, column, radius, 1))
        
        # Carrega o ponto de captura do time 2
        column = self.map_objectives['capture_points']['team_2']['column']
        row = self.map_objectives['capture_points']['team_2']['row']
        radius = self.map_objectives['capture_points']['team_2']['radius']
        self.objectives['capture_points'].append(CapturePoint(self.tile_size, row, column, radius, 2))

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
        self.objectives.update({'dominations': [Domination(self.tile_size, row, column, radius)]})
        