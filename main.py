import asyncio
from pyray import *

import game

TICK = 0.0078125 #128 ticks por segundo

async def main():
    env = game.Game()
    print("\n\n")

    while not env.close_window:
        env.tick += get_frame_time()
        while env.tick >= TICK:
            env.update_tick(TICK)
            env.tick -= TICK
        env.update_frame()
        env.draw()
        await asyncio.sleep(0)

    close_window()


if __name__ == "__main__":
    asyncio.run(main())
