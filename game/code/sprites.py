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

# Guardião de Astra

class EspinhoShadow(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.width = 150
        self.height = 80
        self.player = player
        self.prev_image = pygame.image.load('images/bosses/guardiao_de_astra/torns/torns-shadow.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.prev_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=pos)

        self.spawn_time = pygame.time.get_ticks()
        self.pos = pos
        self.groups_ = groups  # salva referência aos grupos

    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= 800:  # 100ms
            Espinho(self.pos, self.groups_, self.player)
            self.kill()


class Espinho(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        margemy = 80
        self.position = (pos[0], pos[1]-margemy)
        self.width = 100
        self.height = 172
        self.player = player
        self.prev_image = pygame.image.load('images/bosses/guardiao_de_astra/torns/torn_'+ str(random.randint(1, 4)) + '.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.prev_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=self.position).inflate(-10, -10)

        self.spawn_time = pygame.time.get_ticks()
    
    def update(self,dt):
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= 1000:  # 1s
            self.kill()
        if self.player.hitbox_rect.colliderect(self.rect):
            self.kill()

class Lama(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player):
        super().__init__(groups)
        self.player = player
        self.width = 500
        self.height = 350
        self.image_prev = pygame.image.load('images/bosses/guardiao_de_astra/lama/lama.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (self.width, self.height))
        self.sigma_rect = self.image.get_rect(center=pos)
        self.rect = self.sigma_rect.inflate(-25, -25)

        self.spawn_time = pygame.time.get_ticks()
    
    def player_hit(self):
        if self.player.foot_rect.colliderect(self.rect):
            self.player.speed = 100
        else:
            self.player.speed = 500


    def update(self,dt):
        now = pygame.time.get_ticks()
        self.player_hit()
        if now - self.spawn_time >= 3000:  # 1s
            self.player.speed = 500
            self.kill()

class Vinhas(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.width = 500
        self.height = 350
        self.image = pygame.image.load('images/bosses/guardiao_de_astra/vinhas/vinha.png').convert_alpha()
        self.pos = self.player.rect.center
        self.rect = self.image.get_rect(center=self.pos)
        self.break_rect = self.rect.inflate(25, 25)

        self.spawn_time = pygame.time.get_ticks()
    
    def player_stuck(self):
        if self.player.rect.colliderect(self.rect):
            self.player.speed = 0
            self.player.pode_defender = False

    def player_break(self):
        if self.player.attacking:
            if self.player.attack_hitbox.colliderect(self.break_rect):
                self.player.pode_defender = True
                self.player.speed = 500
                self.kill()
    
    def update(self, dt):
        self.player_stuck()
        self.player_break()