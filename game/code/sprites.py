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

class Weakspot(pygame.sprite.Sprite):
    def __init__(self, boss, groups, direction):
        super().__init__(groups)
        self.boss = boss
        self.direction = direction
        self.image = pygame.Surface((30, 50))  # tamanho inicial
        self.image.fill((255, 0, 0))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.update_position(direction)

    def update_position(self, direction):
        if direction in ('left', 'right'):
            self.image = pygame.Surface((30, 50))
        else:  # up ou down
            self.image = pygame.Surface((50, 30))

        self.image.fill((255, 0, 0))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        #print(f"[DEBUG] Atualizando posição do ponto fraco: {direction}")

        if direction == 'left':
            self.rect.midleft = self.boss.rect.midright
            self.rect.x -= 35
        elif direction == 'right':
            self.rect.midright = self.boss.rect.midleft
            self.rect.x += 35
        elif direction == 'up':
            self.rect.midtop = self.boss.rect.midbottom
            self.rect.y -= 35
        elif direction == 'down':
            self.rect.midbottom = self.boss.rect.midtop
            self.rect.y += 35

    def on_hit(self, amount):
        if self.boss.is_player_behind():
            print("[DEBUG] Ponto fraco atingido!")
            self.boss.take_damage(amount, is_weak=True)
