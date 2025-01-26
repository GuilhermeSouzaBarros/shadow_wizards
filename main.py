import asyncio
from pyray import *

from config import GAME_TICK
from window import Window
from menu import Menu
from game import Game

async def main():
    window = Window()

    while not window.close_window:

        menu = Menu(window.size)
        while not (menu.start_game or window.close_window):
            menu.update()
            
            window.close_window = menu.close_window
            window.update()
            if is_window_resized():
                window.update_size()
                menu.update_scale(window.size)

            menu.draw()
            await asyncio.sleep(0)

        if not window.close_window:
            print(f"map_id: {menu.selected_map}\ncaracter_id: {menu.selected_caracter}")
            game = Game(window.size, menu.selected_map, menu.selected_caracter)
            menu.unload()

        while not (window.close_window or game.end):
            window.update()
            if is_window_resized():
                window.update_size()    
                game.update_draw_scale(window.size)

            game.tick += get_frame_time()
            while game.tick >= GAME_TICK:
                game.update_tick(GAME_TICK)
                game.tick -= GAME_TICK

            game.update_frame()
            game.draw()
        
            await asyncio.sleep(0)
        
        if not window.close_window:
            game.unload()

    close_window()


if __name__ == "__main__":
    asyncio.run(main())
