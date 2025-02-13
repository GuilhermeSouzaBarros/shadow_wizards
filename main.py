import asyncio
from pyray import *

from config import GAME_TICK
from window import Window
from menu import Menu
from game import Game

async def main():
    set_trace_log_level(5)
    window = Window()
    menu = Menu(window.size)
    init_audio_device()
    
    while not window.close_window:
        while not (menu.start_game or window.close_window or menu.close_window):
            menu.update()
            
            window.update()
            if is_window_resized():
                window.update_size()
                menu.update_scale(window.size)

            menu.draw()
            await asyncio.sleep(0)

        if not window.close_window:
            game = Game(menu.server, menu.client, window.size, menu.selected_map, menu.server_addr_ip, menu.selected_characters)
            menu.unload()

        while not (window.close_window or game.end):
            window.update()
            if is_window_resized():
                window.update_size()    
                game.update_draw_scale(window.size)

            if game.server:
                game.tick += get_frame_time()
                while game.tick >= GAME_TICK:
                    game.update_tick(GAME_TICK)

            if game.client:
                game.update_client()

            game.update_frame()
            game.draw()
        
            await asyncio.sleep(0)
        
        if not window.close_window:
            game.unload()

    close_audio_device()
    close_window()

if __name__ == "__main__":
    asyncio.run(main())
