import asyncio
from pyray import *

import game

TICK = 0.01

async def main():
    env = game.Game()

    while not env.close_window:
        env.tick += get_frame_time()
        while env.tick >= TICK:
            env.update(TICK)
            env.tick -= TICK
        env.draw()
        await asyncio.sleep(0)

    close_window()

if __name__ == "__main__":
    asyncio.run(main())
