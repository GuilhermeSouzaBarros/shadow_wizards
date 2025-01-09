from pyray import *
from raylib import *

from config import *
from vectors import Vector2
from homescreen.hsselectors import MapSelector, CharacterSelector
from homescreen.hsbutton import Button

class HomeScreen:
    def __init__(self, window_size:list):
        self.window_size = window_size

        self.map_selector = MapSelector(window_size)
        self.character_selector = CharacterSelector(window_size)
        self.play_button = Button(window_size, Vector2(0.5, 0.85), Vector2(0.4, 0.2), GREEN, DARKGREEN, "Play")

        self.font_size = int(window_size[1] * 0.2)
        self.text_spacing = int(window_size[0] * 0.002)
        self.text_size = measure_text_ex(get_font_default(), GAME_TITLE, self.font_size, self.text_spacing)
        self.text_pos = Vector2((window_size[0] - self.text_size.x) / 2, window_size[1] * 0.15 - self.text_size.y * 0.5)

        self.start_game = False

    @property
    def selected_map(self) -> int:
        return self.map_selector.current[0]

    @property
    def selected_caracter(self) -> int:
        return self.character_selector.character_id
    
    def update(self) -> bool:
        self.map_selector.update()
        self.character_selector.update()
        self.play_button.update()
        if self.play_button.is_pressed:
            self.start_game = True
        
    def update_scale(self, window_size:list) -> None:
        self.window_size = window_size  

        self.font_size = int(window_size[1] * 0.2)
        self.text_spacing = int(window_size[0] * 0.002)
        self.text_size = measure_text_ex(get_font_default(), GAME_TITLE, self.font_size, self.text_spacing)
        self.text_pos = Vector2((window_size[0] - self.text_size.x) / 2, window_size[1] * 0.15 - self.text_size.y * 0.5)

        self.map_selector.update_scale(window_size)
        self.character_selector.update_scale(window_size)
        self.play_button.update_scale(window_size)

    def draw_title(self) -> None:
        draw_text_ex(get_font_default(), GAME_TITLE, self.text_pos.to_list(), self.font_size, self.text_spacing, RED)

    def draw(self) -> None:
        begin_drawing()

        clear_background(GRAY)
        self.map_selector.draw()
        self.character_selector.draw()
        self.play_button.draw()
        self.draw_title()

        end_drawing()
    
    def unload(self) -> None:
        for caracter in self.character_selector.options:
            unload_texture(caracter['sprite'])
        print("Menu unloaded")
        