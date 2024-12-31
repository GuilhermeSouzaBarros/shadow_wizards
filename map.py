import json
from pyray import *
from raylib import *

import tiles
from vectors import Vector2

class Map:
    def __init__(self, map_id:int) -> None:
        self.tiles     = []

        self.map_id = map_id # Armazena o identificador do mapa
        self.map_info = self.load_map() # Armazena todas as características do mapa

        self.num_rows = self.map_info['height']
        self.num_columns = self.map_info['width']

        self.tile_size = int(self.map_info['tile_size'])

        # Carrega todos os tiles do mapa
        for i in range(0, self.num_rows):
            row = []
            for j in range(0, self.num_columns):
                tile_type = int(self.map_info['tiles'][i][j])
                tile = self.build_tile(tile_type, i, j)
                row.append(tile)
            self.tiles.append(row)
    
    def draw(self, map_offset:Vector2, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha o mapa do jogo.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        # Itera sobre todos os tiles do mapa
        for row in range(0, self.num_rows):
            for column in range(0, self.num_columns):
                tile = self.tiles[row][column]
                tile.draw(map_offset, scaler)

    def load_map(self) -> dict:
        """ 
        Função: load_map
        Descrição: 
            Carrega e retorna um dicionário com as características do mapa.
        Parâmetros:
            Nenhum.
        Retorno:
            Mapa.
        """
        map = None
        try:
            if self.map_id == 1:
                with open('map/map1.json', 'r') as map_archive:
                    map = json.load(map_archive)
            if self.map_id == 2:
                with open('map/map2.json', 'r') as map_archive:
                    map = json.load(map_archive)
            if self.map_id == 3:
                with open('map/map3.json', 'r') as map_archive:
                    map = json.load(map_archive)
            if self.map_id == 4:
                with open('map/map4.json', 'r') as map_archive:
                    map = json.load(map_archive)
        except FileNotFoundError:
            print("Erro: Arquivo não encontrado.")
        except json.JSONDecodeError:
            print("Erro: Arquivo não contém um JSON válido.")   
        
        return map
    
    def build_tile(self, tile_type: int, row: int, column:int):
        """ 
        Função: build_tile
        Descrição:
            Cria e retorna o tile correspondente da posição no mapa.
        Parâmetros:
            tile_type: int - id do tipo do tile
            row: int - linha em que está o tile
            column: int - coluna em que está o tile 
        Retorno:
            Tile correspondente ao id fornecido.
        """
        if not tile_type or tile_type == 6:
            return tiles.Floor(self.tile_size, tile_type, row, column)
        elif tile_type == 1 or tile_type == 2:
            return tiles.Barrier(self.tile_size, tile_type, row, column)
        elif tile_type == 3 or tile_type == 4:
            return tiles.Border(self.tile_size, tile_type, row, column)
        elif not tile_type % 5:
            return tiles.SpawnPoint(self.tile_size, tile_type, row, column)
        elif tile_type == 7 or tile_type == 8:
            return tiles.Rails(self.tile_size, tile_type, row, column)
        