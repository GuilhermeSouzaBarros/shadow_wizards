from skills.skill import *

class Shield(Skill):
    def __init__(self):
        super().__init__()
        self._cooldown = 1
        self.duration = 2

    def encode(self) -> bytes:
        message = pack("?", self.is_activated)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        data = unpack("?", bytes_string[0:1])
        self.is_activated = data[0]
        return 1
    
    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, *args) -> None:
        activate = self.skill_key(player_pos, angle, 1, player_input)
        if self.can_deactivate():
            self.deactivate()

    def draw(self, *args) -> None:
        pass