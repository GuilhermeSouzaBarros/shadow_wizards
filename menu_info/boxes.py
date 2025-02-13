from pyray import *
from raylib import *

from random import choice

from abc import ABC

from sprite import CharacterSprite

from imaginary import Imaginary
from vectors import Vector2
from shapes import Rectangle

def font_size_from_percentage(string:str, font:Font, font_size:float, size:Vector2) -> int:
    true_font_size = size.y * font_size
    text_len = measure_text_ex(font, string, true_font_size, 2)
    buffer = 1.15
    if text_len.x * buffer > size.x:
        true_font_size *= size.x / (text_len.x * buffer)
    return int(true_font_size)

def load_boxes(font:Font, window_size:Vector2, json:dict):
    boxes = []
    if 'text_boxes' in json:
        for text in json['text_boxes']:
            position = Vector2(text['position'][0], text['position'][1])
            size = Vector2(text['size'][0], text['size'][1])
            if 'type' in text: type = text['type']
            else: type = ''
            text_box = TextBox(text['string'], font, text['font_size'], text['color'], position, size, type, window_size)
            boxes.append(text_box)

    if 'text_buttons' in json:
        for button in json['text_buttons']:
            position = Vector2(button['position'][0], button['position'][1])
            size = Vector2(button['size'][0], button['size'][1])
            text_button = TextButton(button['string'], font, button['font_size'], button['text_color'], button['button_color'], button['type'], button['target'], position, size, window_size)
            boxes.append(text_button)
            
    if 'selected_groups' in json:
        for selected_group in json['selected_groups']:
            buttons = []
            if 'render_buttons' in selected_group:
                for character_button in selected_group['render_buttons']:
                    position = Vector2(character_button['position'][0], character_button['position'][1])
                    size = Vector2(character_button['size'][0], character_button['size'][1])
                    sprite_info = character_button['sprite']
                    sprite_size = Vector2(sprite_info['size'][0], sprite_info['size'][1])
                    sprite_offset = Vector2(sprite_info['offset'][0], sprite_info['offset'][1])
                    sprite = CharacterSprite(sprite_info['path'], sprite_size, sprite_offset, sprite_info['tint'])
                    buttons.append(ButtonRender(sprite, selected_group['type'], character_button['target'], position, size, window_size))

            if 'selected_text_buttons' in selected_group:
                for selected_text_button in selected_group['selected_text_buttons']:
                    position = Vector2(selected_text_button['position'][0], selected_text_button['position'][1])
                    size = Vector2(selected_text_button['size'][0], selected_text_button['size'][1])
                    buttons.append(SelectedTextButton(selected_text_button['string'], font, selected_text_button['font_size'], selected_text_button['text_color'], selected_text_button['button_color'], selected_group['type'], selected_text_button['target'], position, size, window_size))

            boxes.append(SelectedGroup(buttons, selected_group['type']))

    if 'random_renders' in json:
        for random_render in json['random_renders']:
            sprites = []
            for sprite in random_render['sprites']:
                sprite_size = Vector2(sprite['size'][0], sprite['size'][1])
                sprite_offset = Vector2(sprite['offset'][0], sprite['offset'][1])
                sprites.append(
                    CharacterSprite(sprite['path'], sprite_size, sprite_offset, sprite['tint'])
                )
            position = Vector2(random_render['position'][0], random_render['position'][1])
            size = Vector2(random_render['size'][0], random_render['size'][1])
            random_render = RandomRender(sprites, position, size, window_size)
            boxes.append(random_render)
    return boxes

class Box(ABC):
    def __init__(self, position:Vector2, size:Vector2, window_size:Vector2):
        self.position = position
        self._size = size
        
        self.true_position = Vector2(window_size.x * position.x, window_size.y * position.y)
        self.true_size = Vector2(size.x * window_size.x, size.y * window_size.y)
        self.hitbox = Rectangle(self.true_position, self.true_size)

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size:Vector2):
        ratio_x = size.x / self._size.x
        self.true_size.x *= ratio_x
        self.hitbox.size.x *= ratio_x
        
        ratio_y = size.y / self._size.y
        self.true_size.y *= ratio_y
        self.hitbox.size.y *= ratio_y

        self.hitbox.lines = self.hitbox.to_lines()        

        self._size = size

    def update(self):
        pass

    def update_scale(self, window_size:Vector2):
        self.true_position = Vector2(window_size.x * self.position.x, window_size.y * self.position.y)
        self.true_size = Vector2(self.size.x * window_size.x, self.size.y * window_size.y)
        self.hitbox = Rectangle(self.true_position, self.true_size)

    def draw(self):
        pass

class TextBox(Box):
    def __init__(self, string:str, font:Font, font_size:float, color:Color,
                 position:Vector2, size:Vector2, type:str, window_size:Vector2) -> None:
        Box.__init__(self, position, size, window_size)
        self.string = string
        self.font = font
        self.font_size = font_size
        self.text_color = color
        self.position = position
        self.type = type

        self.true_font_size = font_size_from_percentage(string, font, font_size, self.true_size)
        self.text_len =  measure_text_ex(font, string, self.true_font_size, 2)
        self.text_pos = Vector2(self.true_position.x - (self.text_len.x * 0.5),
                                self.true_position.y - (self.text_len.y * 0.5))

    @Box.size.setter
    def size(self, size:Vector2):
        Box.size.fset(self, size)
        self.true_font_size = font_size_from_percentage(self.string, self.font, self.font_size, self.true_size)
        self.text_len =  measure_text_ex(self.font, self.string, self.true_font_size, 2)
        self.text_pos = Vector2(self.true_position.x - (self.text_len.x * 0.5),
                                self.true_position.y - (self.text_len.y * 0.5))

    def update_text(self):
        self.true_font_size = font_size_from_percentage(self.string, self.font, self.font_size, self.true_size)
        self.text_len =  measure_text_ex(self.font, self.string, self.true_font_size, 2)
        self.text_pos = Vector2(self.true_position.x - (self.text_len.x * 0.5),
                                self.true_position.y - (self.text_len.y * 0.5))

    def change_text(self, string:str):
        if string != self.string:
            self.string = string
            self.update_text()

    def update_scale(self, window_size:Vector2) -> None:
        Box.update_scale(self, window_size)
        self.update_text()

    def draw(self):
        draw_text_ex(self.font, self.string, self.text_pos.to_list(), self.true_font_size, 2, self.text_color)


class Button(Box):
    def __init__(self, button_color:Color, type:str, target:int, position:Vector2, size:Vector2, window_size:Vector2):
        Box.__init__(self, position, size, window_size)
        self.type = type
        self.button_color = button_color
        
        self.target = target
        self.hovered = False
        self.pressed = False

        self.true_hitbox = self.hitbox.copy()

        self.animation_time = 0.075
        self.default_size = size

        self.hovered_size = size * 1.05
        self.hovered_time = None

        self.pressed_size = size * 0.95
        self.pressed_time = None

    def update_scale(self, window_size):
        Box.update_scale(self, window_size)
        default_true_size = Vector2(self.default_size.x * window_size.x, self.default_size.y * window_size.y)
        self.true_hitbox = Rectangle(self.true_position, default_true_size)

    def update(self) -> None:
        self.hovered = self.true_hitbox.is_point_inside(get_mouse_position())
        self.pressed = self.hovered and is_mouse_button_down(MOUSE_BUTTON_LEFT)
        cur_time = get_time()
        if self.hovered and not self.hovered_time:
            self.hovered_time = cur_time
        
        if self.pressed and not self.pressed_time:
            self.pressed_time = cur_time
        
        if self.pressed_time:
            if cur_time - self.pressed_time < self.animation_time:
                self.size = self.hovered_size - ((self.pressed_size - self.hovered_size) * (self.pressed_time - cur_time) / self.animation_time)
            else:
                self.size = self.pressed_size  

        elif self.hovered_time:
            if cur_time - self.hovered_time < self.animation_time:
                self.size = self.default_size - ((self.hovered_size - self.default_size) * (self.hovered_time - cur_time) / self.animation_time)
            else:
                self.size = self.hovered_size

        if not self.hovered:
            self.hovered_time = None
            self.pressed_time = None
            if self.size != self.default_size:
                self.size = self.default_size
        

    def draw(self) -> None:
        color = color_brightness(self.button_color, -(self.hovered + self.pressed) / 6)
        self.hitbox.draw(color, outlines=self.hovered)


class TextButton(Button, TextBox):
    def __init__(self, string:str, font:Font, font_size:float, text_color:Color, button_color:Color,
                 type:str, target:int, position:Vector2, size:Vector2, window_size:Vector2):
        TextBox.__init__(self, string, font, font_size, text_color, position, size, type, window_size)
        Button.__init__(self, button_color, type, target, position, size, window_size)

    def update_scale(self, window_size):
        Button.update_scale(self, window_size)
        TextBox.update_scale(self, window_size)

    def draw(self) -> None:
        Button.draw(self)
        TextBox.draw(self)


class SelectedButton(Button):
    def __init__(self, button_color:Color, type:str, target:int, position:Vector2, size:Vector2, window_size:Vector2):
        Button.__init__(self, button_color, type, target, position, size, window_size)
        self.selected = False

    def update(self):
        Button.update(self)
        if self.selected:
            self.size = self.pressed_size
            self.hovered = True


class SelectedTextButton(SelectedButton, TextBox):
    def __init__(self, string:str, font:Font, font_size:float, text_color:Color, button_color:Color,
                 type:str, target:int, position:Vector2, size:Vector2, window_size:Vector2):
        TextBox.__init__(self, string, font, font_size, text_color, position, size, type, window_size)
        SelectedButton.__init__(self, button_color, type, target, position, size, window_size)
    
    def update_scale(self, window_size):
        SelectedButton.update_scale(self, window_size)
        TextBox.update_scale(self, window_size)

    def draw(self):
        SelectedButton.draw(self)
        TextBox.draw(self)


class Render(Box):
    def __init__(self, sprite:CharacterSprite, position:Vector2, size:Vector2, window_size:Vector2):
        Box.__init__(self, position, size, window_size)
        self.angle = Imaginary(0, 1)
        self.sprite = sprite
    
    def draw(self):
        self.sprite.draw(self.hitbox, self.angle, self.sprite.offset)

class ButtonRender(SelectedButton, Render):
    def __init__(self, sprite:CharacterSprite, type:str, target:int, position:Vector2, size:Vector2, window_size:Vector2):
        SelectedButton.__init__(self, WHITE, type, target, position, size, window_size)
        Render.__init__(self, sprite, position, size, window_size)
    
    def draw(self):
        SelectedButton.draw(self)
        Render.draw(self)

class RandomRender(Render):
    def __init__(self, sprites:list, position:Vector2, size:Vector2, window_size:Vector2):
        self.previous_time = get_time()
        self.sprites = sprites
        Render.__init__(self, sprites[0], position, size, window_size)

    def update(self):
        current_time = get_time()
        if current_time - self.previous_time > 1.0:
            self.angle *= Imaginary(1, 1, 1)
            if int(self.angle.to_degree()) == 0:
                self.sprite = choice(self.sprites)
            self.previous_time = current_time

class SelectedGroup:
    def __init__(self, group:SelectedButton, type:str):
        self.group = group
        self.type = type
        self.button_selected = choice(group)
        self.button_selected.selected = True

    def new_selected_button(self, button:Button):
        self.button_selected.selected = False
        self.button_selected = button
        self.button_selected.selected = True

    def new_target(self, target:int):
        for button in self.group:
            if button.target == target:
                self.new_selected_button(button)

    def update(self):
        for button in self.group:
            button.update()
            if button.pressed and button != self.button_selected:
                self.new_target(button.target)

    def update_scale(self, window_size:Vector2):
        for button in self.group:
            button.update_scale(window_size)
        
    def draw(self):
        for button in self.group:
            button.draw()
