from skills.skill import *

class Dash(Skill):
    def __init__(self) -> None:
        """
        Herda Skill. Atributo speed_multiplicator é usado para dar um impuslo
        no player caso a skill dash seja usada
        """
        super().__init__()
        self.speed_multiplier = 20.0
        self._cooldown = 1
        self.duration = 0.1


    def update(self, *args) -> None:
        current_time = get_time()
        if (is_key_pressed(KEY_E) and 
            current_time - self.last_activation > self._cooldown):
            self.activate(*args)
        if current_time - self.last_activation > self.duration:
            self.deactivate() 

    def draw(self, *args) -> None:
        pass

class SuperSpeed(Skill):
    def __init__(self) -> None:
        super().__init__()
        self.speed_multiplier = 6.0
        self.is_activated = True

    def update(self, *args) -> None:
        pass

    def draw(self, *args) -> None:
        pass