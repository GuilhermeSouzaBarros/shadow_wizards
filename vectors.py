class Vector2:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def module(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def swap_xy(self):
        aux = self.x
        print(type(aux))
        self.x = self.y
        self.y = aux
    
class Domain(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        if y < x:
            self.x = y
            self.y = x

    @property
    def a(self):
        return self.x
    
    @a.setter
    def a(self, a):
        self.x = a

    @property
    def b(self):
        return self.x
    
    @b.setter
    def a(self, a):
        self.x = a
    
