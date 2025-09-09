import pygame 
from os.path import join 
from os import walk
import random
import unicodedata

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800 
TILE_SIZE = 64

def remove_accents(input_str):
    """Normaliza a string e remove caracteres de acentuação"""
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])


# Documentação do exio Z

# Grupos
PLAYER_LAYER = 10


EFFECT_LAYER = 20
UI_LAYER = 15

#BOSSES
ENEMY_LAYER = 10
ENEMY_ATTACK_LAYER = 9
ENEMY_SHADOW_ATTACK_LAYER = 8

#MUNDO
OBJECTS_LAYER = 5
WORLD_LAYER = 0