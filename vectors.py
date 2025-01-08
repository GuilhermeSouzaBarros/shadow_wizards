class Vector2:
    def __init__(self, x:float, y:float) -> None:
        """!!! Raylib Y axis increases downwards !!!"""
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, value:float):
        return Vector2(self.x * value, self.y * value)

    def __truediv__(self, value:float):
        return Vector2(self.x / value, self.y / value)

    @property
    def __str__(self):
        return f"{self.x:.2f} / {self.y:.2f}"

    def module(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def to_module(self, value:float=1.0) -> None:
        module = self.module()
        if (module):
            self.x *= value / module
            self.y *= value / module

    def swap_xy(self) -> None:
        aux = self.x
        self.x = self.y
        self.y = aux
    
    def rotate_90_anti(self) -> None:
        aux = self.x
        self.x = self.y
        self.y = -aux

    def copy(self):
        return Vector2(self.x, self.y)
    
    def to_list(self):
        return [self.x, self.y]
    

class Domain(Vector2):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y)
        if y < x:
            self.x = y
            self.y = x
        else:
            self.x = x
            self.y = y

    @property
    def a(self) -> float:
        return self.x
    
    @a.setter
    def a(self, a:float) -> None:
        self.x = a


    @property
    def b(self) -> float:
        return self.y
    
    @b.setter
    def b(self, b:float) -> None:
        self.y = b
    