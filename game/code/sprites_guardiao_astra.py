from settings import *
#==========================================#

           # Guardião de Astra

#==========================================#

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
        margemy = 0
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
            self.player.reset_speed()


    def update(self,dt):
        now = pygame.time.get_ticks()
        self.player_hit()
        if now - self.spawn_time >= 3000:  # 1s
            self.player.reset_speed()
            self.kill()

class Vinhas(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.width = 250
        self.height = 250
        self.image_prev = pygame.image.load('images/bosses/guardiao_de_astra/vinhas/'+ str(random.randint(0, 2))+'.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (self.width, self.height))
        self.pos = self.player.rect.center
        self.rect = self.image.get_rect(center=self.pos)
        self.break_rect = self.rect.inflate(25, 25)

        self.spawn_time = pygame.time.get_ticks()

        self.ultima_troca = 0
        self.delay = 300
    
    def player_stuck(self):
        if self.player.rect.colliderect(self.rect):
            self.player.speed = 0
            self.player.pode_defender = False

    def player_break(self):
        if self.player.attacking:
            if self.player.attack_hitbox.colliderect(self.break_rect):
                self.player.pode_defender = True
                self.player.reset_speed()
                self.kill()
    
    def animate(self):
        self.image_prev = pygame.image.load('images/bosses/guardiao_de_astra/vinhas/'+ str(random.randint(0, 2))+'.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image_prev, (self.width, self.height))
    
    def update(self, dt):
        now = pygame.time.get_ticks()
        self.player_stuck()
        self.player_break()

        if now - self.ultima_troca >= self.delay:
            self.animate()
            self.ultima_troca = now

