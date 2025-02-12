from pyray import *
from raylib import *

from random import randint

class Music:
    def __init__(self):
        tracks = ["sounds/future-beat.mp3",
                  "sounds/hip-hop-beat.mp3",
                  "sounds/old-school-hit-hop.mp3"]
        track_idx = randint(0, 2)

        self.soundtrack = load_music_stream(tracks[track_idx])
        play_music_stream(self.soundtrack)

    def update(self):
        update_music_stream(self.soundtrack)

    def unload(self):
        unload_music_stream(self.soundtrack)
