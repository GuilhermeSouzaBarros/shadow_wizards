from pyray import *
from raylib import *

from collisions import CollisionInfo
from gamemodes.obj import Objective

class Flag(Objective):
    def __init__(self, tile_size:int, row:int,column:int, radius:float, team:int):
        super().__init__(tile_size, row, column, radius)
        self.taken = False
        self.team = team
  
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
        Função:
            check_taken
        Descrição:
            Verifica se a bandeira foi pega por algum jogador. Se verdadeiro, atualiza o jogador para informar que ele está carregando a bandeira e atualiza o estado da bandeira para que ela não seja mais desenhada no centro do mapa. 
        Parâmetros:
            players: list - lista com todos os jogadores no jogo
        Retorno: 
            Nenhum.
        """
        for player in players:
            if player.team == self.team:
                continue

            info = CollisionInfo.collision(player.hitbox, self.hitbox)
            if info.intersection:
                self.taken = True
                player.has_flag = True
                break


    def update(self, **kwargs) -> list:
        """
        Função:
            update
        Descrição:
            Atualiza a região da bandeira, verifica se ela foi pega por um jogador e desenha a bandeira no centro do mapa se nenhum jogador estiver com ela.
        Parâmetros:
            players: list - uma lista com todos os jogadores do jogo.
        Retorno:
            Retorna uma lista vazia.
        """
        self.check_taken(kwargs['players'])
        if self.taken:
            for player in kwargs['players']:
                if not player.has_flag or player.team == self.team:
                    continue
                self.hitbox.position = player.hitbox.position.copy()
        return []
    
    def draw(self, map_offset:Vector2, scaler:float) -> None:
        """ 
        Função:
            draw
        Descrição:
            Desenha a bandeira no centro do mapa caso nenhum jogador estiver com ela em mãos.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.     
        """
        if self.team == 1:
            color = RED
        elif self.team == 2:
            color = BLUE

        # Calcula a posição da bandeira
        self.hitbox.draw(color, map_offset, scaler)


class CapturePoint(Objective):
    def __init__(self, tile_size:int, row:int, column:int, radius:float, team:int):
        super().__init__(tile_size, row, column, radius, 25)
        self.team = team

    def check_flag_capture(self, players:list, flag:Flag) -> int:
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
        for player in players:
            if not player.has_flag or self.team != player.team:
                continue
            info = CollisionInfo.collision(player.hitbox, self.hitbox)
            if info.intersection:
                print(f"{player.nick} captured the flag!")
                player.has_flag = False
                flag.update_region()
                return player.team
        return 0

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

    def update(self, **kwargs) -> list:
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
        
        for flag in kwargs['flags']:
            if flag.team == self.team:
                continue
            capture = self.check_flag_capture(kwargs['players'], flag)
        if capture == 1:
            return [self.pts_gain, 0]
        elif capture == 2:
            return [0, self.pts_gain]
        return []

    def draw(self, map_offset:Vector2, scaler:float) -> None:
        """ 
        Função: draw
        Descrição:
            Desenha o ponto de captura da equipe.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.     
        """
        if self.team == 1:    
            # Desenha o ponto de captura do time 1 
            color = BLUE
        else:
            # Desenha o ponto de captura do time 2
            color = RED

        # Calcula a posição em que a região de captura deverá ser desenhada.
        pos = [map_offset.x + (self.hitbox.position.x * scaler), map_offset.y + (self.hitbox.position.y * scaler)]
        draw_circle_lines_v(pos, self.hitbox.radius * scaler, color)
