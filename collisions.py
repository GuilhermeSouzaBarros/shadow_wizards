from shapes import Rectangle, Circle
from vectors import Vector2
from aux import *

class ColRectangleCircle:
    def __init__(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        self.intersection = False
        self.lines_col = self.collision(rectangle, circle, delta_time)
    
    def simple_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> Vector2:
        next_pos_rec = rectangle.next_position(delta_time)
        next_pos_cir = circle.next_position(delta_time)
        total_dist = Vector2(next_pos_rec.x - next_pos_cir.x,
                             next_pos_rec.y - next_pos_cir.y).module()
        return total_dist <= rectangle.radius + circle.radius

    def precise_col(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        rec_lines = rectangle.to_lines()

        lines_col = []
        for line in rec_lines:
            lines_col.append(circle.collision_line(line, delta_time))
            
        for line in lines_col:
            if line['intersections']:
                self.intersection = True
        return lines_col
                

    def collision(self, rectangle:Rectangle, circle:Circle, delta_time:float) -> None:
        if not self.simple_col(rectangle, circle, delta_time):
            return []

        return self.precise_col(rectangle, circle, delta_time)
        
