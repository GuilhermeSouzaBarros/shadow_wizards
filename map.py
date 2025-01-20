import json
from pyray import *
from raylib import *

import tiles
from shapes import Rectangle
from vectors import Vector2

class Map:
    def __init__(self, map_id:int) -> None:
        self.tiles = []
        self.collision_hitboxes = []
        self.borders = []

        self.map_id = map_id # Armazena o identificador do mapa
        self.map_info = self.load_map() # Armazena todas as características do mapa

        self.num_rows = self.map_info['height']
        self.num_columns = self.map_info['width']

        self.tile_size = int(self.map_info['tile_size'])

        # Carrega todos os tiles do mapa
        all_tiles = []
        for i in range(0, self.num_rows):
            row = []
            for j in range(0, self.num_columns):
                tile_type = int(self.map_info['tiles'][i][j])
                tile = self.build_tile(tile_type, i, j)
                if tile_type == 3 or tile_type == 4:
                    self.borders.append(tile)
                if (tile.has_collision):
                    all_tiles.append([i, j])
                row.append(tile)
            self.tiles.append(row)

        blocks = []
        before_after = [-1, 1]
        remaining_tiles = all_tiles.copy()
        while remaining_tiles:
            block = [remaining_tiles[0]]
            base_tile = block[0]

            for i in before_after:
                next_tile = [base_tile[0], base_tile[1] + i]
                while next_tile in all_tiles:
                    block.insert(len(block) * (i == 1), next_tile.copy())
                    next_tile[1] += i

            for i in before_after:
                add_row = True
                while add_row:
                    row = []
                    row_number = block[-1 + (i == -1)][0]
                    for tile in block:
                        if tile[0] != row_number:
                            continue
                        tile_above = [tile[0] + i, tile[1]]
                        if not tile_above in all_tiles:
                            add_row = False
                            break
                        row.insert(len(row) * (i == 1), tile_above)
                    if add_row:
                        for tile in row:
                            block.insert(len(block) * (i == 1), tile)

            blocks.append([block[0], block[-1]])
            for tile in block:
                if tile in remaining_tiles:
                    remaining_tiles.remove(tile)

        for block in blocks:
            row = (block[0][0] + block[1][0]) / 2
            column = (block[0][1] + block[1][1]) / 2
            hitbox = Rectangle(
            Vector2(self.tile_size * (column + 0.5),
                    self.tile_size * (row + 0.5)),
            Vector2(self.tile_size * (block[1][1] - block[0][1] + 1),
                    self.tile_size * (block[1][0] - block[0][0] + 1)))
            self.collision_hitboxes.append(hitbox)
    

    def draw(self, map_offset:Vector2, scaler:float, vision:int) -> None:
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
                tile.draw(map_offset, scaler, vision)

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
            with open(f'map/map{self.map_id}.json', 'r') as map_archive:
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
        