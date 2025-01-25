from abc import ABC, abstractmethod
from pyray import *
from raylib import *
from shapes import Circle, Rectangle as Rec
from imaginary import Imaginary
from vectors import Vector2, Domain
from lines import *

class Skill(ABC):
    def __init__(self) -> None:
        """
        Atributos essenciais para todas as habilidades
        """
        self.last_activation = 0
        self.is_activated = False
        self.duration = None
        self._cooldown = 0.3
        

    def can_activate(self) -> bool:
        return get_time() - self.last_activation > self._cooldown

    def activate(self, *args) -> None:
        if self.can_activate():
            self.last_activation = get_time()
            self.is_activated = True

    def can_deactivate(self) -> bool:
        if self.duration is None:
            return False
        return get_time() - self.last_activation > self.duration

    def deactivate(self) -> None:
        self.is_activated = False


    @abstractmethod
    def update(self, *args) -> None:
        """
        Atualiza estado da habilidade de acordo 
        com suas características
        """
        pass

    @abstractmethod
    def draw(self, *args) -> None:
        """
        Desenha a habilidade correspondente
        """
        pass