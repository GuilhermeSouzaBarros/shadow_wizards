from math import sqrt
from abc import ABC

from utils import *
from vectors import Vector2
from lines import ColLines
from shapes import Shape, Rectangle, Circle

class CollisionInfo(ABC):
    def __init__(self):
        self.intersection = False
        self.needs_precise = True
        self.calculate_distance = False
        self.distance = Vector2(0, 0) #distance to stop collision, relative to hitbox_1

    def collision(shape_1:Shape, shape_2:Shape, delta_time:float=0.0, calculate_distance:bool=False) -> None:
        if shape_1.__class__ == Rectangle and shape_2.__class__ == Circle:
            return ColRectangleCircle(shape_1, shape_2, delta_time, calculate_distance)
        if shape_1.__class__ == Circle and shape_2.__class__ == Rectangle:
            return ColRectangleCircle(shape_2, shape_1, delta_time, calculate_distance)
        if shape_1.__class__ == Circle and shape_2.__class__ == Circle:
            return ColCircleCircle(shape_1, shape_2, delta_time, calculate_distance)

class ColRectangleCircle(CollisionInfo):
    def __init__(self, rectangle:Rectangle, circle:Circle, delta_time:float=0.0, calculate_distance:bool=False) -> None:
        super().__init__()
        self.lines_col = self.collision(rectangle, circle, delta_time, calculate_distance)

    def simple_col(self, rectangle:Rectangle, circle:Circle, delta_time:float, calculate_distance:bool=False) -> Vector2:
        next_pos_rec = rectangle.next_position(delta_time)
        next_pos_cir = circle.next_position(delta_time)
        total_dist = Vector2(next_pos_rec.x - next_pos_cir.x,
                             next_pos_rec.y - next_pos_cir.y).module()

        if total_dist * 0.85 > rectangle.outer_radius + circle.radius:
            self.intersection = False
            self.needs_precise = False
           
        elif not calculate_distance and total_dist * 1.15 < rectangle.inner_radius + circle.radius:
            self.intersection = True
            self.needs_precise = False


    def precise_col(self, rectangle:Rectangle, circle:Circle, delta_time:float, calculate_distance:bool=False) -> None:
        rectangle = rectangle.copy()
        circle = circle.copy()

        if rectangle.speed.module():
            next_rec_pos = rectangle.copy()
            next_rec_pos.delta_position(delta_time)
        else:
            next_rec_pos = rectangle

        if circle.speed.module():
            next_cir_pos = circle.copy()
            next_cir_pos.delta_position(delta_time)
        else:
            next_cir_pos = circle
        
        lines_col = []
        for line in next_rec_pos.lines:
            lines_col.append(next_cir_pos.collision_line(line, delta_time))
        
        for info in lines_col:
            if info['intersections']:
                self.intersection = True
                break

        rec_side = rectangle.in_side_region(circle.position)

        for i, info in enumerate(lines_col):
            if (rec_side and (info['intersections'] == 2 or
                (info['intersections'] and next_rec_pos.lines[i].is_point_above(circle.position)))):
                push_dir = next_rec_pos.lines[i].direction.copy()
                push_dir.rotate_90_anti()
                push_dir.to_module(1.0)
                
                self.distance = Vector2(rectangle.size.x / 2 + circle.radius, rectangle.size.y / 2 + circle.radius)
                self.distance.x -= abs(next_cir_pos.position.x - next_rec_pos.position.x)
                self.distance.y -= abs(next_cir_pos.position.y - next_rec_pos.position.y)
                self.distance.x *= push_dir.x
                self.distance.y *= push_dir.y
                return lines_col
            
        for i, info_0 in enumerate(lines_col):
            if (not info_0['intersections']):
                continue
            for j, info_1 in enumerate(lines_col):
                if (info_0 == info_1 or not info_1['intersections']):
                    continue

                intersection = ColLines(next_rec_pos.lines[i], next_rec_pos.lines[j])

                push_dir = next_cir_pos.position - intersection.point
                push_dir.to_module(circle.radius + SMALL_FLOAT)

                next_cir_pos.position = intersection.point + push_dir
                
                self.distance.x = (next_cir_pos.position.x - circle.position.x) - circle.speed.x * delta_time
                self.distance.y = (next_cir_pos.position.y - circle.position.y) - circle.speed.y * delta_time

        return lines_col

    def collision(self, rectangle:Rectangle, circle:Circle, delta_time:float, calculate_distance:bool=False) -> None:
        self.simple_col(rectangle, circle, delta_time, calculate_distance)
        if not (self.needs_precise or (self.intersection and self.calculate_distance)):
            return []
        return self.precise_col(rectangle, circle, delta_time)
        
class ColCircleCircle(CollisionInfo):
    def __init__(self, circle_1:Circle, circle_2:Circle, delta_time:float=0.0, calculate_distance:bool=False):
        super().__init__()
        self.collision(circle_1, circle_2, delta_time)
    
    def collision(self, circle1: Circle, circle2: Circle, delta_time:float=0.0, calculate_distance:bool=False) -> bool:
        """ Verifica se dois círculos colidem entre si. """
        distance = sqrt((circle1.position.x - circle2.position.x) ** 2 + (circle1.position.y - circle2.position.y) ** 2)
        self.intersection = distance <= (circle2.radius + circle1.radius)
        # Ainda tenho que terminar essa função para calcular distancia
