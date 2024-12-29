from pyray import *
from raylib import *

from collisions import ColCircleCircle
from gamemodes.obj import Objective

class CapturePoint(Objective):
    def __init__(self, tile_size:int, map_pos:Vector2, row:int, column:int, radius:float, team:int, scaler:float=0.0):
        super().__init__(tile_size, map_pos, row, column, radius, scaler, 25)
        self.team = team

    def check_flag_capture(self, players:list) -> int:
        """ 
        Função: check_flag_capture
        Descrição: 
            Verifica se a bandeira foi capturada por algum time.
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno:
            0, quando a bandeira não foi capturada por nenhum jogador;
            1, quando a bandeira foi capturada pelo time 1;
            2, quando a bandeira foi capturada pelo time 2.
        """
        collision_check = ColCircleCircle()
        for player in players:
            if player.has_flag and self.team == player.team:
                collision = collision_check.check_collision(player.hitbox, self.region, self.scaler)
                if collision:
                    player.has_flag = False
                    return player.team
        return 0

    def draw(self) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha o ponto de captura da equipe.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.     
        """
        # Calcula a posição em que a região de captura deverá ser desenhada.
        pos = [self.map_pos.x + (self.region.position.x * self.scaler), self.map_pos.y + (self.region.position.y * self.scaler)]
        if self.team == 1:    
            # Desenha o ponto de captura do time 1 
            draw_circle_lines_v(pos, self.region.radius * self.scaler, BLUE)
        else:
            # Desenha o ponto de captura do time 2
            draw_circle_lines_v(pos, self.region.radius * self.scaler, RED)

    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região de captura de bandeira.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        super().update_region()

    def update(self, players:list) -> list:
        """
        Função: update
        Descrição:
            Atualiza a região de captura do time, desenha a região de captura e verifica se o time devolveu uma bandeira para a região de captura.
        Parâmetros:
            players: list - uma lista com todos os jogadores do jogo.
        Retorno:
            Retorna uma lista com o acréscimo de pontos de cada time após a verificação.
        """
        self.update_region()
        
        capture = self.check_flag_capture(players)
        if capture == 1:
            return [self.pts_gain, 0]
        elif capture == 2:
            return [0, self.pts_gain]
        return []

class Flag(Objective):
    def __init__(self, tile_size:int, map_pos:Vector2, row:int,column:int, radius:float, team:int, scaler:float=0.0):
        super().__init__(tile_size, map_pos, row, column, radius, scaler)
        self.taken = False
        self.team = team

    def draw(self) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha a bandeira no centro do mapa caso nenhum jogador estiver com ela em mãos.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.     
        """
        # Calcula a posição da bandeira
        pos = [self.map_pos.x + (self.region.position.x * self.scaler), self.map_pos.y + (self.region.position.y * self.scaler)]
        if not self.taken:
            # Desenha a bandeira no centro do mapa se nenhum jogador estiver com ela em mãos
            if self.team == 1:
                draw_circle_v(pos, self.region.radius * self.scaler, BLUE)
            elif self.team == 2:
                draw_circle_v(pos, self.region.radius * self.scaler, RED)       

    def update_region(self) -> None:
        """
        Função: update_region
        Descrição:
            Atualiza a região da bandeira.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum
        """
        super().update_region()

    def check_taken(self, players: list) -> None:
        """
        Função: check_taken
        Descrição:
            Verifica se a bandeira foi pega por algum jogador. Se verdadeiro, atualiza o jogador para informar que ele está carregando a bandeira e atualiza o estado da bandeira para que ela não seja mais desenhada no centro do mapa. 
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno: 
            Nenhum.
        """
        collision_check = ColCircleCircle()
        for player in players:
            if player.team != self.team:
                has_collision = collision_check.check_collision(player.hitbox, self.region, self.scaler)

                if has_collision:
                    self.taken = True
                    player.has_flag = True
                    break
        for player in players:
            if player.has_flag and player.team != self.team:
                return
        self.taken = False

    def update(self, players: list) -> list:
        """
        Função: update
        Descrição:
            Atualiza a região da bandeira, verifica se ela foi pega por um jogador e desenha a bandeira no centro do mapa se nenhum jogador estiver com ela.
        Parâmetros:
            players: list - uma lista com todos os jogadores do jogo.
        Retorno:
            Retorna uma lista vazia.
        """
        self.update_region()
        self.check_taken(players)
        self.draw()
        return []