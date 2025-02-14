from pyray import *
from raylib import *

from struct import pack, unpack

from utils import sign_of
from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle, Circle
from collisions import CollisionInfo
from math import degrees, atan2

class Cart:
    def __init__(self, path:list, path_start:int, region_radius:int, tile_size:float):
        self.region_radius = region_radius
        self.tile_size = tile_size

        self.sprite = load_texture("sprites/carroForte.png")

        row    = path[path_start][0]
        column = path[path_start][1]
        position = Vector2(tile_size * (column + 0.5), tile_size * (row + 0.5))
        self.hitbox = Rectangle(
                                position,
                                Vector2(tile_size, tile_size),
                                Imaginary())
        self.region = Circle(
                                position.copy(), 
                                tile_size * region_radius)
        
        self.path         = path
        self.path_start   = path_start
        self.current_line = [path_start, path_start + 1]
        self.speed        = 0.75 # in tiles per second, keep it simple
        self.angle = Imaginary(1, 0)
        self.max_point = [path_start, path_start]

        self.color = WHITE
        self.curr_team = 0
        self.end_push  = 0
        self.winning_team = 0
    
    def encode(self) -> bytes:
        return pack("?dddd", self.curr_team, self.hitbox.position.x, self.hitbox.position.y, self.angle.real, self.angle.imaginary)
    
    def decode(self, bytes_string:bytes) -> int:
        data = unpack("?dddd", bytes_string[0:40])
        self.curr_team = data[0]
        position = Vector2(data[1], data[2])
        self.angle = Imaginary(data[3], data[4])
        self.hitbox.position = position
        self.region.position = position.copy()
        self.update_color() 
        return 40

    def update_color(self) -> None:
        if not self.curr_team:
            self.color = WHITE

        elif self.curr_team == 1:
            self.color = RED

        elif self.curr_team == 2:
            self.color = BLUE

    def update(self, players:list, delta_time:float) -> list:
        self.hitbox.speed = Vector2(0, 0)
        self.update_players_col(players, delta_time)
        if self.end_push: return [0, 0]

        self.curr_team = self.check_domination(players)
        self.update_color()
        if not self.curr_team: return [0, 0]

        elif self.curr_team == 1:
            to_point_in_line = 1

        elif self.curr_team == 2:
            to_point_in_line = 0
        
        next_point_pos = Vector2((self.path[self.current_line[to_point_in_line]][1] + 0.5) * self.tile_size,
                                 (self.path[self.current_line[to_point_in_line]][0] + 0.5) * self.tile_size)
        distance = next_point_pos - self.hitbox.position

        delta_pos = self.speed * self.tile_size * delta_time
        
        score = [0, 0]

        if (abs(distance.x) > delta_pos or abs(distance.y) > delta_pos) :
            self.hitbox.speed.x = sign_of(distance.x) * self.speed * self.tile_size
            self.hitbox.speed.y = sign_of(distance.y) * self.speed * self.tile_size
        else:
            self.hitbox.speed.x = distance.x / delta_time
            self.hitbox.speed.y = distance.y / delta_time
            
            next_point = -1 + 2 * to_point_in_line
            self.current_line[0] += next_point
            self.current_line[1] += next_point
            if self.curr_team == 1 and self.current_line[0] > self.max_point[0]:
                self.max_point[0] += 1
                score[0] += 20
            elif self.curr_team == 2 and self.current_line[1] < self.max_point[1]:
                self.max_point[1] -= 1
                score[1] += 20
            if self.current_line[0] == -1 or self.current_line[0] == 11:
                self.end_push = True
        self.angle = Imaginary(self.hitbox.speed.x, self.hitbox.speed.y, 1)
        self.hitbox.delta_position(delta_time)
        self.region.position = self.hitbox.position.copy()

        return score
    
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

    def update_players_col(self, players:list, delta_time:float) -> None:
        for player in players:
            info = CollisionInfo.collision(player.hitbox, self.hitbox, delta_time, calculate_distance=True)
            if info.intersection:
                player.hitbox.position -= info.distance

    def draw(self, map_offset:Vector2, scaler:float, show_hitboxes:bool) -> None:
        self.draw_cart   (map_offset, scaler, show_hitboxes)
        self.draw_region (map_offset, scaler)

    def draw_cart(self, map_offset:Vector2, scaler:float, hitbox:bool) -> None:
        if hitbox:
            self.hitbox.draw(self.color, map_offset, scaler)
        else:
            angle = degrees(atan2(self.angle.imaginary, self.angle.real))
            angle += 360 * (angle < 0.0)
            angle /= 90
            angle = int(angle)

            size_im_x = Imaginary(self.hitbox.size.x/2, 0.0)
            size_im_y = Imaginary(0.0, self.hitbox.size.y/2.0)
            up_left_corner = [self.hitbox.position.x - size_im_x.real - size_im_y.real,
                                self.hitbox.position.y - size_im_x.imaginary - size_im_y.imaginary]
            offset = Vector2(self.hitbox.size.x*0.5, self.hitbox.size.y*0.5)
            pos = [map_offset.x + ((up_left_corner[0] + 15)*scaler), 
                    map_offset.y + ((up_left_corner[1] + 32)*scaler)]
            rectangle_dest = [round(pos[0]), round(pos[1]),
                            round(scaler*self.hitbox.size.x),
                            round(scaler*self.hitbox.size.y)]
            draw_texture_pro(self.sprite, [0, angle*32, 32, 32], rectangle_dest, 
                                [round(offset.x*scaler), round(2*offset.y*scaler)], 0, WHITE)
        

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
    
    def unload(self):
        pass