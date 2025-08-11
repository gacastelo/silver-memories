import pygame 
from os.path import join 
from os import walk
import random
import unicodedata

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800 
TILE_SIZE = 64

def remove_accents(input_str):
    # Normaliza a string e remove caracteres de acentuação
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])