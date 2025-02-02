from pyray import *
from raylib import *

from utils import sign_of
from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle, Circle
from collisions import CollisionInfo

class Cart:
    def __init__(self, path:list, path_start:int, region_radius:int, tile_size:float):
        self.region_radius = region_radius
        self.tile_size = tile_size

        row    = path[path_start][0]
        column = path[path_start][1]
        self.hitbox = Rectangle(
                            Vector2(tile_size * (column + 0.5),
                                    tile_size * (row + 0.5)),
                                    Vector2(tile_size, tile_size),
                                    Imaginary())
        self.region = Circle(
                            Vector2(tile_size * (column + 0.5), 
                                    tile_size * (row + 0.5)), 
                                    tile_size * region_radius)
        
        self.path         = path
        self.path_start   = path_start
        self.current_line = [path_start, path_start + 1]
        self.speed        = 0.5 # in tiles per second, keep it simple

        self.color = WHITE
        self.curr_team = 0
        self.end_push  = 0
        self.winning_team = 0
    
    def update(self, players:list, delta_time:float) -> list:
        self.hitbox.speed = Vector2(0, 0)
        self.update_players_col(players, delta_time)
        if self.end_push:
            return [0, 0]
        team_push = self.check_domination(players)
        if self.curr_team != team_push:
            print(f"Current team pushing: {team_push}\n")
            self.curr_team = team_push

        if not team_push:
            self.color = WHITE
            return [0, 0]

        elif team_push == 1:
            self.color = RED
            to_point_in_line = 1

        elif team_push == 2:
            self.color = BLUE
            to_point_in_line = 0
        
        next_point_pos = Vector2((self.path[self.current_line[to_point_in_line]][1] + 0.5) * self.tile_size,
                                 (self.path[self.current_line[to_point_in_line]][0] + 0.5) * self.tile_size)
        distance = next_point_pos - self.hitbox.position

        delta_pos = self.speed * self.tile_size * delta_time
        
        final_result = [0, 0]

        if (abs(distance.x) > delta_pos or abs(distance.y) > delta_pos) :
            self.hitbox.speed.x = sign_of(distance.x) * self.speed * self.tile_size
            self.hitbox.speed.y = sign_of(distance.y) * self.speed * self.tile_size
        else:
            self.hitbox.speed.x = distance.x / delta_time
            self.hitbox.speed.y = distance.y / delta_time
            
            next_point = -1 + 2 * to_point_in_line
            self.current_line[0] += next_point
            self.current_line[1] += next_point

            if self.current_line[0] == -1 or self.current_line[1] == len(self.path):
                self.end_push = 1
                self.winning_team = self.curr_team
                print(f"Push ended, team {self.curr_team} won")
                final_result[self.curr_team-1] = 100
    
        self.hitbox.delta_position(delta_time)
        self.region.position = self.hitbox.position.copy()
        

        return final_result
    
    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região do carrinho.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        self.region = Circle(self.rectangle.position, self.region_radius)

    # *** Função redundante, usar só para testes ***
    def rec_circle_intersection(self, player:Circle):
        # Retorna o quanto o player está penetrando o retângulo e o ponto do retângulo em que ocorre a colisão. Caso não tenha penetração, não retorna nenhum ponto de colisão.
        
        # Encontra o ponto mais próximo no retângulo ao centro do círculo
        closest_x = max((self.hitbox.position.x - self.tile_size/2), min(player.position.x, (self.hitbox.position.x - self.tile_size/2) + self.hitbox.size.x))
        closest_y = max((self.hitbox.position.y - self.tile_size/2), min(player.position.y, (self.hitbox.position.y - self.tile_size/2) + self.hitbox.size.y))
        
        distance = Vector2(player.position.x - closest_x, player.position.y - closest_y)
        
        distance = distance.module()

        # Se a distância for menor que o raio, o player está colidindo com o retângulo
        if distance < player.radius:
            penetration = player.radius - distance
            return penetration, Vector2(closest_x, closest_y)
        return 0, None

    def update_players_col(self, players:list, delta_time:float) -> None:
        for player in players:
            penetration, collision_point = self.rec_circle_intersection(player.hitbox)

            # info = CollisionInfo.collision(self.hitbox, player.hitbox, delta_time, calculate_distance=True)

            if penetration:
                repulsion_dir = Vector2(player.hitbox.position.x - collision_point.x, player.hitbox.position.y - collision_point.y)
                repulsion_length = repulsion_dir.module()
                repulsion_dir = repulsion_dir / repulsion_length
                
                player.hitbox.position += (repulsion_dir * penetration)

    def draw(self, map_offset:Vector2, scaler:float) -> None:
        self.draw_cart   (map_offset, scaler)
        self.draw_region (map_offset, scaler)

    def draw_cart(self, map_offset:Vector2, scaler:float) -> None:
        self.hitbox.draw(self.color, map_offset, scaler)

    def draw_region(self, map_offset:Vector2, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha a região de movimentação do carrinho de acordo com o time que estiver movimentando o carrinho.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        pos = [map_offset.x + (self.region.position.x * scaler),
               map_offset.y + (self.region.position.y * scaler)]
        draw_circle_lines_v(pos, self.region.radius * scaler, self.color)
            

    def check_domination(self, players:list) -> int:
        """
        Função: check_domination
        Descrição:
            Verifica se o carrinho está sendo movimentado por algum time.
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno: 
            0, quando nenhum time estiver movimentando o carrinho;
            1, quando o time 1 estiver movimentando o carrinho;
            2, quando o time 2 estiver movimentando o carrinho.
        """
        teams_inside = []
        for player in players:
            if not player.is_alive:
                continue
            info = CollisionInfo.collision(player.hitbox, self.region)            
            if info.intersection:
                if not (player.team in teams_inside):
                    teams_inside.append(player.team)

        if len(teams_inside) == 1:
            return teams_inside[0]
        return 0