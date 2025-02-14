from pyray import *
from raylib import *

from random import choice

class Music:
    def __init__(self):
        tracks = ["sounds/future-beat.mp3",
                  "sounds/hip-hop-beat.mp3",
                  "sounds/old-school-hit-hop.mp3"]

        self.soundtrack = load_music_stream(choice(tracks))
        #play_music_stream(self.soundtrack)

    def update(self):
        return
        update_music_stream(self.soundtrack)

    def unload(self):
        unload_music_stream(self.soundtrack)
