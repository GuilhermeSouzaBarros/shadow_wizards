from pyray import *
from raylib import *

from vectors import Vector2
from shapes import Rectangle

class Button():
    def __init__(self, window_size:list, pos:Vector2, size: Vector2, default_color: Color, hovering_color: Color, text: str):
        self.percentage_pos = pos
        self.percentage_size = size

        pixel_pos = Vector2(pos.x * window_size[0], pos.y * window_size[1])
        pixel_size = Vector2(size.x * window_size[0], size.y * window_size[1])
        self.rec = Rectangle(pixel_pos, pixel_size)
        self.default_color = default_color
        self.hovering_color = hovering_color

        self.text = text
        self.spacing = int(pixel_size.x / 100)
        self.font_size = int(pixel_size.y * 0.8)
        self.text_size = measure_text_ex(get_font_default(), self.text, self.font_size, 1.0)
        self.text_pos = Vector2(self.rec.position.x - self.text_size.x/2.0,
                                self.rec.position.y - self.text_size.y/2.0)

        self.is_hovering = False
        self.is_pressed = False

    def draw(self) -> None:
        if self.is_hovering:
            self.rec.draw(self.hovering_color, outlines=True)
        else:
            self.rec.draw(self.default_color, outlines=False)
        
        draw_text_ex(get_font_default(), self.text, self.text_pos.to_list(), self.font_size, self.spacing, WHITE)

    def update(self) -> bool:
        mouse_pos = get_mouse_position()
        self.is_hovering = check_collision_point_rec(mouse_pos, [self.rec.position.x - self.rec.size.x / 2,
                                                                 self.rec.position.y - self.rec.size.y / 2,
                                                                 self.rec.size.x, self.rec.size.y])
        self.is_pressed  = self.is_hovering and is_mouse_button_pressed(MOUSE_BUTTON_LEFT)

    def update_scale(self, window_size:list):
        pixel_pos = Vector2(self.percentage_pos.x * window_size[0], self.percentage_pos.y * window_size[1])
        pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.rec = Rectangle(pixel_pos, pixel_size)

        self.spacing = int(pixel_size.x / 100)
        self.font_size = int(pixel_size.y * 0.8)
        self.text_size = measure_text_ex(get_font_default(), self.text, self.font_size, 1.0)
        self.text_pos = Vector2(self.rec.position.x - self.text_size.x/2.0,
                                self.rec.position.y - self.text_size.y/2.0)
        