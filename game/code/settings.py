import pygame 
from os.path import join 
from os import walk
import pygame_gui
import random
import unicodedata

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720 
TILE_SIZE = 64

def remove_accents(input_str):
    # Normaliza a string e remove caracteres de acentuação
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])