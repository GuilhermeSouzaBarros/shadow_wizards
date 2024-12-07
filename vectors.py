class Vector2:
    def __init__(self, x:float, y:float) -> None:
        """!!! Raylib Y axis increases downwards !!!"""
        self.x = float(x)
        self.y = float(y)
    
    def module(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def to_module(self, value:float) -> None:
        module = self.module()
        if (module):
            self.x *= value / module
            self.y *= value / module

    def swap_xy(self) -> None:
        aux = self.x
        print(type(aux))
        self.x = self.y
        self.y = aux
    
    def rotate_90_anti(self) -> None:
        aux = self.x
        self.x = self.y
        self.y = -aux
    
class Domain(Vector2):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y
        if y < x:
            self.x = y
            self.y = x

    @property
    def a(self) -> None:
        return self.x
    
    @a.setter
    def a(self, a:float) -> None:
        self.x = a

    @property
    def b(self) -> None:
        return self.y
    
    @b.setter
    def b(self, b:float) -> None:
        self.y = b
    