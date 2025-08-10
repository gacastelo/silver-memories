from settings import * 

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class BossCollisionSprite(pygame.sprite.Sprite):
    def __init__(self, boss):
        super().__init__()
        self.boss = boss
        self.rect = boss.collision_rect

    def update(self):
        # Atualiza a posição do rect com o boss
        self.rect.center = self.boss.rect.center
