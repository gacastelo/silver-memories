import pygame 
from os.path import join 
from os import walk
import random
import unicodedata

WINDOW_WIDTH, WINDOW_HEIGHT = 1900, 1000 
TILE_SIZE = 64

def remove_accents(input_str):
    """Normaliza a string e remove caracteres de acentuação"""
    nfkd = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])

class Button:
    def __init__(self, text, pos, size=(200, 60)):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.color_idle = (32, 61, 57)
        self.color_hover = (55, 134, 139)
        self.color_active = (150, 150, 150)
        self.font = pygame.font.Font(None, 40)
        self.clicked = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.color_idle

        if self.rect.collidepoint(mouse_pos):
            color = self.color_hover
            if pygame.mouse.get_pressed()[0]:  # botão esquerdo do mouse
                color = self.color_active
                self.clicked = True
            else:
                if self.clicked:
                    self.clicked = False
                    return True
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3, border_radius=10)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        return False




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