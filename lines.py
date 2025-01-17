from pyray  import *
from raylib import *
from math import isnan

from vectors import Vector2, Domain
from imaginary import Imaginary
from utils import *


class Line:
    def __init__(self, direction:Vector2, point:Vector2, limit_t:Domain=Domain(0.0, 1.0)) -> None:
        self._direction = direction
        self._point     = point
        self._limit_t   = limit_t
        self._domain    = self.domain()

    @property
    def direction(self) -> Vector2:
        return self._direction
    
    @direction.setter
    def direction(self, direction:Vector2) -> None:
        self._direction = direction
        self._domain = self.domain()

    @property
    def point(self):
        return self._point
    
    @point.setter
    def point(self, point:Vector2) -> None:
        self._point = point
        self._domain = self.domain()
    
    @property
    def limit_t(self):
        return self._limit_t
    
    @limit_t.setter
    def limit_t(self, limit_t:Domain) -> None:
        self._limit_t = limit_t
        self._domain = self.domain()

    @property
    def __str__(self):
        return f"P = ({self.point.x:.2f}, {self.point.y:.2f}) + t({self.direction.__str__}) / {self.limit_t.x:.2f} <= t <= {self.limit_t.y:.2f}"

    def domain(self) -> Domain:    
        dom = {'x': Domain(self.point.x + self.limit_t.x * self.direction.x,
                           self.point.x + self.limit_t.y * self.direction.x),
               'y': Domain(self.point.y + self.limit_t.x * self.direction.y,
                           self.point.y + self.limit_t.y * self.direction.y)}
        if isnan(dom['x'].a):
            dom['x'].a = self.point.x
        if isnan(dom['y'].a):
            dom['y'].a = self.point.y
        if isnan(dom['x'].b):
            dom['x'].b = self.point.x
        if isnan(dom['y'].b):
            dom['y'].b = self.point.y
        return dom

    def has_point(self, point:Vector2) -> int:
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
        
    def reflection_angle(self, other_line) -> Imaginary:
        self_angle = Imaginary(-self.direction.x, -self.direction.y, 1)
        other_angle = Imaginary(other_line.direction.x, other_line.direction.y, 1)

        relative_angle = self_angle / other_angle
        other_angle *= Imaginary(-1, 0)
        
        return other_angle / relative_angle

    def draw(self, map_offset:Vector2, scaler:float, color:Color):
        s_pos = map_offset + (self.point + self.direction * self.limit_t.a) * scaler
        e_pos = map_offset + (self.point + self.direction * self.limit_t.b) * scaler
        draw_line_v(s_pos.to_list(), e_pos.to_list(), color)


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
                         line_2.direction.x * (vec_points.y)) / denominador

        self.point = line_1.direction * self.t_line_1 + line_1.point

        if line_2.direction.x:
            self.t_line_2 = (self.point.x - line_2.point.x) / line_2.direction.x
        else:
            self.t_line_2 = (self.point.y - line_2.point.y) / line_2.direction.y
 
        self.did_intersect = line_1.has_point(self.point) and line_2.has_point(self.point)
