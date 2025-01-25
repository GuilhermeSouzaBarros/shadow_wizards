from skills.skill import *

class Intangibility(Skill):
    def __init__(self) -> None:
        super().__init__()
        self._cooldown = 5
        self.duration = 3
        self.in_wall = False


    def update(self, player_pos:Vector2, angle:Imaginary, *args) -> None:
        if is_key_pressed(KEY_E):
            self.activate()

        current_time = get_time()
        if current_time - self.last_activation > self.duration:
            self.deactivate()


    def draw(self, *args) -> None:
        pass