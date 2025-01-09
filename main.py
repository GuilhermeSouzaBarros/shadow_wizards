import asyncio
from pyray import *

from window import Window
from home_screen import HomeScreen
from game import Game

TICK = 0.0078125 #128 ticks por segundo

async def main():
    window = Window()

    while not window.close_window:

        menu = HomeScreen(window.size)
        while not (menu.start_game or window.close_window):
            menu.update()
            
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
            game.tick += get_frame_time()
            while game.tick >= TICK:
                game.update_tick(TICK)
                game.tick -= TICK

            window.update()
            if is_window_resized():
                window.update_size()
                game.update_draw_scale(window.size)

            game.update_frame()

            game.draw()
            await asyncio.sleep(0)
        
        if not window.close_window:
            game.unload()

    close_window()


if __name__ == "__main__":
    asyncio.run(main())
