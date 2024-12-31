from pyray import *
from raylib import *

from config import Config
from shapes import Rectangle

from homescreen.hsbutton import Button

class Selector:
    def __init__(self, options:list, num_options:int, left_button_pos:Vector2, right_button_pos:Vector2, buttons_size:Vector2, font_size:float=20.0):
        self.options = options
        self.num_options = num_options
        self.current = 1

        self.buttons_size = buttons_size
        self.left_button_pos = left_button_pos
        self.right_button_pos = right_button_pos

        self.left_button = Button(left_button_pos, self.buttons_size, BLANK, LIGHTGRAY, "<", font_size)
        self.right_button = Button(right_button_pos, self.buttons_size, BLANK, LIGHTGRAY, ">", font_size)
        self.font_size = font_size

    def update(self) -> None:
        """
        Função: update
        Descrição:
            Atualiza o estado do seletor.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        change_amount = self.update_buttons()
        self.change(change_amount)

    def update_scale(self, scaler:float) -> None:
        """
        Função: update_scale
        Descrição:
            Atualiza a escala dos botões do seletor.
        Parâmetros:
            scaler: float - novo valor para a escala.
        Retorno:
            Nenhum.
        """
        self.right_button.update_scale(scaler)
        self.left_button.update_scale(scaler)

    def draw_buttons(self, scaler:float) -> None:
        """
        Função: draw_buttons
        Descrição:
            Desenha os botões do seletor.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        self.left_button.draw(scaler)
        self.right_button.draw(scaler)

    def draw(self, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha o seletor.
        Parâmetros:
            scaler: float - escala em que deve ser o desenho do botão.
        Retorno:
            Nenhum.
        """
        
        self.draw_buttons(scaler)

    def change(self, increment:int) -> None:
        """
        Função: change
        Descrição:
            Atualiza o índice da seleção atual.
        Parâmetros:
            increment: int - o incremento em relação à lista de opções disponíveis.
        Retorno:
            Nenhum.
        """
        if self.current + increment > self.num_options:
            self.current = increment
        elif self.current + increment < 1:
            self.current = self.num_options
        else:
            self.current += increment

    def update_buttons(self) -> int:
        """
        Função: check_button_press
        Descrição:
            Checa se algum dos botões para alterar a seleção atual foi acionado.
        Parâmetros:
            Nenuhm.
        Retorno:
            0, nenhum botão foi acionado;
            -1, o botão da esquerda foi acionado;
            1, o botão da direita foi acionado.
        """
        if self.left_button.update():
            return -1
        if self.right_button.update():
            return 1
        return 0

class MapSelector(Selector):
    def __init__(self):
        maps = ((Config.FREE_FOR_ALL_MAP_ID, "Free For All"), (Config.PAYLOAD_MAP_ID, "Payload"), (Config.CAPTURE_THE_FLAG_MAP_ID, "Capture the Flag"), (Config.DOMINATION_MAP_ID, "Domination"))

        self.map_colors = [PURPLE, MAGENTA, BLUE, BLACK]

        right_button_pos = Vector2(405, 270)
        left_button_pos = Vector2(30, 270)
        buttons_size = Vector2(35, 50)

        super().__init__(maps, len(maps), left_button_pos, right_button_pos, buttons_size)

        self.map_rec_pos = Vector2(75, 210)
        self.map_rec_size = Vector2(320, 180)
        self.map_rec = Rectangle(self.map_rec_pos, self.map_rec_size)       

    def update(self, scaler:float) -> None:
        """
        Função: update
        Descrição:
            Atualiza o estado do seletor de mapas.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().update()
        self.update_scale(scaler)

    def update_scale(self, scaler:float) -> None:
        """
        Função: update_scale
        Descrição:
            Atualiza a escala dos botões.
        Parâmetros:
            scaler: float - novo valor para a escala.
        Retorno:
            Nenhum.
        """
        super().update_scale(scaler)
        
        updated_map_rec_pos = Vector2(self.map_rec_pos.x * scaler, self.map_rec_pos.y * scaler)
        updated_map_rec_size = Vector2(self.map_rec_size.x * scaler, self.map_rec_size.y * scaler)

        self.map_rec.position = updated_map_rec_pos
        self.map_rec.size = updated_map_rec_size

    def draw_buttons(self, scaler:float) -> None:
        """
        Função: draw_buttons
        Descrição:
            Desenha os botões do seletor de mapa.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().draw_buttons(scaler)

    def draw_map(self, scaler:float) -> None:
        """
        Função: draw_map
        Descrição:
            Desenha o mapa selecionado no momento.
        Parâmetros:
            scaler: float - escala atual da janela.
        Retorno:
            Nenhum.
        """
        draw_rectangle_v(self.map_rec.position, self.map_rec.size, self.map_colors[self.current-1])

        map_name = self.options[self.current-1][1]
        spacing = 1.0

        text_size = measure_text_ex(get_font_default(), map_name, 20.0 * scaler, spacing)
        text_pos = Vector2(self.map_rec.position.x + (self.map_rec.size.x - text_size.x)/2.0, 145 * scaler)

        draw_text_ex(get_font_default(), map_name, text_pos, 20.0 * scaler, spacing, BLACK)

    def change(self, increment:int) -> None:
        """
        Função: change
        Descrição:
            Atualiza o índice da seleção atual.
        Parâmetros:
            increment: int - o incremento em relação à lista de opções disponíveis.
        Retorno:
            Nenhum.
        """
        super().change(increment)

    def check_button_press(self) -> int:
        """
        Função: check_button_press
        Descrição:
            Checa se algum dos botões para alterar a seleção de mapa atual foi acionado.
        Parâmetros:
            Nenuhm.
        Retorno:
            0, nenhum botão foi acionado;
            -1, o botão da esquerda foi acionado;
            1, o botão da direita foi acionado.
        """
        return super().check_button_press()

    def draw(self, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha os botões para alterar a escolha do mapa e qual mapa está sendo escolhido no momento.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().draw(scaler)
        self.draw_map(scaler)
    
class SkinSelector(Selector):
    def __init__(self):
        skins = ((Config.RED_SKIN_ID, "Red Shadow Wizard"), (Config.BLUE_SKIN_ID, "Blue Shadow Wizard"), (Config.GREEN_SKIN_ID, "Green Shadow Wizard"), (Config.GOLD_SKIN_ID, "Golden Shadow Wizard"))
        
        # *** Definir a posição dos botões
        right_button_pos = Vector2(750, 270)
        left_button_pos = Vector2(495, 270)
        buttons_size = Vector2(35, 50)

        self.skin_pos = Vector2(640, 310)
        self.skin_radius = 90

        self.name_pos = Vector2(535, 145)

        super().__init__(skins, len(skins), left_button_pos, right_button_pos, buttons_size)

    def update(self, scaler:float):
        """
        Função: update
        Descrição:
            Atualiza o estado do seletor de skin.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().update()
        self.update_scale(scaler)

    def update_scale(self, scaler:float) -> None:
        """
        Função: update_scale
        Descrição:
            Atualiza a escala dos botões.
        Parâmetros:
            scaler: float - novo valor para a escala.
        Retorno:
            Nenhum.
        """
        super().update_scale(scaler)

    def draw_buttons(self, scaler:float):
        """
        Função: draw_buttons
        Descrição:
            Desenha os botões do seletor de skin.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().draw_buttons(scaler)

    def draw_skin(self, scaler:float) -> None:        
        """
        Função: draw_skin
        Descrição:
            Desenha a skin selecionada no momento junto com o seu nome.
        Parâmetros:
            scaler: float - escala atual da janela.
        Retorno:
            Nenhum.
        """
        skin_name = self.options[self.current-1][1]
        draw_circle_v(Vector2(self.skin_pos.x * scaler, self.skin_pos.y * scaler), self.skin_radius * scaler, self.skin_color)
        
        spacing = 1.0

        text_size = measure_text_ex(get_font_default(), skin_name, 20.0 * scaler, spacing)
        text_pos = Vector2(self.skin_pos.x * scaler + (self.skin_radius * scaler - text_size.x), 145 * scaler)
        
        draw_text_ex(get_font_default(), skin_name, text_pos, 20.0 * scaler, spacing, BLACK)

    def change(self, increment:int):
        """
        Função: change
        Descrição:
            Atualiza o índice da seleção atual.
        Parâmetros:
            increment: int - o incremento em relação à lista de opções disponíveis.
        Retorno:
            Nenhum.
        """
        super().change(increment)

    def check_button_press(self):
        """
        Função: check_button_press
        Descrição:
            Checa se algum dos botões para alterar a seleção de skin atual foi acionado.
        Parâmetros:
            Nenuhm.
        Retorno:
            0, nenhum botão foi acionado;
            -1, o botão da esquerda foi acionado;
            1, o botão da direita foi acionado.
        """
        return super().check_button_press()

    @property
    def skin_color(self) -> Color:
        current_skin = self.options[self.current-1][0]
        if current_skin == Config.RED_SKIN_ID:
            return RED
        elif current_skin == Config.BLUE_SKIN_ID:
            return BLUE
        elif current_skin == Config.GREEN_SKIN_ID:
            return GREEN
        elif current_skin == Config.GOLD_SKIN_ID:
            return GOLD
        
        raise AttributeError

    def draw(self, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha os botões para alterar a escolha da skin e qual skin está sendo escolhido no momento.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        super().draw(scaler)
        self.draw_skin(scaler)
