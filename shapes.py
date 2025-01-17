from pyray  import *
from raylib import *
from math import atan2, degrees

from typing import List

from utils import sign_of
from imaginary import Imaginary
from vectors import Vector2
from lines import Line, ColLines

class Shape:
    def __init__(self, position:Vector2, angle:Imaginary=Imaginary(), speed:Vector2=Vector2(0, 0)) -> None:
        self._position = position
        self.speed    = speed
        self._angle    = angle

    @property
    def position(self) -> Vector2: 
        return self._position
    
    @position.setter
    def position(self, new_position:Vector2) -> None:
        self._position = new_position

    @property
    def angle(self) -> Imaginary:
        return self._angle

    @angle.setter
    def angle(self, new_angle:Imaginary) -> None:
        self._angle = new_angle

    def delta_position(self, delta_time:float) -> None:
        change = self.speed.copy()
        change.x *= delta_time
        change.y *= delta_time
        self.position += change

    def next_position(self, delta_time:float) -> Vector2:
        next_pos = self._position.copy()
        next_pos.x += self.speed.x * delta_time
        next_pos.y += self.speed.y * delta_time
        return next_pos

    def copy(self):
        return Shape(self._position.copy(), self._angle.copy())

class Rectangle(Shape):
    def __init__(self, position:Vector2, size:Vector2, angle:Imaginary=Imaginary(), speed:Vector2=Vector2(0, 0)) -> None:
        super().__init__(position, angle, speed)
        self._size   = size
        self.inner_radius = 0
        self.outer_radius = 0
        self.att_radius()
        self.lines  = self.to_lines()
    
    @property
    def position(self) -> Vector2: 
        return self._position
    
    @position.setter
    def position(self, new_position:Vector2) -> None:
        self._position = new_position
        self.lines = self.to_lines()

    @property
    def angle(self) -> Imaginary:
        return self._angle

    @angle.setter
    def angle(self, new_angle:Imaginary) -> None:
        self._angle = new_angle
        self.lines = self.to_lines()

    @property
    def size(self) -> Vector2:
        return self._size
    
    @size.setter
    def size(self, new_size:Vector2):
        self._size = new_size
        self.to_lines()
        self.att_radius()

    def att_radius(self):
        self.inner_radius = min(self.size.x, self.size.y) / 2.0
        self.outer_radius = ((self.size.x ** 2 + self.size.y ** 2) ** 0.5) / 2.0

    def copy(self):
        return Rectangle(self.position.copy(), self.size.copy(), self.angle.copy(), self.speed)

    def distance_to_side(self, angle:Imaginary) -> Vector2:
        relative_angle = angle / self.angle
        angle_size = Vector2(abs(relative_angle.imaginary * self.size.x),
                             abs(relative_angle.real * self.size.y))
        
        if angle_size.x < angle_size.y:
            ratio = relative_angle.imaginary / relative_angle.real
            return Vector2(sign_of(relative_angle.real) * self.size.x * 0.5,  ratio * self.size.x * 0.5)
        else:
            ratio = relative_angle.real / relative_angle.imaginary
            return Vector2(ratio * self.size.y * 0.5, sign_of(relative_angle.imaginary) * self.size.y * 0.5)
        
    def to_lines(self) -> List[Line]:
        size_im_x = Imaginary(self.size.x / 2.0, 0.0) * self.angle
        size_im_y = Imaginary(0.0, self.size.y / 2.0) * self.angle
        
        corners = [
            Vector2(self.position.x - size_im_x.real      - size_im_y.real,
                    self.position.y - size_im_x.imaginary - size_im_y.imaginary), #upper_left
            Vector2(self.position.x + size_im_x.real      - size_im_y.real,
                    self.position.y + size_im_x.imaginary - size_im_y.imaginary), #upper_right
            Vector2(self.position.x + size_im_x.real      + size_im_y.real,
                    self.position.y + size_im_x.imaginary + size_im_y.imaginary), #bottom_right
            Vector2(self.position.x - size_im_x.real      + size_im_y.real,
                    self.position.y - size_im_x.imaginary + size_im_y.imaginary)] #bottom_left
        
        size_im_x = Imaginary(self.size.x, 0.0) * self.angle
        size_im_y = Imaginary(0.0, self.size.y) * self.angle

        lines = [
            Line(
                Vector2(size_im_x.real, size_im_x.imaginary),
                corners[0]
            ),
            Line(
                Vector2(size_im_y.real, size_im_y.imaginary),
                corners[1]
            ),
            Line(
                Vector2(-size_im_x.real, -size_im_x.imaginary),
                corners[2]
            ),
            Line(
                Vector2(-size_im_y.real, -size_im_y.imaginary),
                corners[3]
            )
        ]

        return lines

    def collision_line(self, line:Line) -> ColLines:
        colls = [ColLines(line, self.lines[0]),
                 ColLines(line, self.lines[1]),
                 ColLines(line, self.lines[2]),
                 ColLines(line, self.lines[3])]

        #Reta com menor t significa primeira colisão
        t_menor = colls[0]
        for i in range(1, 4):
            if (colls[i].coll and colls[i].t_1 < t_menor.t_1):
                t_menor = colls[i]

        return t_menor
    
    def in_side_region(self, point:Vector2) -> int:
        """Expand the sides to infinity, the diagonals are the outside and the sides the inside"""
        lines = self.to_lines()
        count = 0
        for line in lines:
            count += line.is_point_above(point)
        return count == 1

    @property
    def __str__(self) -> None:
        return f"pos: {self.position.__str__}, size: {self.size.__str__}"

    def draw(self, color:Color, map_offset:Vector2=Vector2(0, 0), scaler:float=1, outlines:bool=True) -> None:
        size_im_x = Imaginary(self.size.x / 2.0, 0.0) * self.angle
        size_im_y = Imaginary(0.0, self.size.y / 2.0) * self.angle
        up_left_corner = [self.position.x - size_im_x.real      - size_im_y.real,
                          self.position.y - size_im_x.imaginary - size_im_y.imaginary]
        
        rec = [map_offset.x + up_left_corner[0] * scaler,
               map_offset.y + up_left_corner[1] * scaler,
               self.size.x * scaler,
               self.size.y * scaler]
        ori = [0, 0]
        degree = degrees(atan2(self.angle.imaginary, self.angle.real))

        draw_rectangle_pro(rec, ori, degree, color)
        if outlines:
            self.draw_lines(map_offset, scaler, BLACK)

    def draw_lines(self, map_offset:Vector2, scaler:float, color:Color) -> None:
        for line in self.lines:
            line.draw(map_offset, scaler, color)


class Circle(Shape):
    def __init__(self, position:Vector2, radius:float, speed:Vector2=Vector2(0, 0)) -> None:
        super().__init__(position, speed=speed)
        self.radius = radius

    def copy(self):
        return Circle(self.position.copy(), self.radius, self.speed)
    
    @property
    def __str__(self) -> None:
        f"pos: {self.position.x:.2f} / {self.position.y:.2f}, radius: {self.radius:.2f}"
    
    def draw(self, color:Color, map_offset:Vector2=Vector2(0, 0), scaler:float=1, outlines:bool=True) -> None:
        pos = self.position * scaler
        pos += map_offset
        pos = pos.to_list()
        radius = self.radius * scaler
        draw_circle_v(pos, radius, color)
        if outlines:
            draw_circle_lines_v(pos, radius, BLACK)

class ColCircleLine:
    def __init__(self, circle:Circle, line:Line, delta_time:float=0):
        self.did_intersect = 0
        self.intersections = [False, False]
        self.point_1 = Vector2(0, 0)
        self.point_2 = Vector2(0, 0)
        self.collision_line(circle, line, delta_time)

    def collision_line(self, circle:Circle, line:Line, delta_time:float) -> dict:
        next_pos_circle = circle.next_position(delta_time)

        #equação de segundo grau para achar t em P = A + tV
        
        a = (line.direction.x) ** 2 + (line.direction.y) ** 2

        b = 2 * (line.direction.x * (line.point.x - next_pos_circle.x) +
                 line.direction.y * (line.point.y - next_pos_circle.y))
        
        c = ((line.point.x - next_pos_circle.x) ** 2 +
             (line.point.y - next_pos_circle.y) ** 2 -
             (circle.radius) ** 2)

        delta = b ** 2 - 4 * a * c
        if (delta < 0.0):
            return

        t_1 = (-b + delta ** 0.5) / (2 * a)
        t_2 = (-b - delta ** 0.5) / (2 * a)

        self.point_1 = Vector2(line.point.x + t_1 * line.direction.x, line.point.y + t_1 * line.direction.y)
        self.point_2 = Vector2(line.point.x + t_2 * line.direction.x, line.point.y + t_2 * line.direction.y)
        
        self.intersections[0] = line.has_point(self.point_1)
        self.intersections[1] = line.has_point(self.point_2)
        self.did_intersect = self.intersections[0] + self.intersections[1]

    @property
    def __str__(self):
        return f"{self.intersections[0]}: {self.point_1.__str__} e {self.intersections[1]}: {self.point_2.__str__}"
