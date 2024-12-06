from pyray  import *
from raylib import *

from typing import List

from vectors import Vector2
from lines import Line, Domain, ColLines

class Shape:
    def __init__(self, position:Vector2) -> None:
        self.position = position
        self.speed    = Vector2(0.0, 0.0)

    def delta_position(self, delta_time:float) -> None:
        self.position.x += (self.speed.x * delta_time)
        self.position.y += (self.speed.y * delta_time)
    
    def next_position(self, delta_time:float) -> Vector2:
        next_pos = Vector2(self.position.x, self.position.y)
        next_pos.x += self.speed.x * delta_time
        next_pos.y += self.speed.y * delta_time
        return next_pos

class Rectangle(Shape):
    def __init__(self, position:Vector2, size:Vector2) -> None:
        super().__init__(position)
        self.size  = size
        self.radio = (self.size.x ** 2 + self.size.y ** 2) ** 0.5
    
    def to_lines(self) -> List[Line]:
        lines = []
        hsize = Vector2(self.size.y / 2, self.size.x / 2)

        lines.append(Line(
            Vector2(self.size.x, 0.0),
            Vector2(self.position.x - hsize.x, self.position.y - hsize.y), 
            Domain(0.0, 1.0)))

        lines.append(Line(Vector2(0.0, self.size.y),
            Vector2(self.position.x + hsize.x, self.position.y - hsize.y),
            Domain(0.0, 1.0)))
        
        lines.append(Line(
            Vector2(-self.size.x, 0.0), 
            Vector2(self.position.x + hsize.x, self.position.y + hsize.y), 
            Domain(0.0, 1.0)))
        
        lines.append(Line(
            Vector2(0.0, -self.size.y), 
            Vector2(self.position.x - hsize.x, self.position.y + hsize.y), 
            Domain(0.0, 1.0)))

        return lines

    def collision_line(self, line:Line) -> ColLines:
        rec_lines = self.to_lines()
        colls = [ColLines(line, rec_lines[0]),
                 ColLines(line, rec_lines[1]),
                 ColLines(line, rec_lines[2]),
                 ColLines(line, rec_lines[3])]

        t_menor = colls[0]
        for i in range(1, 4):
            if (colls[i].coll and colls[i].t_1 < t_menor.t_1):
                t_menor = colls[i]

        return t_menor

class Circle(Shape):
    def __init__(self, position:Vector2, radio:float) -> None:
        super().__init__(position)
        self.radio = radio

    def collision_line(self, line:Line, delta_time:float) -> dict:
        next_pos_circle = self.next_position(delta_time)
        info = {'instersections': 0}

        #equação de segundo grau para achar t em P = A + tV
        
        a = (line.direction.x) ** 2 + (line.direction.y) ** 2
        b = 2 * (line.direction.x * (line.point.x - next_pos_circle.x) +
                 line.direction.y * (line.point.y - next_pos_circle.y))
        c = ((line.point.x - next_pos_circle.x) ** 2 +
             (line.point.y - next_pos_circle.y) ** 2 -
             (self.radio) ** 2)

        delta = b ** 2 - 4 * a * c
        if (delta < 0.0):
            return info

        t_1 = (-b + delta ** 0.5) / (2 * a)
        t_2 = (-b - delta ** 0.5) / (2 * a)

        info.update({"point_1":
            Vector2(line.point.x + t_1 * line.direction.x,
                    line.point.y + t_1 * line.direction.y)})
        
        info.update({"point_2":
            Vector2(line.point.x + t_2 * line.direction.x,
                    line.point.y + t_2 * line.direction.y)})
        
        info['instersections'] = (line.has_point(info["point_1"]) +
                                 line.has_point(info["point_2"]))
        return info