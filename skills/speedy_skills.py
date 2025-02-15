from skills.skill import *

class Dash(Skill):
    def __init__(self) -> None:
        """
        Herda Skill. Atributo speed_multiplicator é usado para dar um impuslo
        no player caso a skill dash seja usada
        """
        super().__init__()
        self.speed_multiplier = 25.0
        self._cooldown = 1.25
        self.duration = 0.15

    def encode(self) -> bytes:
        return "".encode()
    
    def decode(self, bytes_string:bytes) -> int:
        return 0

    def update(self, *args) -> None:
        activate = self.skill_key(args[0], args[1], 1, args[2])
        
        if self.can_deactivate():
            self.deactivate() 

    def draw(self, *args) -> None:
        pass

class SuperSpeed(Skill):
    def __init__(self) -> None:
        super().__init__()
        self.speed_multiplier = 8.0
        self.is_activated = True

    def encode(self) -> bytes:
        return "".encode()
    
    def decode(self, bytes_string:bytes) -> int:
        return 0
    
    def deactivate(self):
        pass

    def update(self, *args) -> None:
        pass

    def draw(self, *args) -> None:
        pass