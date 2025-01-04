import asyncio
from pyray import *

from window import Window
from vectors import Vector2
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
            game = Game(window.size, menu.selected_map, menu.selected_skin)
        while not window.close_window:
            game.tick += get_frame_time()
            while game.tick >= TICK and not game.end:
                game.update_tick(TICK)
                game.tick -= TICK

            if game.end:
                break

            window.update()
            if is_window_resized():
                window.update_size()
                game.update_draw_scale(window.size)

            game.update_frame()

            game.draw()
            await asyncio.sleep(0)
        

    close_window()


if __name__ == "__main__":
    asyncio.run(main())
