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
        self.current_id = 1
        self.current = self.options[0]

        self.percentage_pos = pos
        self.percentage_size = size

        self.side_buttons_size = Vector2(size.x * 0.1, size.y * 0.2)
        self.left_button  = Button(window_size, Vector2(pos.x - size.x * 0.6, pos.y), self.side_buttons_size, BLANK, LIGHTGRAY, "<")
        self.right_button = Button(window_size, Vector2(pos.x + size.x * 0.6, pos.y), self.side_buttons_size, BLANK, LIGHTGRAY, ">")

    def update_buttons(self) -> int:
        self.left_button.update()
        self.right_button.update()
    
    def change(self) -> None:
        self.current_id += -self.left_button.is_pressed + self.right_button.is_pressed
        self.current_id %= self.num_options
        if self.current_id < 0:
            self.current_id = self.num_options
        self.current = self.options[self.current_id-1]

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
        maps = ((FREE_FOR_ALL_MAP_ID, "Free For All", PURPLE),
                (PAYLOAD_MAP_ID, "Payload", MAGENTA),
                (CAPTURE_THE_FLAG_MAP_ID, "Capture the Flag", BLUE),
                (DOMINATION_MAP_ID, "Domination", LIGHTGRAY))

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
        self.map_rec.draw(self.current[2])

        map_name = self.current[1]
        font_size = self.pixel_size.y * 0.15
        spacing = self.pixel_size.x * 0.01
        text_size = measure_text_ex(get_font_default(), map_name, font_size, spacing)
        text_pos = Vector2(self.map_rec.position.x - text_size.x/2.0, self.map_rec.position.y - text_size.y/2.0)

        draw_text_ex(get_font_default(), map_name, text_pos.to_list(), font_size, spacing, BLACK)

    def draw(self) -> None:
        self.draw_map()
        super().draw()


class CharacterSelector(Selector):
    def __init__(self, window_size:list):
        characters = [] 
        for character in CHARACTERS:
            characters.append(character.copy())
        
        for character in characters:
            character['sprite'] = load_texture(character['sprite'])
        
        self.percentage_pos  = Vector2(0.75, 0.5)
        self.percentage_size = Vector2(0.35, 0.4)
        self.percentage_character_radius = self.percentage_size.y / 2.0

        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.pixel_character_radius = self.percentage_character_radius * window_size[1] / 2

        self.text_pos = Vector2(self.percentage_pos.x, self.percentage_pos.y - self.percentage_size.y * 0.6)
        super().__init__(window_size, characters, self.percentage_pos, self.percentage_size)

    def update_scale(self, window_size:list) -> None:
        self.pixel_pos  = Vector2(self.percentage_pos.x  * window_size[0], self.percentage_pos.y  * window_size[1])
        self.pixel_size = Vector2(self.percentage_size.x * window_size[0], self.percentage_size.y * window_size[1])
        self.pixel_character_radius = self.percentage_character_radius * window_size[1] / 2
        super().update_scale(window_size)

    def draw_character(self) -> None:
        tint = self.current['color']
        if self.current['id'] == CHARACTER_RED['id']:
            tint = WHITE
        pos_x = 0
        if self.current['id'] == CHARACTER_BLUE['id']:
            tint = WHITE
            pos_x += 32

        draw_texture_pro(self.current['sprite'], [pos_x, 64, 32, 32],
                         [self.pixel_pos.x - self.pixel_size.y / 2,
                          self.pixel_pos.y - self.pixel_size.y / 2,
                          self.pixel_size.y, self.pixel_size.y], [0, 0], 0, tint)
        
    
        character_name = self.current["name"]
        font_size = self.pixel_size.y * 0.15
        spacing = self.pixel_size.x * 0.01
        text_size = measure_text_ex(get_font_default(), character_name, font_size, spacing)
        text_pos = Vector2(self.pixel_pos.x - text_size.x/2.0, self.pixel_pos.y - self.pixel_size.y * 0.6 - text_size.y/2.0)
        
        draw_text_ex(get_font_default(), character_name, text_pos.to_list(), font_size, spacing, BLACK)

    @property
    def character_id(self) -> int:
        return self.current['id']

    def draw(self) -> None:
        self.draw_character()
        super().draw()
