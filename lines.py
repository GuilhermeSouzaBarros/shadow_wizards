from pyray  import *
from raylib import *
from math import isnan

from vectors import Vector2, Domain
from utils import *


class Line:
    def __init__(self, direction:Vector2, point:Vector2, limit_t:Domain=Domain(0.0, 1.0)) -> None:
        self.direction = direction
        self.point     = point
        self.limit_t   = limit_t
        self._domain    = self.domain()

    @property
    def __str__(self):
        return f"P = ({self.point.x:.2f}, {self.point.y:.2f}) + t({self.direction.__str__}) / {self.limit_t.x:.2f} <= t <= {self.limit_t.y:.2f}"

    def domain(self) -> Domain:    
        dom = {'x': Domain(self.point.x + self.limit_t.x * self.direction.x,
                           self.point.x + self.limit_t.y * self.direction.x),
               'y': Domain(self.point.y + self.limit_t.x * self.direction.y,
                           self.point.y + self.limit_t.y * self.direction.y)}      
        if isnan(dom['x'].a):
            dom['x'] = Domain(self.point.x, self.point.x)
        if isnan(dom['y'].a):
            dom['y'] = Domain(self.point.y, self.point.y)
        return dom

    def has_point(self, point:Vector2) -> int:

        #has = ((self._domain['x'].a - SMALL_FLOAT <= point.x and point.x <= self._domain['x'].b + SMALL_FLOAT) and
        #       (self._domain['y'].a - SMALL_FLOAT <= point.y and point.y <= self._domain['y'].b + SMALL_FLOAT))
        has = ((self._domain['x'].a <= point.x and point.x <= self._domain['x'].b) and
               (self._domain['y'].a <= point.y and point.y <= self._domain['y'].b))
        return has

    def is_point_above(self, point:Vector2) -> int:
        """Here above is the direction after a 90 degree anticlockwise rotation"""

        above_line_dir = Vector2(self.direction.x, self.direction.y)
        above_line_dir.rotate_90_anti()
        above_line = Line(above_line_dir, point, Vector2(float('-inf'), float('inf')))

        intersection = ColLines(self, above_line)

        return (intersection.did_intersect and intersection.t_line_2 < 0.0)

    def point_distance(self, point:Vector2) -> Vector2:
        perpendicular_line_dir = Vector2(self.direction.x, self.direction.y)
        perpendicular_line_dir.rotate_90_anti()
        perpendicular_line = Line(perpendicular_line_dir, point, Vector2(float('-inf'), float('inf')))

        intersection = ColLines(self, perpendicular_line)

        return (intersection.point - point)

    def is_parallel(self, other_line):
        if (self.direction.x and self.direction.y and other_line.direction.x and other_line.direction.y):
            ratio = Vector2(self.direction.x / other_line.direction.x, self.direction.y / other_line.direction.y)
            return ratio.x == ratio.y
        else:
            return not ((self.direction.x or other_line.direction.x) and (self.direction.y or other_line.direction.y))
        
    def draw(self, map_offset:Vector2, scaler:float, color:Color):
        s_pos = [
            map_offset.x + scaler * self.point.x,
            map_offset.y + scaler * self.point.y
        ]
        e_pos = [
            map_offset.x + scaler * (self.point.x + self.direction.x * self.limit_t.b),
            map_offset.y + scaler * (self.point.y + self.direction.y * self.limit_t.b)
        ]
        draw_line_v(s_pos, e_pos, color)


class ColLines:
    def __init__(self, line_1:Line, line_2:Line) -> None:
        self.point = Vector2(0.0, 0.0)
        self.t_line_1 = 0.0
        self.t_line_2 = 0.0
        self.parallel = False
        self.did_intersect = False
        self.intersection(line_1, line_2)
    
    def intersection(self, line_1:Line, line_2:Line) -> None:
        denominador = (line_1.direction.y * line_2.direction.x -
                       line_1.direction.x * line_2.direction.y)

        vec_points = Vector2(line_1.point.x - line_2.point.x,
                             line_1.point.y - line_2.point.y)
        
        is_equal = line_1.direction.x * vec_points.y == line_1.direction.y * vec_points.x

        if eq_z(denominador):
            self.parallel = 1
            self.did_intersect = is_equal
            return
        
        self.t_line_1 = (line_2.direction.y * (vec_points.x) -
                         line_2.direction.x * (vec_points.y))
        self.t_line_1 /= denominador

        self.point.x = line_1.direction.x * self.t_line_1 + line_1.point.x
        self.point.y = line_1.direction.y * self.t_line_1 + line_1.point.y

        if line_2.direction.x:
            self.t_line_2 = (self.point.x - line_2.point.x) / line_2.direction.x
        else:
            self.t_line_2 = (self.point.y - line_2.point.y) / line_2.direction.y
 
        self.did_intersect = line_1.has_point(self.point) and line_2.has_point(self.point)
