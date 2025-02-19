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
        self.load()

    def encode(self) -> bytes:
        message = "".encode()
        for objectives in self.objectives:
            for objective in self.objectives[objectives]:
                message += objective.encode()
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        pointer = 0
        for objectives in self.objectives:
            for objective in self.objectives[objectives]:
                pointer += objective.decode(bytes_string[pointer:])
        return pointer

    def load(self) -> None:
        # Carrega os objetivos do mapa de acordo com o seu ID
        if self.map_id == 2:
            self.load_cart() 
        elif self.map_id == 3:
            self.load_flags()            
            self.load_capture_points()
        elif self.map_id == 4:
            self.load_domination()

    def update(self, players:list, delta_time:float) -> list:
        final_score_inc = [0, 0]
        for objective_type in self.objectives:
            for objective in self.objectives[objective_type]:
                if 'flags' in self.objectives:
                    score_increase = objective.update(players, delta_time, flags=self.objectives['flags'] )
                else:
                    score_increase = objective.update(players, delta_time)
                i = 0
                while i < len(score_increase):
                    final_score_inc[i] += score_increase[i]
                    i += 1
        return final_score_inc

    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool=False) -> None:
        for objective_type in self.objectives:
            for objective in self.objectives[objective_type]:
                objective.draw(map_offset, scaler, show_hitboxes)

    def unload(self):
        for objective_type in self.objectives:
            for objective in self.objectives[objective_type]:
                objective.unload()

    def load_cart(self) -> None:
        # Carrega o caminho do carrinho
        path          = self.map_objectives['cart']['path']
        path_start    = self.map_objectives['cart']['start']
        region_radius = self.map_objectives['cart']['region_radius']

        self.objectives.update({'carts': [Cart(path, path_start, region_radius, self.tile_size)]})

    def load_flags(self) -> None:
        # Carrega a bandeira do time 1
        self.objectives.update({'flags': []})
        column = self.map_objectives['flags']['team_1']['column']
        row = self.map_objectives['flags']['team_1']['row']
        radius = self.map_objectives['flags']['team_1']['radius']
        self.objectives['flags'].append(Flag(self.tile_size, row, column, radius, 1))

        # Carrega a bandeira do time 2
        column = self.map_objectives['flags']['team_2']['column']
        row = self.map_objectives['flags']['team_2']['row']
        radius = self.map_objectives['flags']['team_2']['radius']
        self.objectives['flags'].append(Flag(self.tile_size, row, column, radius, 2))

    def load_capture_points(self) -> None:
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
        column = self.map_objectives['zone']['column']
        row = self.map_objectives['zone']['row']
        radius = self.map_objectives['zone']['radius']
        self.objectives.update({'dominations': [Domination(self.tile_size, row, column, radius)]})
        