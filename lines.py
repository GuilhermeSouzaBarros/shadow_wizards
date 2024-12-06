from vectors import Domain
from aux import *

from pyray  import *
from raylib import *

class Line:
    def __init__(self, direction:Vector2, point:Vector2, limit_t:Domain) -> None:
        self.direction = direction
        self.point     = point
        self.limit_t   = limit_t
        self.domain    = self.domain()

    def domain(self) -> Domain:    
        dom = {'x': Domain(self.point.x + self.limit_t.x * self.direction.x,
                           self.point.x + self.limit_t.y * self.direction.x),
               'y': Domain(self.point.y + self.limit_t.x * self.direction.y,
                           self.point.y + self.limit_t.y * self.direction.y)}
        
        return dom

    def has_point(self, point):
         return ((self.domain['x'].x <= point.x and point.x <= self.domain['x'].y) and
                 (self.domain['y'].x <= point.y and point.y <= self.domain['y'].y))


class ColLines:
    def __init__(self, line_1:Line, line_2:Line) -> None:
        self.point = Vector2(0.0, 0.0)
        self.t_1 = 0.0
        self.t_2 = 0.0
        self.parallel = False
        self.did_intercect = False
        self.intersection(line_1, line_2)
    
    def intersection(self, line_1:Line, line_2:Line) -> None:
        denominador = line_1.dir.y * line_2.dir.x - line_1.dir.x * line_2.dir.y

        vec_points = Vector2(line_1.point.x - line_2.point.x, line_1.point.y - line_2.point.y)
        is_equal = line_1.dir.x * vec_points.y == line_1.dir.y * vec_points.y

        if eq_z(denominador):
            self.parallel = 1
            self.coll = is_equal
            return
        
        self.t_line_2 = (line_1.dir.y * (line_1.point.x - line_2.point.x) -
                    line_1.dir.x * (line_1.point.y - line_2.point.y))
        self.t_line_2 /= denominador

        self.point.x = line_2.dir.x * self.t_line_2 + line_2.point.x
        self.point.y = line_2.dir.y * self.t_line_2 + line_2.point.y

        if line_1.dir.x:
            self.t_line_1 = (self.point.x - line_1.point.x) / line_1.dir.x
        else:
            self.t_line_1 = (self.point.y - line_1.point.y) / line_1.dir.y
 
        self.coll = line_1.has_point(self.point) and line_2.has_point(self.point)