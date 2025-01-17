
STATE_INITIAL_MENU = 1 
STATE_PLAY_GAME = 2
STATE_EXIT = 0

GAME_TITLE = "Shadow Wizards"

TICK = 0.00390625 #256 ticks por segundo

# Cores verdadeiras dos Shadow Wizards
RED = (246, 39, 49, 255)
BLUE = (90, 100, 231, 255)
PINK = (255, 201, 227, 255)
LIME = (201, 242, 39, 255)
GOLD = (239, 163, 3, 255)
YELLOW = (254, 248, 4, 255)
DARKGREEN = (29, 145, 63, 255)
PURPLE = (178, 82, 179, 255)

FREE_FOR_ALL_MAP_ID = 1
PAYLOAD_MAP_ID = 2
CAPTURE_THE_FLAG_MAP_ID = 3
DOMINATION_MAP_ID = 4

CHARACTER_RED       = {"id": 1, "name": "Red Shadow Wizard",    "sprite": "sprites/red_wizard.png", "color": RED}
CHARACTER_BLUE      = {"id": 2, "name": "Blue Shadow Wizard",   "sprite": "sprites/blue_wizard.png",     "color": BLUE}
CHARACTER_PINK      = {"id": 3, "name": "Pink Shadow Wizard",   "sprite": "sprites/wizard.png",     "color": PINK}
CHARACTER_LIME      = {"id": 4, "name": "Lime Shadow Wizard",   "sprite": "sprites/wizard.png",     "color": LIME}
CHARACTER_GOLD      = {"id": 5, "name": "Golden Shadow Wizard", "sprite": "sprites/wizard.png",     "color": GOLD}
CHARACTER_YELLOW    = {"id": 6, "name": "Yellow Shadow Wizard", "sprite": "sprites/wizard.png",     "color": YELLOW}
CHARACTER_DARKGREEN = {"id": 7, "name": "Green Shadow Wizard",  "sprite": "sprites/wizard.png",     "color": DARKGREEN}
CHARACTER_PURPLE    = {"id": 8, "name": "Purple Shadow Wizard", "sprite": "sprites/wizard.png",     "color": PURPLE}

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