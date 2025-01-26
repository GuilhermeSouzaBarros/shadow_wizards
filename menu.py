from pyray import *
from raylib import *
from json import load

from random import choice

from config import *
from vectors import Vector2

from sprite import CaracterSprite
from menu_info.boxes import *

class MenuScreen():
    def __init__(self, json_path:str, font:Font, window_size:Vector2):
        self.font = font
        self.info = load(open(json_path, 'r'))
        self.id = self.info['id']
        self.esc_page = self.info['esc_page']
        self.background_color = self.info['background']

        self.boxes = load_boxes(font, window_size, self.info)


    def update_scale(self, window_size:Vector2):
        for box in self.boxes:
            box.update_scale(window_size)

    def update(self) -> None:
        for box in self.boxes:
            box.update()

    def draw(self):
        begin_drawing()
        clear_background(self.background_color)
        
        for box in self.boxes:
            box.draw()

        end_drawing()

class Menu:
    def __init__(self, window_size:list):
        self.window_size = Vector2(window_size[0], window_size[1])
        self.font = load_font_ex("fonts/PixAntiqua.ttf", 32, None, 250)
        self.current_screen = None
        self.screens = []
        for screen in MENU_SCREENS:
            new_screen = MenuScreen(screen, self.font, self.window_size)
            if new_screen.id == MENU_MAIN_ID:
                self.current_screen = new_screen
            self.screens.append(new_screen)

        self.selected_caracter = 1
        self.selected_map = 1
        self.start_game = False

        self.close_window = False

    def update(self):
        if is_key_pressed(KEY_ESCAPE):
            self.current_screen = self.screens[self.current_screen.esc_page]
            return
        
        if is_mouse_button_released(MOUSE_BUTTON_LEFT):
            for button in self.current_screen.boxes:
                if not issubclass(button.__class__, Button) or not button.pressed:
                    continue
                if button.type == "screen":
                    self.current_screen = self.screens[button.target]
                elif button.type == "game_start":
                    self.start_game = True
                    for group in self.current_screen.boxes:
                        if group.__class__ != SelectedGroup:
                            continue
                        if group.type == "caracter":
                            self.selected_caracter = group.button_selected.target
                        elif group.type == "map":
                            self.selected_map = group.button_selected.target
                elif button.type == "exit":
                    self.close_window = True

        self.current_screen.update()
        
    def update_scale(self, window_size:list) -> None:
        window_size = Vector2(window_size[0], window_size[1])
        for screen in self.screens:
            screen.update_scale(window_size)
    
    def draw(self):
        self.current_screen.draw()
    
    def unload(self) -> None:
        unload_font(self.font)
        for screen in self.screens:
            for sprite_haver in screen.boxes:    
                if sprite_haver.__class__ == Render:
                    unload_texture(sprite_haver.texture)

                elif sprite_haver.__class__ == RandomRender:
                    for sprite in sprite_haver.sprites:
                        unload_texture(sprite.texture)

                elif sprite_haver.__class__ == SelectedGroup:
                    for button in sprite_haver.group:
                        if issubclass(button.__class__, Render):
                            unload_texture(button.sprite.texture)
        print("Menu unloaded")
        