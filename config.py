# Cores verdadeiras dos Shadow Wizards
RED = (246, 39, 49, 255)
BLUE = (90, 100, 231, 255)
PINK = (255, 201, 227, 255)
LIME = (201, 242, 39, 255)
GOLD = (239, 163, 3, 255)
YELLOW = (254, 248, 4, 255)
DARKGREEN = (29, 145, 63, 255)
PURPLE = (178, 82, 179, 255)

GAME_TITLE = "Shadow Wizards"

MENU_MAIN_ID = 0
MENU_SCREENS = ["menu_info/main_menu.json", "menu_info/join_room.json", "menu_info/host_room.json"]

GAME_TICK = 0.0078125 #128 ticks por segundo

FREE_FOR_ALL_MAP_ID = 1
PAYLOAD_MAP_ID = 2
CAPTURE_THE_FLAG_MAP_ID = 3
DOMINATION_MAP_ID = 4

CHARACTER_RED       = {"id": 1, "name": "Red",    "sprite": "sprites/red_wizard.png", "color": RED}
CHARACTER_BLUE      = {"id": 2, "name": "Blue",   "sprite": "sprites/blue_wizard.png","color": BLUE}
CHARACTER_PINK      = {"id": 3, "name": "Pink",   "sprite": "sprites/wizard.png",     "color": PINK}
CHARACTER_LIME      = {"id": 4, "name": "Lime",   "sprite": "sprites/wizard.png",     "color": LIME}
CHARACTER_GOLD      = {"id": 5, "name": "Golden", "sprite": "sprites/wizard.png",     "color": GOLD}
CHARACTER_YELLOW    = {"id": 6, "name": "Yellow", "sprite": "sprites/wizard.png",     "color": YELLOW}
CHARACTER_DARKGREEN = {"id": 7, "name": "Green",  "sprite": "sprites/wizard.png",     "color": DARKGREEN}
CHARACTER_PURPLE    = {"id": 8, "name": "Purple", "sprite": "sprites/wizard.png",     "color": PURPLE}

CHARACTERS = (CHARACTER_RED, CHARACTER_BLUE, CHARACTER_PINK, CHARACTER_LIME, CHARACTER_GOLD, CHARACTER_YELLOW, CHARACTER_DARKGREEN, CHARACTER_PURPLE)

SKILLS = {"Fireball": "Joga uma bola de fogo que ao atingir algo explode", 
          "Dash": "Dá um impulso no personagem", 
          "Gun": "Permite atirar várias balas", 
          "Traps": "Perimite colocar armadilhas no chão, que podem causar dano ou outro efeito", 
          "SuperSpeed": "Jogador possui maior velocidade", 
          "Intangibility": "Permite atravessar paredes", 
          "Shield": "Por alguns segundos o jogador não recebe dano", 
          "Laser": "Atira um laser na direção que o jogador está olhando"}

BASE_WIDTH = 800
BASE_HEIGHT = 600

MATCH_DURATION = 180.00