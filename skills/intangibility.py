from skills.skill import *

class Intangibility(Skill):
    def __init__(self) -> None:
        super().__init__()
        self._cooldown = 5
        self.duration = 3
        self.in_wall = False


    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, *args) -> None:
        activate = self.skill_key(player_pos, angle, 1, player_input)

        current_time = get_time()
        if current_time - self.last_activation > self.duration:
            self.deactivate()


    def draw(self, *args) -> None:
        pass