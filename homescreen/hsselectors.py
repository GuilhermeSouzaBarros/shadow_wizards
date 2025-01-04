from pyray import *
from raylib import *

from config import *
from vectors import Vector2
from shapes import Rectangle

from homescreen.hsbutton import Button

class Selector:
    def __init__(self, window_size:list, options:list, pos:Vector2, size:Vector2):
        self.options = options
        self.num_options = len(options)
        self.current = 1

        self.percentage_pos = pos
        self.percentage_size = size

        self.side_buttons_size = Vector2(size.x * 0.1, size.y * 0.2)
        self.left_button  = Button(window_size, Vector2(pos.x - size.x * 0.6, pos.y), self.side_buttons_size, BLANK, LIGHTGRAY, "<")
        self.right_button = Button(window_size, Vector2(pos.x + size.x * 0.6, pos.y), self.side_buttons_size, BLANK, LIGHTGRAY, ">")

    def update_buttons(self) -> int:
        self.left_button.update()
        self.right_button.update()
    
    def change(self) -> None:
        self.current += -self.left_button.is_pressed + self.right_button.is_pressed
        self.current %= self.num_options
        if self.current < 0:
            self.current = self.num_options

    def update(self) -> None:
        self.update_buttons()
        self.change()

    def update_scale(self, window_size:list) -> None:
        self.left_button.update_scale(window_size)
        self.right_button.update_scale(window_size)

    def draw_buttons(self) -> None:
        self.left_button.draw()
        self.right_button.draw()

    def draw(self) -> None:
        self.draw_buttons()


class MapSelector(Selector):
    def __init__(self, window_size:list):
        maps = ((FREE_FOR_ALL_MAP_ID, "Free For All"),
                (PAYLOAD_MAP_ID, "Payload"),
                (CAPTURE_THE_FLAG_MAP_ID, "Capture the Flag"),
                (DOMINATION_MAP_ID, "Domination"))

        self.map_colors = [PURPLE, MAGENTA, BLUE, LIGHTGRAY]

        self.percentage_pos  = Vector2(0.25, 0.5)
        self.percentage_size = Vector2(0.35, 0.4)

        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.map_rec    = Rectangle(self.pixel_pos, self.pixel_size)

        super().__init__(window_size, maps, self.percentage_pos, self.percentage_size)
    
    def update_scale(self, window_size:list) -> None:
        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.map_rec    = Rectangle(self.pixel_pos, self.pixel_size)
        super().update_scale(window_size)

    def draw_map(self) -> None:
        self.map_rec.draw(Vector2(0, 0), 1.0, self.map_colors[self.current-1])

        map_name = self.options[self.current-1][1]
        font_size = self.pixel_size.y * 0.15
        spacing = self.pixel_size.x * 0.01
        text_size = measure_text_ex(get_font_default(), map_name, font_size, spacing)
        text_pos = Vector2(self.map_rec.position.x - text_size.x/2.0, self.map_rec.position.y - text_size.y/2.0)

        draw_text_ex(get_font_default(), map_name, text_pos.to_list(), font_size, spacing, BLACK)

    def draw(self) -> None:
        self.draw_map()
        super().draw()


class SkinSelector(Selector):
    def __init__(self, window_size:list):
        skins = ((RED_SKIN_ID, "Red Shadow Wizard"),
                 (BLUE_SKIN_ID, "Blue Shadow Wizard"),
                 (PINK_SKIN_ID, "Pink Shadow Wizard "),
                 (LIME_SKIN_ID, "Lime Shadow Wizard"),
                 (GOLD_SKIN_ID, "Golden Shadow Wizard"),
                 (YELLOW_SKIN_ID, "Yellow Shadow Wizard"),
                 (DARKGREEN_SKIN_ID, "Dark Green Shadow Wizard"),
                 (PURPLE_SKIN_ID, "Purple Shadow Wizard")
                 )
        
        self.percentage_pos  = Vector2(0.75, 0.5)
        self.percentage_size = Vector2(0.35, 0.4)
        self.percentage_skin_radius = self.percentage_size.y / 2.0

        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.pixel_skin_radius = self.percentage_skin_radius * window_size[1] / 2

        self.text_pos = Vector2(self.percentage_pos.x, self.percentage_pos.y - self.percentage_size.y * 0.6)
        super().__init__(window_size, skins, self.percentage_pos, self.percentage_size)

    def update_scale(self, window_size:list) -> None:
        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.pixel_skin_radius = self.percentage_skin_radius * window_size[1] / 2
        super().update_scale(window_size)

    def draw_skin(self) -> None:
        draw_circle_v(self.pixel_pos.to_list(), self.pixel_skin_radius, self.skin_color)
        
        skin_name = self.options[self.current-1][1]
        font_size = self.pixel_size.y * 0.15
        spacing = self.pixel_size.x * 0.01
        text_size = measure_text_ex(get_font_default(), skin_name, font_size, spacing)
        text_pos = Vector2(self.pixel_pos.x - text_size.x/2.0, self.pixel_pos.y - self.pixel_size.y * 0.6 - text_size.y/2.0)
        
        draw_text_ex(get_font_default(), skin_name, text_pos.to_list(), font_size, spacing, BLACK)

    @property
    def skin_color(self) -> Color:
        current_skin = self.options[self.current-1][0]
        if current_skin == RED_SKIN_ID:
            return RED
        elif current_skin == BLUE_SKIN_ID:
            return BLUE
        elif current_skin == PINK_SKIN_ID:
            return PINK
        elif current_skin == LIME_SKIN_ID:
            return LIME
        elif current_skin == GOLD_SKIN_ID:
            return GOLD
        elif current_skin == YELLOW_SKIN_ID:
            return YELLOW
        elif current_skin == DARKGREEN_SKIN_ID:
            return DARKGREEN
        elif current_skin == PURPLE_SKIN_ID:
            return PURPLE
        
        raise AttributeError

    def draw(self) -> None:
        self.draw_skin()
        super().draw()
