from pyray import *
from raylib import *

from config import *
from skills import *


class Character():
    def __init__(self, character_id:int, pos:Vector2)->None:
        self.pos = pos
        self.skill = self.choose_character(character_id)

    def choose_character(self, character_id) -> Skill:
        """
        Recebe um id correspondendo ao personagem escolhido e retorna a Habilidade dele
        """
        if character_id == CHARACTER_RED["id"]:
            skill = Fireball(self.pos)
            self.skill_name = "Flames"
            self.color = RED
        elif character_id == CHARACTER_BLUE["id"]:
            skill = Dash()
            self.skill_name = "Dash"
            self.color = BLUE
        elif character_id == CHARACTER_PINK["id"]:
            skill = Gun(self.pos)
            self.skill_name = "Gun"
            self.color = PINK
        elif character_id == CHARACTER_LIME["id"]:
            skill = Traps(self.pos)
            self.skill_name = "Trap"
            self.color = LIME
        elif character_id == CHARACTER_GOLD["id"]:
            skill = SuperSpeed()
            self.skill_name = "Speed"
            self.color = GOLD
        elif character_id == CHARACTER_YELLOW["id"]:
            skill = Intangibility()
            self.skill_name = "Intangibility"
            self.color = YELLOW
        elif character_id == CHARACTER_DARKGREEN["id"]:
            skill = Parry()
            self.skill_name = "Parry"
            self.color = GREEN
        elif character_id == CHARACTER_PURPLE["id"]:
            skill = Ray()
            self.skill_name = "RAY"
            self.color = PURPLE

        return skill