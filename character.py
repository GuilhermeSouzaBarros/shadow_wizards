from pyray import *
from raylib import *

from skills import *

class Character():
    def __init__(self, id:int, pos:Vector2)->None:
        self.color = RED
        self.pos = pos
        self.skill = self.choose_character(id)
        self.skill_name

    def choose_character(self, character_id) -> Skill:
        """
        Recebe um id correspondendo ao personagem escolhido e retorna a Habilidade dele
        """
        if character_id == 0:
            skill = Fireball(self.pos)
            self.skill_name = "Flames"
            self.color = RED
        elif character_id == 1:
            skill = Dash()
            self.skill_name = "Dash"
            self.color = BLUE
        elif character_id == 2:
            skill = Gun(self.pos)
            self.skill_name = "Gun"
            self.color = PINK
        elif character_id == 3:
            skill = Traps(self.pos)
            self.skill_name = "Trap"
            self.color = LIME
        elif character_id == 4:
            skill = SuperSpeed()
            self.skill_name = "Speed"
            self.color = GOLD
        elif character_id == 5:
            skill = Intangibility()
            self.skill_name = "Intangibility"
            self.color = YELLOW
        elif character_id == 6:
            skill = Parry()
            self.skill_name = "Parry"
            self.color = GREEN
        elif character_id == 7:
            skill = Ray()
            self.skill_name = "RAY"
            self.color = PURPLE

        return skill