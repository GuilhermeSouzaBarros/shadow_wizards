from skills.skill import *

class Shield(Skill):
    def __init__(self):
        super().__init__()
        self._cooldown = 1
        self.duration = 2
        self.size = Vector2(32, 32)
        self.sprite = load_texture("sprites/shield.png")
        self.pos = Vector2(0, 0)

    def encode(self) -> bytes:
        message = pack("?", self.is_activated)
        return message
    
    def decode(self, bytes_string:bytes) -> int:
        data = unpack("?", bytes_string[0:1])
        self.is_activated = data[0]
        return 1
    
    def update(self, player_pos:Vector2, angle:Imaginary, player_input:dict, *args) -> None:
        activate = self.skill_key(player_pos, angle, 1, player_input)
        self.pos = player_pos
        if self.can_deactivate():
            self.deactivate()

    def draw(self, *args) -> None:
        if self.is_activated:
            sprite = args[-1]
            scaler = args[1]
            size_im_x = Imaginary(self.size.x/2, 0.0)
            size_im_y = Imaginary(0.0, self.size.y/2.0)
            up_left_corner = [self.pos.x - size_im_x.real - size_im_y.real,
                              self.pos.y - size_im_x.imaginary - size_im_y.imaginary]
            offset = Vector2(self.size.x*0.5, self.size.y*0.5)
            pos = [args[0].x + ((up_left_corner[0] + 16)*scaler), 
                   args[0].y + ((up_left_corner[1] + 32)*scaler)]
            rectangle_dest = [round(pos[0]), round(pos[1]),
                            round(scaler*self.size.x),
                            round(scaler*self.size.y)]
            draw_texture_pro(self.sprite, [0, 0, 32, 32], rectangle_dest, 
                             [round(offset.x*scaler), round(2*offset.y*scaler)], 0, WHITE)