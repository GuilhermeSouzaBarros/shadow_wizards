from abc import ABC

from utils import *
from vectors import Vector2, Domain
from lines import Line, ColLines
from shapes import Shape, Rectangle, Circle, ColCircleLine

class CollisionInfo(ABC):
    def __init__(self, calculate_distance:bool):
        self.intersection = False
        self.border_intersection = False
        self.calculate_distance = calculate_distance
        self.distance = Vector2(0, 0)

    def collision(shape_1:Shape, shape_2:Shape, delta_time:float=0.0, calculate_distance:bool=False) -> None:
        """Distance to stop collision is relative to first shape"""
        if shape_1.__class__ == Rectangle and shape_2.__class__ == Circle:
            return ColRectangleCircle(shape_1, shape_2, delta_time, calculate_distance)
        
        if shape_1.__class__ == Circle and shape_2.__class__ == Rectangle:
            col = ColRectangleCircle(shape_2, shape_1, delta_time, calculate_distance)
            col.distance *= -1
            return col
        
        if shape_1.__class__ == Circle and shape_2.__class__ == Circle:
            return ColCircleCircle(shape_1, shape_2, delta_time, calculate_distance)
        
        if shape_1.__class__ == Rectangle and shape_2.__class__ == Rectangle:
            return ColRectangleRectangle(shape_1, shape_2, delta_time, calculate_distance)

    def shape_copy(shape:Shape, delta_time:float) -> Shape:
        shape = shape.copy()
        if shape.speed.module():
            shape.delta_position(delta_time)
        return shape



class ColRectangleRectangle(CollisionInfo):
    def __init__(self, rectangle_1:Rectangle, rectangle_2:Rectangle, delta_time:float=0.0, calculate_distance:bool=False) -> None:
        super().__init__(calculate_distance)
        self.needs_precise = True
        self.collision(rectangle_1, rectangle_2, delta_time)

    def simple_col(self, rectangle_1:Rectangle, rectangle_2:Rectangle, delta_time:float) -> None:
        next_pos_1 = rectangle_1.next_position(delta_time)
        next_pos_2 = rectangle_2.next_position(delta_time)
        total_dist = (next_pos_1 - next_pos_2).module()

        if total_dist > rectangle_1.outer_radius + rectangle_2.outer_radius:
            self.intersection = False
            self.needs_precise = False
           
        elif total_dist < rectangle_1.inner_radius + rectangle_2.inner_radius:
            self.intersection = True
            self.needs_precise = False

    def precise_col(self, rectangle_1:Rectangle, rectangle_2:Rectangle, delta_time:float=0):
        next_pos_1 = CollisionInfo.shape_copy(rectangle_1, delta_time)
        next_pos_2 = CollisionInfo.shape_copy(rectangle_2, delta_time)
        next_pos_1.lines = next_pos_1.to_lines()
        next_pos_2.lines = next_pos_2.to_lines()

        lines_col = []
        for line_1 in next_pos_1.lines:
            for line_2 in next_pos_2.lines:
                col = ColLines(line_1, line_2)
                if col.did_intersect and not col.parallel:
                    self.intersection = True
                    self.border_intersection = True
                    lines_col.append({'line_1': line_1, 'line_2':line_2, 'col': col})
                elif not self.calculate_distance:
                    return

        if not self.border_intersection or len(lines_col) != 2:
            return

        if (lines_col[0]['line_1'] == lines_col[1]['line_1'] or
            lines_col[0]['line_2'] == lines_col[1]['line_2']):
            relative = 1
            if lines_col[0]['line_2'] == lines_col[1]['line_2']:
                aux = next_pos_1
                next_pos_1 = next_pos_2
                next_pos_2 = aux
                for col in lines_col:
                    aux = col['line_1']
                    col['line_1'] = col['line_2']
                    col['line_2'] = aux
                relative = -1
            possible_corner = [ lines_col[0]['line_2'].point,
                                lines_col[0]['line_2'].point + lines_col[0]['line_2'].direction,
                                lines_col[1]['line_2'].point,
                                lines_col[1]['line_2'].point + lines_col[1]['line_2'].direction]
            
            dist_ori = []
            ori_line_dir = lines_col[0]['line_1'].direction.copy()
            ori_line = Line(ori_line_dir, next_pos_1.position, Domain(float('-inf'), float('inf')))
            for possible in possible_corner:
                dist_ori.append(ori_line.point_distance(possible).module())

            shortest_dist = [0, dist_ori[0]]
            for i, possible in enumerate(dist_ori):
                if possible < shortest_dist[1]:
                    shortest_dist[0] = i
                    shortest_dist[1] = possible
            corner = possible_corner[shortest_dist[0]]

            direction = lines_col[0]['line_1'].direction.copy()
            direction.rotate_90_anti()
            push_line = Line(direction, corner, Domain(float('-inf'), float('inf')))
            push = ColLines(push_line, lines_col[0]['line_1'])
            self.distance = push.point - corner
            self.distance *= relative
            
        else:
            corner = ColLines(lines_col[0]['line_1'], lines_col[1]['line_1'])
            if not corner.did_intersect:
                return
            corner = corner.point

            push = [(lines_col[0]['col'].point - corner).module(), (lines_col[1]['col'].point - corner).module()]
            push = lines_col[push[0] > push[1]]['col']
            self.distance = corner - push.point


    def collision(self, rectangle_1:Rectangle, rectangle_2:Rectangle, delta_time:float=0.0) -> None:
        self.simple_col(rectangle_1, rectangle_2, delta_time)
        if self.needs_precise or not self.intersection and self.calculate_distance:
             self.precise_col(rectangle_1, rectangle_2, delta_time)



class ColRectangleCircle(CollisionInfo):
    def __init__(self, rectangle:Rectangle, circle:Circle, delta_time:float=0.0, calculate_distance:bool=False) -> None:
        super().__init__(calculate_distance)
        self.needs_precise = True
        self.collision(rectangle, circle, delta_time)

    def simple_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        next_pos_rec = rectangle.next_position(delta_time)
        next_pos_cir = circle.next_position(delta_time)
        total_dist = (next_pos_rec - next_pos_cir).module()

        if total_dist > rectangle.outer_radius + circle.radius:
            self.intersection = False
            self.needs_precise = False
           
        elif total_dist < rectangle.inner_radius + circle.radius:
            self.intersection = True
            self.needs_precise = False


    def precise_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        next_rec = CollisionInfo.shape_copy(rectangle, delta_time)
        next_cir = CollisionInfo.shape_copy(circle, delta_time)

        lines_col = []
        for line in next_rec.lines:
            col = ColCircleLine(next_cir, line, delta_time)
            if col.did_intersect:
                self.intersection = True
                self.border_intersection = True
                if not self.calculate_distance:
                    return
                lines_col.append({'line': line, 'col': col})
        
        if not self.intersection:
            return

        if not self.border_intersection or rectangle.is_point_inside(next_cir.position):
            ori_angle = circle.position - rectangle.position
            ori_line = Line(ori_angle, rectangle.position.copy(), Domain(0, float("inf")))

            for line in rectangle.lines:
                col = ColLines(ori_line, line)
                if col.did_intersect:
                    push_line = line
                    break

            distance = push_line.point_distance(next_cir.position)
            distance.to_module(distance.module() + next_cir.radius)
            self.distance = distance
            return

        num_col = len(lines_col)
        diff = Vector2(0, 0)
        if num_col == 1 or (num_col == 2 and (lines_col[0]['line'].is_parallel(lines_col[1]['line']))):
            if (num_col == 1):
                col = lines_col[0]['col']
                middle_point = (col.point_1 + col.point_2) * 0.5
            else:
                line_1 = lines_col[0]['line']
                line_2 = lines_col[1]['line']
                possible_corners = [[line_1.point, line_1.point + line_1.direction],
                                    [line_2.point, line_2.point + line_2.direction]]
                corners = []
                for corner in possible_corners:
                    dist = [(corner[0] - next_cir.position).module(), (corner[1] - next_cir.position).module()]
                    corners.append(corner[dist[0] > dist[1]])
                middle_point = (corners[0] + corners[1]) * 0.5

            diff = next_cir.position - middle_point
        elif num_col == 2:
            line_1 = lines_col[0]['line']
            line_2 = lines_col[1]['line']
            corner = ColLines(line_1, line_2).point
            axis = [Line(line_1.direction, next_cir.position, Domain(float("-inf"), float("inf"))),
                    Line(line_2.direction, next_cir.position, Domain(float("-inf"), float("inf")))]
            axis_col = [ColLines(axis[1], line_1), ColLines(axis[0], line_2)]
            if not (axis_col[0].did_intersect or axis_col[1].did_intersect):
                diff = next_cir.position - corner
            elif axis_col[0].did_intersect and axis_col[1].did_intersect:
                return
            elif axis_col[0].did_intersect:
                diff = next_cir.position - axis_col[0].point
            elif axis_col[1].did_intersect:
                diff = next_cir.position - axis_col[1].point

        radius = diff.copy()
        radius.to_module(next_cir.radius)
        self.distance = radius - diff
            
    def collision(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        self.simple_col(rectangle, circle, delta_time)
        if (self.needs_precise or (self.intersection and self.calculate_distance)):
            self.precise_col(rectangle, circle, delta_time)
        
class ColCircleCircle(CollisionInfo):
    def __init__(self, circle_1:Circle, circle_2:Circle, delta_time:float=0.0, calculate_distance:bool=False):
        super().__init__(calculate_distance)
        self.collision(circle_1, circle_2, delta_time)
    
    def collision(self, circle_1:Circle, circle_2:Circle, delta_time:float=0.0) -> bool:
        next_cir_1 = CollisionInfo.shape_copy(circle_1, delta_time)
        next_cir_2 = CollisionInfo.shape_copy(circle_2, delta_time)

        origins = next_cir_2.position - next_cir_1.position
        total_radius = next_cir_1.radius + next_cir_2.radius
        distance = origins.module()
        self.intersection = distance <= total_radius

        if self.intersection and self.calculate_distance:
            distance = origins.copy()
            distance.to_module(total_radius)
            self.distance = distance - origins
