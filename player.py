from pyray import *
from raylib import *
import struct
from math import atan2, degrees

from config import *

from imaginary import Imaginary
from vectors import Vector2
from collisions import CollisionInfo
from shapes import Shape, Circle
from sword import Sword

from skills.fireball import Fireball
from skills.gun import Gun
from skills.traps import Traps
from skills.speedy_skills import Dash, SuperSpeed
from skills.shield import Shield
from skills.intangibility import Intangibility
from skills.laser import Laser

class Player:
    def __init__(self, tile_size:float,
                 start_row:int, start_column:int, start_angle:list,
                 player_id:int, character_id:int, map_id:int, nick:str) -> None:
        self.character_id = character_id
        for character in CHARACTERS:
            if character['id'] == self.character_id:
                self.character_name = character['name']
                self.sprite = character['sprite']
                self.color = character['color']
        
        self.tile_size   = tile_size

        pos = Vector2(tile_size * (start_column + 0.5),
                      tile_size * (start_row    + 0.5))
        self.start_pos = Vector2(
            tile_size * (start_column + 0.5),
            tile_size * (start_row    + 0.5)
        )
        self.start_angle = Imaginary(start_angle[0], start_angle[1])

        self.hitbox      = Circle(pos, tile_size * 0.4)
        self.is_alive    = True
        self.respawn     = 2
        self.start_time  = 0
        self.angle       = Imaginary(start_angle[0], start_angle[1])
        self.speed_multiplier = 4.0

        self.sword = Sword(pos)
        self.skill = self.choose_character(character_id, pos.copy())
        
        self.kills  = 0
        self.deaths = 0

        self.nick   = nick
        self.sprite = load_texture(self.sprite) 

        self.player_id = player_id
        self.team = player_id if map_id == 1 else (player_id == 2 or player_id == 4) + 1

        self.has_flag = False


    def choose_character(self, character_id, pos):
        """
        Recebe um id correspondendo ao personagem escolhido e retorna a Habilidade dele
        """
        if character_id == CHARACTER_RED["id"]:
            skill = Fireball(pos)
            self.skill_name = "Fireball"
        elif character_id == CHARACTER_BLUE["id"]:
            skill = Dash()
            self.skill_name = "Dash"
        elif character_id == CHARACTER_PINK["id"]:
            skill = Gun(pos)
            self.skill_name = "Gun"
        elif character_id == CHARACTER_LIME["id"]:
            skill = Traps(pos)
            self.skill_name = "Traps"
        elif character_id == CHARACTER_GOLD["id"]:
            skill = SuperSpeed()
            self.skill_name = "Speed"
        elif character_id == CHARACTER_YELLOW["id"]:
            skill = Intangibility()
            self.skill_name = "Intangibility"
        elif character_id == CHARACTER_DARKGREEN["id"]:
            skill = Shield()
            self.skill_name = "Shield"
        elif character_id == CHARACTER_PURPLE["id"]:
            skill = Laser(pos)
            self.skill_name = "Laser"

        return skill

    def update_angle(self, player_input:dict) -> None:
        if (player_input["up"]):    self.angle.y -= 1.0
        if (player_input["left"]):  self.angle.x -= 1.0
        if (player_input["down"]):  self.angle.y += 1.0
        if (player_input["right"]): self.angle.x += 1.0

    def update_player_pos(self, speed_multiplier, player_input:dict) -> None:
        if speed_multiplier == 0:
            self.hitbox.speed = Vector2(0, 0)
            return

        speed = self.tile_size * speed_multiplier
        previous_angle = self.angle

        self.angle = Vector2(0.0, 0.0)
        self.update_angle(player_input)
        
        if (self.angle.module()):
            self.angle.to_module(1.0)
            self.hitbox.speed.x = self.angle.x * speed
            self.hitbox.speed.y = self.angle.y * speed
            self.angle = Imaginary(self.angle.x, self.angle.y)
        else:
            self.angle = previous_angle
            self.hitbox.speed = Vector2(0, 0)
    
    def update(self, player_input:dict) -> None:
        if self.is_alive:
            if ((self.skill_name == "Speed" or 
                self.skill_name == "Dash") and self.skill.is_activated):
                self.update_player_pos(self.skill.speed_multiplier, player_input)

            elif(self.skill_name == "Laser" and self.skill.is_activated):
                self.update_player_pos(0, player_input)
                
            else:
                self.update_player_pos(self.speed_multiplier, player_input)
                        
        elif (get_time() - self.start_time >= self.respawn):
            self.is_alive = True
            self.hitbox.position = self.start_pos.copy()
            self.angle           = self.start_angle.copy()

    def killed(self):
        self.kills += 1

    def died(self):
        self.deaths += 1
        self.is_alive = False
        self.has_flag = False
        self.start_time = get_time()
        self.hitbox.speed = Vector2(0, 0)

        self.sword.deactivate()

    def draw(self, map_offset:Vector2, scaler:float, hitbox:bool) -> None:
        color = self.color
        tint = self.color
        if (self.character_id == CHARACTER_RED['id'] or
            self.character_id == CHARACTER_BLUE['id']):
            tint = WHITE

        color = (color[0], color[1], color[2], int(color[3] / (2 - ((not self.has_flag and self.is_alive and not self.skill.is_activated)))))
        tint = (tint[0], tint[1], tint[2], int(tint[3] / (2 - ((not self.has_flag and self.is_alive and not self.skill.is_activated)))))
        if (hitbox):
            self.hitbox.draw(color, map_offset, scaler)
        else:
            angle = degrees(atan2(self.angle.imaginary, self.angle.real))
            angle += 360 * (angle < 0.0)
            angle /= 45
            angle = int(angle)
            offset = self.hitbox.radius * 0.5

            pos = [map_offset.x + ((self.hitbox.position.x - self.hitbox.radius) * scaler),
                   map_offset.y + ((self.hitbox.position.y - self.hitbox.radius) * scaler)]
            rectangle_dest = [round(pos[0]), round(pos[1]),
                            round(scaler * (self.hitbox.radius + offset) * 2),
                            round(scaler * (self.hitbox.radius + offset) * 2)]

            draw_texture_pro(self.sprite, [0, angle * 32, 32, 32], rectangle_dest, [round(offset * scaler), round(2 * offset * scaler)], 0, tint)

        self.sword.draw(map_offset, scaler, color)
        self.skill.draw(map_offset, scaler)
    
    def encode(self) -> bytes:
        message = "p".encode()
        message += bytes(struct.pack("dddd??", self.hitbox.position.x, self.hitbox.position.y,
                                     self.angle.real, self.angle.imaginary, self.is_alive,
                                     self.sword.active))
        return message
    
    def decode(self, byte_string:bytes) -> int:
        datas = struct.unpack("dddd??", byte_string[1:35])
        self.hitbox.position = Vector2(datas[0], datas[1])
        self.angle.real = datas[2]
        self.angle.imaginary = datas[3]
        self.is_alive = datas[4]
        if (datas[5]):
            self.sword.update(self.hitbox.position, self.angle, {"sword": True})
        else:
            self.sword.deactivate()
        return 35
    