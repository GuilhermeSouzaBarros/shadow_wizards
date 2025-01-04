from pyray import *
from raylib import *

from config import *
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
        if character_id == RED_SKIN_ID:
            skill = Fireball(self.pos)
            self.skill_name = "Flames"
            self.color = RED
        elif character_id == BLUE_SKIN_ID:
            skill = Dash()
            self.skill_name = "Dash"
            self.color = BLUE
        elif character_id == PINK_SKIN_ID:
            skill = Gun(self.pos)
            self.skill_name = "Gun"
            self.color = PINK
        elif character_id == LIME_SKIN_ID:
            skill = Traps(self.pos)
            self.skill_name = "Trap"
            self.color = LIME
        elif character_id == GOLD_SKIN_ID:
            skill = SuperSpeed()
            self.skill_name = "Speed"
            self.color = GOLD
        elif character_id == YELLOW_SKIN_ID:
            skill = Intangibility()
            self.skill_name = "Intangibility"
            self.color = YELLOW
        elif character_id == DARKGREEN_SKIN_ID:
            skill = Parry()
            self.skill_name = "Parry"
            self.color = GREEN
        elif character_id == PURPLE_SKIN_ID:
            skill = Ray()
            self.skill_name = "RAY"
            self.color = PURPLE

        return skill