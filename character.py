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
            skill = Trap()
            self.skill_name = "Trap"
            self.color = YELLOW

        return skill