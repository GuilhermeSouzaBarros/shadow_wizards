from pyray import *
from raylib import *

from config import Config
from homescreen.hsselectors import MapSelector,SkinSelector
from homescreen.hsbutton import Button

class HomeScreen:
    def __init__(self, window_size:list):    
        self.map_selector = MapSelector()
        self.skin_selector = SkinSelector()
        
        play_button_pos = Vector2(290, 500)
        play_button_size = Vector2(220, 75)
        play_button_text = "Play"
        
        self.play_button = Button(play_button_pos, play_button_size, GREEN, DARKGREEN, play_button_text)

        self.window_size = window_size
        self.scaler = 0.0

    def draw(self) -> None:
        """
        Função: draw
        Descrição:
            Desenha a tela inicial do jogo.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        self.map_selector.draw(self.scaler)
        self.skin_selector.draw(self.scaler)
        self.play_button.draw(self.scaler)
        self.draw_game_name()

    def draw_game_name(self) -> None:
        """
        Função: draw_game_name
        Descrição:
            Desenha na tela o nome do jogo.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        text_size = measure_text_ex(get_font_default(), Config.GAME_TITLE, 100.0 * self.scaler, 1.0)
        text_pos = Vector2((Config.BASE_WIDTH * self.scaler - text_size.x)/2, 0)
        spacing = 5.0

        draw_text_ex(get_font_default(), Config.GAME_TITLE, text_pos, 100.0 * self.scaler, spacing, RED)

    def update(self) -> bool:
        """
        Função: update
        Descrição:
            Atualiza os seletores de mapa e skin, além de verificar se o botão de jogar foi pressionado ou não.
        Parâmetros:
            Nenhum.
        Retorno:
            True, quando o botão de jogar for pressionado;
            False, enquanto o botão de jogar não for pressionado.
        """
        self.map_selector.update(self.scaler)
        self.skin_selector.update(self.scaler)
        self.play_button.update_scale(self.scaler)

        return self.play_button.update()

    def update_scale(self, window_size:list) -> None:
        """
        Função: update_scale
        Descrição:
            Atualiza a escala da janela de acordo com o tamanho da janela.
        Parâmetros:
            window_size: list - tamanho atual da janela.
        Retorno:
            Nenhum.
        """
        self.window_size = window_size
        new_scaler = min(self.window_size[0] / Config.BASE_WIDTH, self.window_size[1] / Config.BASE_HEIGHT)
        self.scaler = new_scaler        

    @property
    def selected_map(self) -> int:
        return self.map_selector.options[self.map_selector.current-1][0]

    @property
    def selected_skin(self) -> int:
        return self.skin_selector.skin_color