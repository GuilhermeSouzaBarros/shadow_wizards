from raylib import *
from pyray import *

from config import *

class Window:
    def __init__(self):
        set_config_flags(FLAG_MSAA_4X_HINT)
        set_config_flags(FLAG_WINDOW_RESIZABLE)

        init_window(0, 0, GAME_TITLE)

        full_size = [get_monitor_width(0), get_monitor_height(0)]
        self.size = [int(full_size[0] * 0.8), int(full_size[1] * 0.8)]
        self.pos = (int(full_size[0] * 0.1), int(full_size[1] * 0.1))


        set_window_min_size(int(self.size[0] * 0.5), int(self.size[1] * 0.5))
        set_window_size(self.size[0], self.size[1])
        set_window_position(self.pos[0], self.pos[1])
        set_target_fps(get_monitor_refresh_rate(get_current_monitor()))
        set_exit_key(KEY_DELETE)


        self.close_window = False

    def update_size(self) -> None: 
        window = get_window_handle()
        new_width = ffi.new('int *', 1)
        new_height = ffi.new('int *', 1)
        glfw_get_window_size(window, new_width, new_height)
        self.size[0] = int(ffi.unpack(new_width,  ffi.sizeof(new_width) )[0])
        self.size[1] = int(ffi.unpack(new_height, ffi.sizeof(new_height))[0])
        ffi.release(new_width)
        ffi.release(new_height)

    def update(self) -> None:
        if (is_key_pressed(KEY_F11)):
            ToggleFullscreen()
        self.close_window = self.close_window or window_should_close()
        