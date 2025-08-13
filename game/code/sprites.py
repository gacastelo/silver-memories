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


# Boss


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
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))  # tamanho inicial
        self.image.fill((255, 0, 0))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.offset = 35

        self.update_position(direction)

    def update_position(self, direction):
        if direction in ('left', 'right'):
            self.image = pygame.Surface((self.width, self.height))
        else:  # up ou down
            self.image = pygame.Surface((self.height, self.width))

        self.image.fill((255, 0, 0))
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        #print(f"[DEBUG] Atualizando posição do ponto fraco: {direction}")

        if direction == 'left':
            self.rect.midleft = self.boss.rect.midright
            self.rect.x -= self.offset
        elif direction == 'right':
            self.rect.midright = self.boss.rect.midleft
            self.rect.x += self.offset
        elif direction == 'up':
            self.rect.midtop = self.boss.rect.midbottom
            self.rect.y -= self.offset
        elif direction == 'down':
            self.rect.midbottom = self.boss.rect.midtop
            self.rect.y += self.offset

    def on_hit(self, amount):
        if self.boss.is_player_behind():
            print("[DEBUG] Ponto fraco atingido!")
            self.boss.take_damage(amount, is_weak=True)

class EspinhoShadow(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.width = 30
        self.height = 16
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 255, 0))  # verde
        self.rect = self.image.get_rect(center=pos)

        self.spawn_time = pygame.time.get_ticks()
        self.pos = pos
        self.groups_ = groups  # salva referência aos grupos

    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= 400:  # 100ms
            Espinho(self.pos, self.groups_)
            self.kill()


class Espinho(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        margemy = 27
        self.position = (pos[0], pos[1]-margemy)
        self.width = 25
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 51, 0))  # marrom
        self.rect = self.image.get_rect(center=self.position)

        self.spawn_time = pygame.time.get_ticks()
    
    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= 1000:  # 1s
            self.kill()

class Lama(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.player = player
        self.width = 500
        self.height = 350
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 255))  # azul
        self.rect = self.image.get_rect(center=pos)

        self.spawn_time = pygame.time.get_ticks()
    
    def player_hit(self):
        if self.player.rect.colliderect(self.rect):
            self.player.speed = 100
        else:
            self.player.speed = 500


    def update(self,dt):
        now = pygame.time.get_ticks()
        self.player_hit()
        if now - self.spawn_time >= 3000:  # 1s
            self.kill()
