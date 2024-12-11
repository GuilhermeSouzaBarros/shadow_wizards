class Imaginary():
    def __init__(self, real:float=1.0, imaginary:float=0.0):
        self.real      = real
        self.imaginary = imaginary
    
    def __add__(self, other):
        return Imaginary(self.real      + other.real,
                         self.imaginary + other.imaginary)
    
    def __sub__(self, other):
        return Imaginary(self.real      - other.real,
                         self.imaginary - other.imaginary)
    
    def __mul__(self, other):
        real      = (self.real * other.real -
                     self.imaginary * other.imaginary)
        imaginary = (self.real * other.imaginary +
                     other.real * self.imaginary)
        return Imaginary(real, imaginary)