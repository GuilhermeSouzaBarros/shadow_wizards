from math import atan2, degrees

class Imaginary():
    def __init__(self, real:float=1.0, imaginary:float=0.0, to_module:float=0.0):
        """to_module = 0 means no change"""
        self.real      = real
        self.imaginary = imaginary

        if (real or imaginary) and to_module:
            module = (real ** 2 + imaginary ** 2) ** 0.5
            self.real *= to_module / module
            self.imaginary *= to_module / module
    
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
    
    def __truediv__(self, other):
        if not (other.real or other.imaginary):
            raise ZeroDivisionError
        denominator = other.real ** 2 + other.imaginary ** 2
        real = (self.real * other.real + self.imaginary * other.imaginary) / denominator
        imaginary = (self.imaginary * other.real - self.real * other.imaginary) / denominator
        return Imaginary(real, imaginary)

    @property
    def __str__(self) -> str:
        return f"{self.real:.2f} + {self.imaginary:.2f}i / {self.to_degree()}"

    def to_degree(self) -> float:
        return degrees(atan2(self.imaginary, self.real))

    def copy(self):
        return Imaginary(self.real, self.imaginary)
    