from pyray import *
from raylib import *

from shapes import Rectangle
from imaginary import Imaginary

class Button():
    def __init__(self, button_pos: Vector2, button_size: Vector2, default_color: Color, hovering_color: Color, text: str, font_size:float=20.0):
        
        self.button_pos = button_pos
        self.button_size = button_size
        
        self.button_rec = Rectangle(button_pos, button_size)
        self.default_color = default_color
        self.hovering_color = hovering_color
        self.text = text
        self.font_size = font_size

    def draw(self, scaler:float) -> None:
        """
        Função: draw
        Descrição:
            Desenha o botão.
        Parâmetros:
            Nenhum.
        Retorno:
            Nenhum.
        """
        if self.is_hovering:
            # Desenha o botão com cor quando o mouse estiver por cima dele
            draw_rectangle_v(self.button_rec.position, self.button_rec.size, self.hovering_color)
        else:
            # Desenha o botão transparente enquanto o mouse não estiver por cima dele
            draw_rectangle_v(self.button_rec.position, self.button_rec.size, self.default_color)
        
        # Calcula o posicionamento do texto centralizado
        text_size = measure_text_ex(get_font_default(), self.text, self.font_size * scaler, 1.0)
        text_pos = Vector2(self.button_rec.position.x + (self.button_rec.size.x - text_size.x)/2.0, self.button_rec.position.y + (self.button_rec.size.y - text_size.y)/2.0)
        spacing = 1.0

        # Desenha o texto do botão
        draw_text_ex(get_font_default(), self.text, text_pos, self.font_size * scaler, spacing, WHITE)

    def update(self) -> bool:
        """
        Função: update
        Descrição:
            Retorna o estado atualizado do botão.
        Parâmetros:
            scaler: float - fator de escala
        Retorno:
            False, o botão não foi pressionado;
            True, o botão foi pressionado.
        """
        return self.check_button_press()

    def update_scale(self, scaler:float) -> None:
        """
        Função: update_scale
        Descrição:
            Atualiza o tamanho e a posição do botão de acordo com o scaler.
        Parâmetros:
            scaler: float - fator de escala.
        Retorno:
            Nenhum.
        """
        updated_rec_pos = Vector2(self.button_pos.x * scaler, self.button_pos.y * scaler)
        self.button_rec.position = updated_rec_pos

        updated_rec_size = Vector2(self.button_size.x * scaler, self.button_size.y * scaler)
        self.button_rec.size = updated_rec_size

    @property
    def is_hovering(self) -> bool:
        # Retorna se o mouse está em cima do botão ou não
        mouse_pos = get_mouse_position()
        if check_collision_point_rec(mouse_pos, [self.button_rec.position.x, self.button_rec.position.y, self.button_rec.size.x, self.button_rec.size.y]):
            return True
        return False

    def check_button_press(self) -> bool:
        """
        Função: check_button_press
        Descrição:
            Checa se o botão foi acionado.
        Parâmetros:
            Nenuhm.
        Retorno:
            True, o botão foi acionado;
            False, o botão não foi acionado.
        """
        if self.is_hovering and is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                return True
        return False
