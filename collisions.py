from shapes import Rectangle, Circle
from lines import Line, ColLines
from vectors import Vector2
from aux import *

class ColRectangleCircle:
    def __init__(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        self.intersection = False
        self.point_1 = Vector2(0.0, 0.0)
        self.point_2 = Vector2(0.0, 0.0)
        self.collision(rectangle, circle, delta_time)
    
    def simple_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> Vector2:
        next_pos_rec = rectangle.next_position(delta_time)
        next_pos_cir = circle.next_position(delta_time)
        total_dist = Vector2(next_pos_rec.x - next_pos_cir.x,
                             next_pos_rec.y - next_pos_cir.y).module()

        return total_dist <= rectangle.radius + circle.radius

    def precise_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        rec_lines = rectangle.to_lines()
        circle_next_pos = circle.next_position(delta_time)
        rec_side = rectangle.in_side_region(circle.position)

        lines_col = []
        for i, line in enumerate(rec_lines):
            lines_col.append([circle.collision_line(line, delta_time), i])
        
        for info in lines_col:
            if (rec_side and (info[0]['intersections'] == 2 or
                (info[0]['intersections'] and rec_lines[info[1]].is_point_above(circle.position)))):
                push_dir = Vector2(rec_lines[info[1]].direction.x, rec_lines[info[1]].direction.y)
                push_dir.rotate_90_anti()
                push_dir.to_module(1.0)
                
                distance = Vector2(rectangle.size.x / 2 + circle.radius, rectangle.size.y / 2 + circle.radius)
                distance.x -= abs(circle_next_pos.x - rectangle.position.x)
                distance.y -= abs(circle_next_pos.y - rectangle.position.y)

                circle.speed.x += (distance.x * push_dir.x / delta_time)
                circle.speed.y += (distance.y * push_dir.y / delta_time)
                return

        for info_0 in lines_col:
            if (not info_0[0]['intersections']):
                continue
            for info_1 in lines_col:
                if (info_0 == info_1 or not info_1[0]['intersections']):
                    continue

                intersection = ColLines(rec_lines[info_0[1]], rec_lines[info_1[1]])

                push_dir = Vector2(circle_next_pos.x - intersection.point.x, circle_next_pos.y - intersection.point.y)
                push_dir.to_module(circle.radius + SMALL_FLOAT)

                next_pos = Vector2(intersection.point.x + push_dir.x, intersection.point.y + push_dir.y)
                
                circle.speed.x = (next_pos.x - circle.position.x) / delta_time
                circle.speed.y = (next_pos.y - circle.position.y) / delta_time


    def collision(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        if (eq_z(circle.speed.module() + rectangle.speed.module())):
            return

        if not self.simple_col(rectangle, circle, delta_time):
            return

        self.precise_col(rectangle, circle, delta_time)
