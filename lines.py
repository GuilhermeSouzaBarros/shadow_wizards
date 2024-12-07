from pyray  import *
from raylib import *

from vectors import Vector2, Domain
from aux import *


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

    def has_point(self, point:Vector2) -> int:
         return ((self.domain['x'].a <= point.x and point.x <= self.domain['x'].b) and
                 (self.domain['y'].a <= point.y and point.y <= self.domain['y'].b))

    def is_point_above(self, point:Vector2) -> int:
        """Here above is defined as the direction of the line after a 90 degree anticlockwise rotation"""

        above_line = Line(Vector2(self.direction.x, self.direction.y), point, Vector2(float('-inf'), float('inf')))
        above_line.direction.rotate_90_anti()

        intersection = ColLines(self, above_line)

        dir_point_line = Vector2(point.x - intersection.point.x, point.y - intersection.point.y)

        "This works because rectangle lines currently are axis aligned"
        return (dir_point_line.x * above_line.direction.x >= 0.0) and (dir_point_line.y * above_line.direction.y >= 0.0)


class ColLines:
    def __init__(self, line_1:Line, line_2:Line) -> None:
        self.point = Vector2(0.0, 0.0)
        self.t_1 = 0.0
        self.t_2 = 0.0
        self.parallel = False
        self.did_intercect = False
        self.intersection(line_1, line_2)
    
    def intersection(self, line_1:Line, line_2:Line) -> None:
        denominador = line_1.direction.y * line_2.direction.x - line_1.direction.x * line_2.direction.y

        vec_points = Vector2(line_1.point.x - line_2.point.x, line_1.point.y - line_2.point.y)
        is_equal = line_1.direction.x * vec_points.y == line_1.direction.y * vec_points.y

        if eq_z(denominador):
            self.parallel = 1
            self.coll = is_equal
            return
        
        self.t_line_2 = (line_1.direction.y * (line_1.point.x - line_2.point.x) -
                    line_1.direction.x * (line_1.point.y - line_2.point.y))
        self.t_line_2 /= denominador

        self.point.x = line_2.direction.x * self.t_line_2 + line_2.point.x
        self.point.y = line_2.direction.y * self.t_line_2 + line_2.point.y

        if line_1.direction.x:
            self.t_line_1 = (self.point.x - line_1.point.x) / line_1.direction.x
        else:
            self.t_line_1 = (self.point.y - line_1.point.y) / line_1.direction.y
 
        self.coll = line_1.has_point(self.point) and line_2.has_point(self.point)