from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=pos)


class ColisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = pygame.Surface(surface)
        self.rect = self.image.get_rect(topleft=pos)
        