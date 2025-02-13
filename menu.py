from pyray import *
from raylib import *
from json import load

from config import *
from vectors import Vector2

from menu_info.boxes import *

from sockets.address import get_address
from sockets.server import Server
from sockets.client import Client

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
    def __init__(self, window_size:list, initial_screen:int=0, server:Server=None, client:Client=None, server_addr_ip:dict={}):
        self.window_size = Vector2(window_size[0], window_size[1])
        self.font = load_font_ex("fonts/PixAntiqua.ttf", 32, None, 250)
        self.screens = []
        for screen in MENU_SCREENS:
            self.screens.append(MenuScreen(screen, self.font, self.window_size))
        self.current_screen = self.screens[initial_screen]

        for group in self.screens[1].boxes:
            if group.__class__ != SelectedGroup:
                continue
            self.selected_character = group.button_selected.target
            break

        for group in self.screens[2].boxes:
            if group.__class__ != SelectedGroup:
                continue
            self.selected_map = group.button_selected.target
            break

        self.selected_characters = {}
        self.server_addr_ip = server_addr_ip
        self.start_game = False

        self.server = server
        self.client = client

        self.close_window = False

    def update(self):
        if is_key_pressed(KEY_ESCAPE):
            self.current_screen = self.screens[self.current_screen.esc_page]
            return
        
        if is_mouse_button_released(MOUSE_BUTTON_LEFT):
            for button in self.current_screen.boxes:
                if not issubclass(button.__class__, Button) or not button.pressed:
                    continue
                button.pressed_time = None
                if button.type == "screen":
                    self.current_screen = self.screens[button.target]

                elif button.type == "open_lobby":
                    if not self.server:
                        self.server = Server()

                elif button.type == "find_lobby":
                    if not self.client:
                        self.client = Client()
                        button.change_text("Searching...")

                elif button.type == "change_ip":
                    self.client.server_addr = get_address()

                elif button.type == "game_start":
                    if len(self.selected_characters) >= 0:
                        self.server.send_queue.put(self.encode("start"))
                        self.start_game = True

                elif button.type == "exit":
                    self.close_window = True

            for group in self.current_screen.boxes:
                if group.__class__ != SelectedGroup or not group.button_selected.pressed:
                    continue
                if group.type == "character":
                    self.selected_character = group.button_selected.target
                    if self.client and self.client.server_handshake:
                        self.client.send_queue.put(self.encode("character"))

                elif group.type == "map":
                    self.selected_map = group.button_selected.target
                    if self.server:
                        self.server.send_queue.put(self.encode("map"))

        if self.server:
            self.server.update()
            while True:
                try:
                    data = self.server.get_queue.get_nowait()
                except:
                    break
                self.decode(data[0], data[1])
            for box in self.screens[2].boxes:
                if issubclass(box.__class__, TextButton) and box.type == "open_lobby":
                    box.change_text(f"Lobby: {len(self.server.clients_addresses)}/4 players")

        if self.client:
            self.client.update()
            while True:
                try:
                    data = self.client.get_queue.get_nowait()
                except:
                    break
                self.decode(self.client.server_addr, data)

            if self.client.server_handshake:
                for button in self.screens[1].boxes:
                    if not issubclass(button.__class__, Button) or button.type != "find_lobby":
                        continue
                    button.change_text("Lobby found!")
            else:
                if self.client.send_queue.empty():
                    self.client.send_queue.put(self.encode("ping"))

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
    
    def encode(self, data:str) -> bytes:
        if data == "ping":
            return "p".encode()
        
        if data == "map":
            return "m".encode() + self.selected_map.to_bytes(1)
        
        if data == "character":
            return "c".encode() + self.selected_character.to_bytes(1)
        
        if data == "start":
            message = "s".encode() + len(self.selected_characters).to_bytes(1)
            for character in self.selected_characters.values():
                message += character.to_bytes(1)
            message += self.selected_map.to_bytes(1)
            return message
    
    def decode(self, addr:tuple, data:bytes) -> None:
        data_dec = chr(data[0])
        if data_dec == "p":
            if self.server and (self.server.ip, self.server.port) != addr:
                if not addr in self.server.clients_addresses:
                    self.server.clients_addresses.append(addr)
                    self.server_addr_ip.update({addr: len(self.server_addr_ip) + 1})
                    for box in self.screens[2].boxes:
                        if issubclass(box.__class__, TextButton) and box.type == "open_lobby":
                            box.change_text(f"Lobby: {len(self.server.clients_addresses)}/4 players")

                self.server.send_queue.put(self.encode("ping"))
                self.server.send_queue.put(self.encode("map"))
            else:
                self.client.server_handshake = True
                self.client.send_queue.put(self.encode("character"))

        elif data_dec == "m" and not self.server:
            self.selected_map = data[1]
            for group in self.screens[2].boxes:
                if group.__class__ != SelectedGroup and group.type != "map":
                    continue
                group.new_target(self.selected_map)
        
        elif data_dec == "c":
            self.selected_characters[self.server_addr_ip[addr]] = data[1]

        elif data_dec == "s":
            character_count = data[1]
            for i in range(2, 2 + character_count):
                self.selected_characters.update({i - 1: data[i]})
            self.selected_map = data[2+character_count]
            self.start_game = True
