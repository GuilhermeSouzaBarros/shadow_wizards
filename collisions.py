from shapes import Rectangle, Circle
from vectors import Vector2
from aux import *

class ColRectangleCircle:
    def __init__(self, rectangle, circle, delta_time):
        self.intersection = False
        self.point_1 = Vector2(0.0, 0.0)
        self.point_2 = Vector2(0.0, 0.0)
        self.collision(rectangle, circle, delta_time)
    
    def simple_col(self, rectangle, circle, delta_time):
        next_pos_rec = rectangle.next_position(delta_time)
        next_pos_cir = circle.next_position(delta_time)
        total_dist = Vector2(next_pos_rec.x - next_pos_cir.x,
                             next_pos_rec.y - next_pos_cir.y).module()

        return total_dist <= rectangle.radio + circle.radio

    def precise_col(self, rectangle, circle, delta_time):
        rec_retas = rectangle.to_lines()
        col = 0
        for line in rec_retas:
            info = circle.collision_line(line, delta_time)
            col += info['instersections']
        return col

    def collision(self, rectangle, circle, delta_time):
        #if (eq_z(circle.speed.module() + rectangle.speed.module())):
            #return

        if not self.simple_col(rectangle, circle, delta_time):
            return
        print("Simple col pass")

        if not self.precise_col(rectangle, circle, delta_time):
            return
        print("Precise col pass")

        self.intersection = True
